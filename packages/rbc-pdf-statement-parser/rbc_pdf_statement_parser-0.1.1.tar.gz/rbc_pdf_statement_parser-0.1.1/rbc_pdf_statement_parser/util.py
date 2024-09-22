"""Utility for parsing statement metadata from a PDF statement."""

import re
from datetime import date, datetime


def get_statement_metadata(text: str) -> dict:
    """Parse the statement metadata from the text of a PDF statement.

    Args:
    ----
        text (str): The text of the PDF statement. Can be just the first page.

    Returns:
    -------
        dict: A dictionary containing the statement metadata.

    """
    pattern = re.compile(
        r"""
Opening\sbalance\son\s(?P<opening_date>[A-Za-z]+\s\d{1,2},\s\d{4})\s*
(?P<opening_balance>-?\$[\d,]+\.\d{2})\s*
Total\sdeposits\s&\scredits\s\(\d+\)\s*
(?P<deposits>[-+]\s[\d,]+\.\d{2})\s*
Total\s+cheques\s+&\s+debits\s\(\d+\)\s*
(?P<debits>[-+]\s[\d,]+\.\d{2})\s*
Closing\sbalance\son\s(?P<closing_date>[A-Za-z]+\s\d{1,2},\s\d{4})\s*
=\s(?P<closing_balance>-?\$[\d,]+\.\d{2})\s*
Account\snumber:\s*
(?P<account_number>\d+)\s*
(?P<routing_number>[\d-]+)\s*
        """.strip(),
    )

    match = pattern.search(text)
    if match is None:
        msg = "Could not find statement metadata in the text."
        raise ValueError(msg)

    result = match.groupdict()

    for col in ["opening_date", "closing_date"]:
        if result[col]:
            result[col] = datetime.strptime(
                result[col].strip(), "%B %d, %Y"
            ).date()

    for col in ["opening_balance", "deposits", "debits", "closing_balance"]:
        if result[col]:
            result[col] = float(re.sub(r"[,\$+ ]+", "", result[col]))

    return result


def convert_short_month_to_number(short_month: str) -> int:
    """Convert a short month name to a month number."""
    return {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }[short_month]


def get_date_between_two_dates(
    month_number: int, day_number: int, start_date: date, end_date: date
) -> date:
    """Get the date between two dates based on the month and day number.

    Raises
    ------
        ValueError: If the date is not between the two dates.

    """
    year = start_date.year
    date_to_return = date(year, month_number, day_number)
    if start_date <= date_to_return <= end_date:
        return date_to_return

    date_to_return = date(year + 1, month_number, day_number)
    if start_date <= date_to_return <= end_date:
        return date_to_return

    msg = f"Date {date_to_return} is not between {start_date} and {end_date}"
    raise ValueError(msg)


def extract_payer_name(description: str) -> str:
    """Extract the payer name from a transaction description."""
    # Check for each pattern in order of expected match
    if (
        match := re.search(r"Interac purchase - (.+)", description)
        or (
            match := re.search(
                r"Funds transfer\s*(?:credit|fee)? (.+)", description
            )
        )
        or (
            match := re.search(
                r"e-Transfer - Autodeposit (.+?)\s\w+$", description
            )
        )
        or (match := re.search(r"e-Transfer sent (.+)", description))
        or (match := re.search(r"Misc Payment (.+)", description))
    ):
        return match.group(1)

    # Return description as a fallback (or customize based on needs)
    return description
