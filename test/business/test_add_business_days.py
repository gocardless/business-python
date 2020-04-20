import unittest
from datetime import timedelta

from business.calendar import Calendar
from conftest import parse_date_noniso

day_interval = timedelta(days=1)


class TestAddBusinessDays(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(holidays=["Tuesday 1st Jan, 2013"],)
        self.delta = 2

    def test_add_zero_days(self):
        test_date = parse_date_noniso("Wednesday 2nd Jan, 2013")
        result = self.calendar.add_business_days(test_date, 0)
        assert result == test_date

    def test_given_a_business_day_and_a_period_that_includes_only_business_days(self):
        test_date = parse_date_noniso("Wednesday 2nd Jan, 2013")
        assert (
            self.calendar.add_business_days(test_date, self.delta)
            == test_date + self.delta * day_interval
        )

    def test_given_a_business_day_and_a_period_that_includes_a_weekend(self):
        test_date = parse_date_noniso("Friday 4th Jan, 2013")
        assert (
            self.calendar.add_business_days(test_date, self.delta)
            == test_date + (self.delta + 2) * day_interval
        )

    def test_given_a_business_day_and_a_period_that_includes_a_working_date_weekend(self):
        test_date = parse_date_noniso("Friday 4th Jan, 2013")
        calendar = Calendar(
            holidays=["Tuesday 1st Jan, 2013"], extra_working_dates=["Sunday 6th Jan, 2013"]
        )
        assert (
            calendar.add_business_days(test_date, self.delta)
            == test_date + (self.delta + 1) * day_interval
        )

    def test_given_a_business_day_and_a_period_that_includes_a_holiday_day(self):
        test_date = parse_date_noniso("Monday 31st Dec, 2012")
        assert (
            self.calendar.add_business_days(test_date, self.delta)
            == test_date + (self.delta + 1) * day_interval
        )

    def test_given_a_non_business_day(self):
        test_date = parse_date_noniso("Tuesday 1st Jan, 2013")
        assert (
            self.calendar.add_business_days(test_date, self.delta)
            == test_date + (self.delta + 1) * day_interval
        )


class TestSubtractBusinessDays(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(holidays=["Thursday 3rd Jan, 2013"],)
        self.delta = 2

    def test_given_a_business_day_and_a_period_that_includes_only_business_days(self):
        test_date = parse_date_noniso("Wednesday 2nd Jan, 2013")
        assert (
            self.calendar.add_business_days(test_date, -self.delta)
            == test_date - self.delta * day_interval
        )

    def test_given_a_business_day_and_a_period_that_includes_a_weekend(self):
        test_date = parse_date_noniso("Monday 31st Dec, 2012")
        assert (
            self.calendar.add_business_days(test_date, -self.delta)
            == test_date - (self.delta + 2) * day_interval
        )

    def test_given_a_business_day_and_a_period_that_includes_a_working_date_weekend(self):
        test_date = parse_date_noniso("Monday 31st Dec, 2012")
        calendar = Calendar(
            holidays=["Tuesday 1st Jan, 2013"], extra_working_dates=["Saturday 29th Dec, 2012"]
        )
        assert (
            calendar.add_business_days(test_date, -self.delta)
            == test_date - (self.delta + 1) * day_interval
        )

    def test_given_a_business_day_and_a_period_that_includes_a_holiday_day(self):
        test_date = parse_date_noniso("Friday 4th Jan, 2013")
        assert (
            self.calendar.add_business_days(test_date, -self.delta)
            == test_date - (self.delta + 1) * day_interval
        )

    def test_given_a_non_business_day(self):
        test_date = parse_date_noniso("Thursday 3rd Jan, 2013")
        assert (
            self.calendar.add_business_days(test_date, -self.delta)
            == test_date - (self.delta + 1) * day_interval
        )


class TestNextBusinessDay(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(holidays=["Tuesday 1st Jan, 2013"],)

    def test_given_a_business_day(self):
        test_date = parse_date_noniso("Wednesday 2nd Jan, 2013")
        assert self.calendar.next_business_day(test_date) == test_date + day_interval

    def test_given_a_non_business_day_with_a_business_day_following_it(self):
        test_date = parse_date_noniso("Tuesday 1st Jan, 2013")
        assert self.calendar.next_business_day(test_date) == test_date + day_interval

    def test_given_a_non_business_day_followed_by_another_non_business_day(self):
        test_date = parse_date_noniso("Saturday 5th Jan, 2013")
        assert self.calendar.next_business_day(test_date) == test_date + (2 * day_interval)


class TestPreviousBusinessDay(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(holidays=["Tuesday 1st Jan, 2013"])

    def test_given_a_business_day(self):
        test_date = parse_date_noniso("Thursday 3nd Jan, 2013")
        assert self.calendar.previous_business_day(test_date) == test_date - day_interval

    def test_given_a_non_business_day_with_a_business_day_preceding_it(self):
        test_date = parse_date_noniso("Tuesday 1st Jan, 2013")
        assert self.calendar.previous_business_day(test_date) == test_date - day_interval

    def test_given_a_non_business_day_preceded_by_another_non_business_day(self):
        test_date = parse_date_noniso("Sunday 6th Jan, 2013")
        assert self.calendar.previous_business_day(test_date) == test_date - (2 * day_interval)


class TestRollForward(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(holidays=["Tuesday 1st Jan, 2013"])

    def test_given_a_business_day(self):
        test_date = parse_date_noniso("Wednesday 2nd Jan, 2013")
        assert self.calendar.roll_forward(test_date) == test_date

    def test_given_a_non_business_day_with_a_business_day_following_it(self):
        test_date = parse_date_noniso("Tuesday 1st Jan, 2013")
        assert self.calendar.roll_forward(test_date) == test_date + day_interval

    def test_given_a_non_business_day_followed_by_another_non_business_day(self):
        test_date = parse_date_noniso("Saturday 5th Jan, 2013")
        assert self.calendar.roll_forward(test_date) == test_date + (2 * day_interval)


class TestRollBackward(unittest.TestCase):
    def setUp(self):
        self.calendar = Calendar(holidays=["Tuesday 1st Jan, 2013"])

    def test_given_a_business_day(self):
        test_date = parse_date_noniso("Wednesday 2nd Jan, 2013")
        assert self.calendar.roll_backward(test_date) == test_date

    def test_given_a_non_business_day_with_a_business_day_preceding_it(self):
        test_date = parse_date_noniso("Tuesday 1st Jan, 2013")
        assert self.calendar.roll_backward(test_date) == test_date - day_interval

    def test_given_a_non_business_day_preceded_by_another_non_business_day(self):
        test_date = parse_date_noniso("Sunday 6th Jan, 2013")
        assert self.calendar.roll_backward(test_date) == test_date - (2 * day_interval)
