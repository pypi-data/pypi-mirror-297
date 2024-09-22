"""Tests for the `util.py` file."""

from datetime import date

import pytest

from rbc_pdf_statement_parser.util import (
    extract_payer_name,
    get_date_between_two_dates,
    get_statement_metadata,
)


def test_get_statement_metadata_1() -> None:
    """Test the get_statement_metadata function."""
    data = """
RANDOM TEXT HERE
Opening balance on January 1, 2024
$12,345.67
Total deposits & credits (3)
+ 4,321.00
Total cheques & debits (5)
- 2,345.89
Closing balance on February 1, 2024
= $14,320.78
Account number:
12345
987-654-3
RANDOM TEXT HERE
    """

    expected_output = {
        "opening_date": date(2024, 1, 1),
        "opening_balance": 12345.67,
        "deposits": 4321.00,
        "debits": -2345.89,
        "closing_date": date(2024, 2, 1),
        "closing_balance": 14320.78,
        "account_number": "12345",
        "routing_number": "987-654-3",
    }

    result = get_statement_metadata(data)
    assert result == expected_output


def test_get_statement_metadata_2() -> None:
    """Test the get_statement_metadata function."""
    data = """
RANDOM TEXT AND ADDRESS HERE
Opening balance on March 10, 2024
$25,600.50
Total deposits & credits (4)
+ 5,780.25
Total cheques & debits (7)
- 8,150.75
Closing balance on April 10, 2024
= $23,230.00
Account number:
54321
321-987-6
RANDOM TEXT HERE
    """

    expected_output = {
        "opening_date": date(2024, 3, 10),
        "opening_balance": 25600.50,
        "deposits": 5780.25,
        "debits": -8150.75,
        "closing_date": date(2024, 4, 10),
        "closing_balance": 23230.00,
        "account_number": "54321",
        "routing_number": "321-987-6",
    }

    result = get_statement_metadata(data)
    assert result == expected_output


def test_get_statement_metadata_3() -> None:
    """Test the get_statement_metadata function."""
    data = """
RANDOM TEXT HERE
RANDOM TEXT AND ADDRESS HERE
Opening balance on September 17, 2021
$0.00
Total deposits & credits (0)
+ 0.00
Total cheques & debits (1)
- 5.00
Closing balance on October 5, 2021
= -$5.00
Account number:
12345
123-456-7
RANDOM TEXT HERE
    """

    expected_output = {
        "opening_date": date(2021, 9, 17),
        "opening_balance": 0.00,
        "deposits": 0,
        "debits": -5,
        "closing_date": date(2021, 10, 5),
        "closing_balance": -5.00,
        "account_number": "12345",
        "routing_number": "123-456-7",
    }

    result = get_statement_metadata(data)
    assert result == expected_output


def test_get_date_between_two_dates() -> None:
    """Test the `get_date_between_two_dates()` function."""
    assert get_date_between_two_dates(
        5, 15, date(2024, 1, 1), date(2024, 12, 31)
    ) == date(2024, 5, 15)

    assert get_date_between_two_dates(
        12, 25, date(2024, 1, 1), date(2024, 12, 31)
    ) == date(2024, 12, 25)

    # In between years; in less year.
    assert get_date_between_two_dates(
        month_number=12,
        day_number=25,
        start_date=date(2024, 12, 15),
        end_date=date(2025, 1, 15),
    ) == date(2024, 12, 25)

    # In between years; in greater year.
    assert get_date_between_two_dates(
        month_number=1,
        day_number=5,
        start_date=date(2024, 12, 15),
        end_date=date(2025, 1, 15),
    ) == date(2025, 1, 5)

    # On first date.
    assert get_date_between_two_dates(
        month_number=1,
        day_number=15,
        start_date=date(2024, 1, 15),
        end_date=date(2024, 2, 15),
    ) == date(2024, 1, 15)

    # On last date.
    assert get_date_between_two_dates(
        month_number=2,
        day_number=15,
        start_date=date(2024, 1, 15),
        end_date=date(2024, 2, 15),
    ) == date(2024, 2, 15)

    # Day before first date.
    with pytest.raises(ValueError, match="is not between"):
        get_date_between_two_dates(
            month_number=1,
            day_number=14,
            start_date=date(2024, 1, 15),
            end_date=date(2024, 2, 15),
        )

    # Day after last date.
    with pytest.raises(ValueError, match="is not between"):
        get_date_between_two_dates(
            month_number=2,
            day_number=16,
            start_date=date(2024, 1, 15),
            end_date=date(2024, 2, 15),
        )


def test_extract_payer_name() -> None:
    """Test the `extract_payer_name()` function."""
    assert (
        extract_payer_name("Interac purchase - 9410 CLASSIFIED YYC")
        == "9410 CLASSIFIED YYC"
    )
    assert extract_payer_name("Misc Payment U OF T") == "U OF T"
    assert (
        extract_payer_name("Funds transfer credit TT COMPANY123")
        == "TT COMPANY123"
    )
    assert extract_payer_name("Funds transfer COMPANY NAME") == "COMPANY NAME"
    assert (
        extract_payer_name("Funds transfer credit COMPANY NAME")
        == "COMPANY NAME"
    )
    assert (
        extract_payer_name("Funds transfer fee COMPANY NAME") == "COMPANY NAME"
    )
    assert (
        extract_payer_name("e-Transfer - Autodeposit PERSON NAME CABs4NaH")
        == "PERSON NAME"
    )
    assert (
        extract_payer_name("e-Transfer sent Person Middle Last")
        == "Person Middle Last"
    )
    assert (
        extract_payer_name(
            "e-Transfer - Autodeposit SOMEONE NAME LAST ANOTHER "
            "436123079E3C4A2A9E44E591513FCDF3"
        )
        == "SOMEONE NAME LAST ANOTHER"
    )

    # Should return the original description if no match.
    assert (
        extract_payer_name("INTERAC e-Transfer fee")
        == "INTERAC e-Transfer fee"
    )
