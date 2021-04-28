import datetime

import pytest
from conftest import parse_date_noniso

from business.calendar import Calendar


def test_parse_date_str_noniso():
    assert parse_date_noniso("6/1/2019") == datetime.date(2019, 1, 6)


def test_parse_date_str_date():
    assert Calendar.parse_date("Jan 1st, 2019") == datetime.date(2019, 1, 1)


def test_parse_date_str_date_iso():
    assert Calendar.parse_date("2019-01-06") == datetime.date(2019, 1, 6)


def test_parse_date_str_datetime():
    assert Calendar.parse_date("2019-01-06T10:30:00") == datetime.date(2019, 1, 6)


def test_parse_date_date():
    assert Calendar.parse_date(datetime.date(2019, 1, 1)) == datetime.date(2019, 1, 1)


def test_parse_date_datetime():
    assert Calendar.parse_date(datetime.datetime(2019, 1, 1)) == datetime.date(2019, 1, 1)


def test_parse_date_raise_boolean():
    with pytest.raises(TypeError):
        Calendar.parse_date(True)


def test_parse_date_raise_numeric():
    with pytest.raises(TypeError):
        Calendar.parse_date(123)


# test Calendar.parse_dates
def test_parse_dates_str():
    assert Calendar.parse_dates(["Jan 1st, 2019", "Jan 6th, 2019"]) == [
        datetime.date(2019, 1, 1),
        datetime.date(2019, 1, 6),
    ]
