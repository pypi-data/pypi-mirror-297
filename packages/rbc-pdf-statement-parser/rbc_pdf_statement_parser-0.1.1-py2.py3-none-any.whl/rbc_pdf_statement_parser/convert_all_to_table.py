"""Convert all PDF files in a directory to nice table files."""

from __future__ import annotations

import argparse
import uuid
from pathlib import Path

import fitz
import orjson
import pandas as pd
import polars as pl
import tabula

from rbc_pdf_statement_parser.util import (
    convert_short_month_to_number,
    extract_payer_name,
    get_date_between_two_dates,
    get_statement_metadata,
)


def read_pdf_metadata(input_file: Path) -> dict:
    """Read a PDF and extract statement metadata from the first page's text."""
    with fitz.open(input_file) as doc:
        first_page = doc[0]
        text = first_page.get_text()

    metadata = get_statement_metadata(text)
    metadata["file_name"] = input_file.name
    return metadata


def parse_single_page_table(df: pl.DataFrame) -> pl.DataFrame:
    """Parse a single page of a PDF statement into a transaction table."""
    assert len(df.columns) == 4, f"Expected 4 columns, got {len(df.columns)}"
    df.columns = [
        "raw_date_and_description",
        "cheques_and_debits",
        "deposits_and_credits",
        "raw_balance",
    ]

    # Strip all cells.
    df = df.with_columns(
        pl.all().str.strip_chars(),
    )

    # Filter to only rows after the start row.
    df = df.with_row_index("row_num")
    df = df.with_columns(
        row_str_concat=pl.concat_str(pl.all().fill_null(""), separator=""),
    ).with_columns(
        is_start_row=(
            pl.col("row_str_concat").str.contains(
                r"Date.+Cheques.+Debits.+Deposits.+Credits.+Balance.+"
            )
        ),
        # Identify the end row by the presence of "Page X of Y" indicator.
        is_end_row=(
            pl.col("row_str_concat")
            .str.contains(r"^\d+\s*of\s+\d+")
            .fill_null(pl.lit(value=False))
        ),
    )

    # Filter to only rows between the start and end rows.
    assert (
        df["is_start_row"].sum() == 1
    ), f"Expected 1 start row, found {df['is_start_row'].sum()}"
    start_row_num = df.filter(pl.col("is_start_row")).select("row_num").item()
    df = df.filter(pl.col("row_num") > pl.lit(start_row_num))
    assert (
        df["is_end_row"].sum() == 1
    ), f"Expected 1 end row, found {df['is_end_row'].sum()}"
    end_row_num = df.filter(pl.col("is_end_row")).select("row_num").item()
    df = df.filter(pl.col("row_num") < pl.lit(end_row_num))

    # Make `raw_date` and `description` columns.
    df = df.with_columns(
        raw_date=pl.col("raw_date_and_description").str.extract(
            r"^(?P<raw_date>\d{2} \w{3})"
        )
    )
    df = df.with_columns(
        description=pl.col("raw_date_and_description").str.extract(
            r"^(\d{2} \w{3}\s+)?(?P<description>.+)", group_index=2
        ),
    )

    # Remove the "Opening balance" first row, as it messes with the fills/
    # backfills/groupings coming up.
    df_before = df
    df = df.filter(
        pl.col("description").str.contains("^Opening balance").not_()
        & pl.col("description").str.contains("^Closing balance").not_()
        # Remove the "Account fees" sum rows. Worry not: the fees are
        # included in the transactions as line items still.
        & pl.col("description").str.contains("^Account Fees: ").not_()
    )
    assert (df_before.height - df.height) <= 3, (
        "Expected to remove <=3 rows, "
        f"removed {df_before.height - df.height}"
    )

    # Merge up the descriptions into a long string. The description column
    # may be split into multiple rows. Row 1...n-1 have null
    # `cheques_and_debits` and `deposits_and_credits` values, while the
    # last row of each transaction has the actual value.
    df = df.with_columns(
        INTERNAL_is_last_row_of_group=(
            pl.col("cheques_and_debits").is_not_null()
            | pl.col("deposits_and_credits").is_not_null()
        ),
    )
    df = df.with_columns(
        INTERNAL_description_row_group_uuid=pl.col(
            "INTERNAL_is_last_row_of_group"
        ).map_elements(
            lambda x: str(uuid.uuid4()) if x else None,
            return_dtype=pl.String,
        ),
    )
    df = df.with_columns(
        pl.col("INTERNAL_description_row_group_uuid").fill_null(
            strategy="backward"
        ),
    )
    df = (
        df
        # Group-by, and aggregate each as a list.
        .group_by(
            "INTERNAL_description_row_group_uuid", maintain_order=True
        ).agg(
            pl.col("raw_date").drop_nulls(),
            pl.col("description").drop_nulls(),
            pl.col("cheques_and_debits").drop_nulls(),
            pl.col("deposits_and_credits").drop_nulls(),
            pl.col("raw_balance").drop_nulls(),
            # Dropping 'row_num' col here, and several others.
        )
    )

    # Assert that each col only has max 1 value per group.
    for col in [
        "raw_date",
        "cheques_and_debits",
        "deposits_and_credits",
        "raw_balance",
    ]:
        unique_list_vals = df[col].list.len().unique().sort().to_list()
        assert unique_list_vals in ([0, 1], [0], [1]), (
            f"Expected 0 or 1 value per group for {col}, got "
            f"{df[col].list.len().unique().to_list()}"
        )

        df = df.with_columns(
            pl.col(col).list.first(),
        )

    # Clean up the descriptions.
    df = df.with_columns(
        description=pl.col("description").list.join(" "),
    )

    # Clean up the numerical columns.
    for col in [
        "cheques_and_debits",
        "deposits_and_credits",
        "raw_balance",
    ]:
        df = df.with_columns(pl.col(col).str.replace(",", "").str.to_decimal())

    df = df.with_columns(
        pl.col("raw_date").fill_null(strategy="forward"),
        signed_amount=(
            pl.col("deposits_and_credits").fill_null(0)
            - pl.col("cheques_and_debits").fill_null(0)
        ),
        payer_name=(
            pl.col("description")
            .map_elements(extract_payer_name, return_dtype=pl.String)
            .str.to_titlecase()
        ),
    )
    df = df.with_columns(
        credit_or_debit=(
            pl.when(pl.col("signed_amount") > 0)
            .then(pl.lit("credit"))
            .when(pl.col("signed_amount") < 0)
            .then(pl.lit("debit"))
            .otherwise(pl.lit("zero"))
        )
    )

    df = df.drop(["INTERNAL_description_row_group_uuid"])

    return df  # noqa: RET504


def read_pdf_transactions(input_file: Path) -> pl.DataFrame:
    """Read a PDF and extract the transactions from the remaining pages."""
    dfs = tabula.read_pdf(
        input_file,
        pages="all",
        # Parse the whole page instead of guessing a small region.
        guess=False,
        multiple_tables=True,
        relative_columns=True,  # Force `columns` arg to be percentages.
        # columns=[14.4, 51.7, 67.8, 90.2], # noqa: ERA001
        columns=[47.67, 65.1, 83.14],
    )
    metadata = read_pdf_metadata(input_file)

    output_df_list: list[pl.DataFrame] = []

    for page_number, pd_df in enumerate(dfs, 1):
        assert isinstance(pd_df, pd.DataFrame)

        df = pl.from_pandas(pd_df, include_index=False)

        if (df.height < 10) and any(
            x.startswith("Serial #") for x in df[df.columns[0]] if x
        ):
            # This is a table on a page with cheque images, not transactions.
            # Skip it.
            print(f"Skipping page {page_number} with cheque image(s): {df}")
            continue

        df = parse_single_page_table(df)

        # Create the date column (currently like "06 Dec" for Dec 6; no year).
        df = df.with_columns(
            date=pl.col("raw_date").map_elements(
                lambda x: get_date_between_two_dates(
                    month_number=convert_short_month_to_number(
                        x.split(" ")[1]
                    ),
                    day_number=int(x.split(" ")[0]),
                    start_date=metadata["opening_date"],
                    end_date=metadata["closing_date"],
                ),
                return_dtype=pl.Date,
            )
        )

        # Add some metadata columns.
        df = df.with_columns(
            META_statement_start_date=metadata["opening_date"],
            META_statement_end_date=metadata["closing_date"],
            META_file_name=pl.lit(input_file.name, dtype=pl.String),
            META_page_number=pl.lit(page_number, dtype=pl.Int32),
        )

        output_df_list.append(df)

    df = pl.concat(output_df_list)

    return df  # noqa: RET504


def process_entire_directory(input_dir: Path, output_dir: Path) -> None:
    """Convert all PDF files in a directory to nice files."""
    df_transactions_list: list[pl.DataFrame] = []
    metadata_list: list[dict] = []

    for pdf_file in input_dir.glob("*.pdf"):
        assert isinstance(pdf_file, Path)
        print(f"Processing {pdf_file}")
        metadata: dict = read_pdf_metadata(pdf_file)
        df_transactions: pl.DataFrame = read_pdf_transactions(pdf_file)

        # Save files.
        metadata_file = output_dir / (pdf_file.stem + "_metadata.json")
        metadata_file.write_bytes(
            orjson.dumps(metadata, option=orjson.OPT_INDENT_2)
        )
        transactions_file = output_dir / (pdf_file.stem + "_transactions.csv")
        df_transactions.write_csv(transactions_file)

        metadata_list.append(metadata)
        df_transactions_list.append(df_transactions)

    print(f"Processed {len(df_transactions_list)} PDF files.")

    # Combine all transactions into one big DataFrame.
    df_all_transactions: pl.DataFrame = pl.concat(df_transactions_list)
    df_all_transactions = df_all_transactions.sort("date", maintain_order=True)
    df_all_transactions.write_csv(
        all_transactions_file := output_dir / "00_all_transactions.csv"
    )
    df_all_transactions.write_parquet(
        _all_transactions_parquet := output_dir / "00_all_transactions.pq"
    )

    # Save metadata to a CSV file.
    df_metadata = pl.DataFrame(metadata_list)
    df_metadata = df_metadata.sort("opening_date", maintain_order=True)
    df_metadata.write_csv(
        all_metadata_file := output_dir / "00_all_statement_metadata.csv"
    )
    df_metadata.write_parquet(
        _all_metadata_parquet := output_dir / "00_all_statement_metadata.pq"
    )

    print(f"Saved all transactions to: {all_transactions_file}")
    print(f"Saved all metadata to: {all_metadata_file}")


def main() -> None:
    """Convert all PDF files in a directory to nice table files.

    Argparse wrapped version of `process_entire_directory`.
    """
    parser = argparse.ArgumentParser(
        description="Convert all PDF files in a directory to nice table files."
    )
    parser.add_argument(
        "input_dir", type=Path, help="The directory containing the PDF files."
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="The directory where the table files will be saved.",
    )

    args = parser.parse_args()

    process_entire_directory(Path(args.input_dir), Path(args.output_dir))


if __name__ == "__main__":
    main()
