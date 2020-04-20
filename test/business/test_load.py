import datetime
import os
import unittest
from glob import glob
from time import time

import pytest

from business.calendar import Calendar
from conftest import parse_date_noniso

bundled_calendars_path = os.path.join(os.path.dirname(__file__), "../..", "business", "data")


class TestLoad(unittest.TestCase):
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "data")
    Calendar.additional_load_paths = [fixture_path]

    def test_when_given_a_valid_calendar(self):
        calendar = Calendar.load("weekdays")
        assert isinstance(calendar, Calendar)

    def test_when_given_a_calendar_from_a_custom_directory(self):
        calendar = Calendar.load("ecb")
        assert isinstance(calendar, Calendar)

    def test_that_also_exists_as_a_default_calendar(self):
        calendar = Calendar.load("bacs")
        assert calendar.is_business_day(parse_date_noniso("25th December 2014"))

    def test_when_given_a_calendar_that_does_not_exist(self):
        with pytest.raises(ValueError):
            Calendar.load("invalid-calendar")

    def test_when_given_a_calendar_that_has_invalid_keys(self):
        with pytest.raises(ValueError):
            Calendar.load("invalid-keys")


class TestLoadCache(unittest.TestCase):
    def test_when_given_a_valid_calendar(self):
        calendar = Calendar.load_cache("weekdays")
        assert isinstance(calendar, Calendar)

    def test_cache_loads_faster_second_time(self):
        start_time_1 = time()
        Calendar.load_cache("bacs")
        duration_1 = time() - start_time_1

        start_time_2 = time()
        Calendar.load_cache("bacs")
        duration_2 = time() - start_time_2

        assert duration_2 < duration_1


@pytest.mark.parametrize(
    "calendar_file",
    [
        os.path.splitext(os.path.basename(path))[0]
        for path in glob(os.path.join(bundled_calendars_path, "*.yml"))
    ],
)
def test_bundled_calendars_should_load_without_issues(calendar_file):
    calendar = Calendar.load(calendar_file)
    assert len(calendar.working_days) >= 1


class TestSetWorkingDays(unittest.TestCase):
    def test_when_given_valid_working_days(self):
        working_days = ["mon", "fri"]
        calendar = Calendar(working_days=working_days)
        assert calendar.working_days == working_days

    def test_when_given_valid_working_days_that_are_unnormalised(self):
        calendar = Calendar(working_days=["Monday", "Friday"])
        assert calendar.working_days == ["mon", "fri"]

    def test_when_given_an_invalid_business_day(self):
        with pytest.raises(ValueError):
            Calendar(working_days=["Notaday"])

    def test_when_given_none(self):
        calendar = Calendar(working_days=None)
        assert calendar.working_days == Calendar.default_working_days


class TestSetHolidays(unittest.TestCase):
    def test_when_given_valid_working_days(self):
        calendar = Calendar(holidays=["1st Jan, 2013"])
        assert len(calendar.holidays) == 1
        assert [isinstance(d, datetime.date) for d in calendar.holidays]

    def test_when_given_none(self):
        calendar = Calendar(holidays=None)
        assert len(calendar.holidays) == 0


class TestSetExtraWorkingDates(unittest.TestCase):
    def test_when_given_valid_working_days(self):
        calendar = Calendar(extra_working_dates=["Sun 06/01/2013"])
        assert len(calendar.extra_working_dates) == 1
        assert [isinstance(d, datetime.date) for d in calendar.extra_working_dates]

    def test_when_given_none(self):
        calendar = Calendar(extra_working_dates=None)
        assert len(calendar.extra_working_dates) == 0

    def test_when_holiday_is_also_a_working_date(self):
        with pytest.raises(ValueError):
            Calendar(holidays=["2018-01-06"], extra_working_dates=["2018-01-06"])

    def test_when_working_date_on_working_day(self):
        with pytest.raises(ValueError):
            Calendar(working_days=["monday"], extra_working_dates=["Monday 26th Mar, 2018"])
