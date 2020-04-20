from datetime import date

from dateutil.parser import parse as dateutil_parse


def parse_date_noniso(input_date_str: str) -> date:
    """Parse test dates in %d/%m/%y format."""
    return dateutil_parse(input_date_str, dayfirst=True).date()
