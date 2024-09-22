"""Move all PDF files to a new folder with a new name."""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import date, datetime
from pathlib import Path

import fitz


def get_statement_dates(input_file_path: Path) -> tuple[date, date]:
    """Read a PDF and extract the statement dates from the first page's text.

    Args:
    ----
        input_file_path (Path): The path to the PDF file.

    Returns:
    -------
        tuple[date, date]: The start and end dates of the statement.

    """
    with fitz.open(input_file_path) as doc:
        first_page = doc[0]
        text = first_page.get_text()

    # Extract the statement date from the first page's text.
    # Business Account Statement\s+May 3, 2024 to June 5, 2024

    match = re.search(
        r"Business Account Statement\s+(\w+ \d+, \d+) to (\w+ \d+, \d+)", text
    )
    assert match, f"Could not find statement date in {input_file_path}"

    start_date = datetime.strptime(match.group(1), "%B %d, %Y").date()
    end_date = datetime.strptime(match.group(2), "%B %d, %Y").date()

    return start_date, end_date


def copy_to_renamed_folder(input_dir: Path, output_folder: Path) -> None:
    """Copy all PDF files to a new folder with a new name."""
    count = 0
    for pdf_file in input_dir.glob("**/*.pdf"):
        start_date, end_date = get_statement_dates(pdf_file)
        new_file_name = (
            f"CalgaryToSpace RBC Statement - {start_date} to {end_date}.pdf"
        )
        new_file_path = output_folder / new_file_name

        if new_file_path.exists():
            print(
                f"Note: {new_file_name} already exists in {output_folder}. "
                "May be a duplicate in the source?"
            )

        shutil.copy(pdf_file, new_file_path)
        count += 1

    print(f"Moved {count} PDF files to {output_folder}")


def main() -> None:
    """Move all PDF files to a new folder with a new name."""
    parser = argparse.ArgumentParser(
        description="Move all PDF files to a new folder with a new name."
    )
    parser.add_argument(
        "input_dir", type=Path, help="The directory containing the PDF files."
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="The directory where the PDF files will be copied.",
    )

    args = parser.parse_args()

    copy_to_renamed_folder(Path(args.input_dir), Path(args.output_dir))


if __name__ == "__main__":
    main()
