import unittest

from business.calendar import Calendar
from conftest import parse_date_noniso


# A set of examples that are supposed to work when given Date and Time
# objects. The implementation slightly differs, so i's worth running the
# tests for both Date *and* Time.
class TestIsBusinessDay(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(
            holidays=["9am, Tuesday 1st Jan, 2013"],
            extra_working_dates=["9am, Sunday 6th Jan, 2013"],
        )

    def test_when_given_a_business_day(self):
        test_date = parse_date_noniso("9am, Wednesday 2nd Jan, 2013")
        assert self.calendar.is_business_day(test_date) is True

    def test_when_given_a_non_business_day(self):
        test_date = parse_date_noniso("9am, Saturday 5th Jan, 2013")
        assert self.calendar.is_business_day(test_date) is False

    def test_when_given_a_business_day_that_is_a_holiday(self):
        test_date = parse_date_noniso("9am, Tuesday 1st Jan, 2013")
        assert self.calendar.is_business_day(test_date) is False

    def test_when_given_a_non_business_day_that_is_a_working_date(self):
        test_date = parse_date_noniso("9am, Sunday 6th Jan, 2013")
        assert self.calendar.is_business_day(test_date) is True
