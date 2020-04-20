"""Main Calendar class."""
import datetime
import logging
import os
from threading import RLock
from typing import List, Optional, Union

import yaml
from dateutil.parser import parse as dateutil_parse

logger = logging.getLogger("business")

day_interval = datetime.timedelta(days=1)
INPUT_TYPES = Union[str, datetime.date]


class Mutex:
    """Helper class for thread-safe locking."""

    def __init__(self, obj):
        """Initialise reentrant lock."""
        super().__init__()
        self.__obj = obj
        self.lock = RLock()

    def __enter__(self):
        """Acquire lock on entering."""
        self.lock.acquire()
        return self.__obj

    def __exit__(self, *args, **kwargs):
        """Release lock on exit."""
        self.lock.release()


class Calendar:
    """Calendar class."""

    _cache = Mutex(dict())

    additional_load_paths: List[str] = []
    bundled_calendars_path: List[str] = [os.path.join(os.path.dirname(__file__), "data")]

    DAY_NAMES = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    default_working_days = ["mon", "tue", "wed", "thu", "fri"]

    def __init__(
        self,
        holidays: Optional[List[INPUT_TYPES]] = None,
        working_days: Optional[List[str]] = None,
        extra_working_dates: Optional[List[INPUT_TYPES]] = None,
    ) -> None:
        """Initialise Calendar instance."""
        self.holidays = self.parse_dates(holidays or [])
        self.working_days = [w[:3].lower() for w in working_days or self.default_working_days]
        self.extra_working_dates = self.parse_dates(extra_working_dates or [])

        # validations
        for w in self.working_days:
            if w not in self.DAY_NAMES:
                raise ValueError(f"Invalid working day name: {w}")

        for d in self.holidays:
            if d in self.extra_working_dates:
                raise ValueError(f"Holidays cannot be extra working dates: {d}")

        for d in self.extra_working_dates:
            if d.strftime("%a").lower() in self.working_days:
                raise ValueError(f"Extra working dates cannot be on working days: {d}")

    @classmethod
    def load(cls, calendar_str: str):
        """Load a scheme calendar YAML file.

        >>> %timeit -n 100 Calendar.load('bacs')
            23.9 ms ± 228 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
        """
        calendar_directories = cls.additional_load_paths + cls.bundled_calendars_path
        directory_find = [
            dir
            for dir in calendar_directories
            if os.path.exists(os.path.join(dir, f"{calendar_str}.yml"))
        ]

        if len(directory_find) >= 1:
            directory = directory_find[0]
        else:
            raise ValueError(f"No such calendar '{calendar_str}'")

        calendar_filepath = os.path.join(directory, f"{calendar_str}.yml")
        logger.debug(f"Extracting data from {calendar_filepath} yaml file")
        with open(calendar_filepath, "r") as fh:
            calendar_yaml = yaml.safe_load(fh)

        valid_keys = ["holidays", "working_days", "extra_working_dates"]
        for yaml_key in calendar_yaml.keys():
            if yaml_key not in valid_keys:
                raise ValueError(
                    f"Invalid key {yaml_key} found. Only valid keys are: {', '.join(valid_keys)}"
                )

        return cls(
            holidays=calendar_yaml.get("holidays", []),
            working_days=calendar_yaml["working_days"],
            extra_working_dates=calendar_yaml.get("extra_working_dates", []),
        )

    @classmethod
    def load_cache(cls, calendar_str: str):
        """Load a scheme calendar YAML file with cache.

        >>> %timeit Calendar.load_cache('bacs')
            969 ns ± 10.8 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
        """
        with cls._cache as cache:
            if not (calendar_str in cache):
                cache[calendar_str] = cls.load(calendar_str)
            return cache[calendar_str]

    @staticmethod
    def parse_date(input_date_raw: INPUT_TYPES) -> datetime.date:
        """Parse a raw input date.

        >>> d1 = datetime.date(2020, 1, 1)
            %timeit Calendar.parse_date(d1)
            649 ns ± 6.47 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
        >>> d2 = datetime.datetime(2020, 1, 1)
            %timeit Calendar.parse_date(d2)
            582 ns ± 17.6 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
        >>> %timeit Calendar.parse_date("2020-01-01")
            57.7 µs ± 1.47 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
        """
        if isinstance(input_date_raw, datetime.datetime):
            # datetime.datetime is also an instance of datetime.date
            # this also works with pandas.Timestamp
            # so, check datetime type first!
            return input_date_raw.date()
        elif isinstance(input_date_raw, datetime.date):
            return input_date_raw
        elif isinstance(input_date_raw, str):
            return dateutil_parse(input_date_raw).date()
        else:
            raise TypeError(
                f"Unexpected input type {type(input_date_raw)} (supported: str or datetime.date)"
            )

    @staticmethod
    def parse_dates(dates: List[INPUT_TYPES]) -> List[datetime.date]:
        """Parse a list of raw input dates."""
        return [Calendar.parse_date(d) for d in dates]

    def is_holiday(self, input_date: INPUT_TYPES) -> bool:
        """Return true if the date given is a holiday."""
        input_date = self.parse_date(input_date)
        return input_date in self.holidays

    def is_working_day(self, input_date: INPUT_TYPES) -> bool:
        """Return true if the date given is a working day (typically that means a non-weekend day)."""
        input_date = self.parse_date(input_date)
        return input_date.strftime("%a").lower() in self.working_days

    def is_business_day(self, input_date: INPUT_TYPES) -> bool:
        """Return true if the date given is a working day (typically that means a non-weekend day) and not a holiday."""
        input_date = self.parse_date(input_date)
        if self.is_holiday(input_date):
            return False
        elif input_date in self.extra_working_dates:
            return True
        else:
            return self.is_working_day(input_date)

    def business_days_between(self, from_date: INPUT_TYPES, to_date: INPUT_TYPES) -> int:
        """Count the number of business days between two dates.

        This method counts from start of from_date to start of to_date. So,
        business_days_between(mon, weds) = 2 (assuming no holidays)

        To optimise this method we split the range into full weeks and a remaining period.
        We then calculate business days in the full weeks period by multiplying number of weeks by
        number of working days in a week and removing holidays one by one.

        For the remaining period, we just loop through each day and check whether it is a business day.

        >>> calendar = Calendar.load('bacs')
        >>> %timeit calendar.business_days_between(datetime.date(2020, 1, 1), datetime.date(2020, 1, 7))
            89.5 µs ± 4.3 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
        >>> %timeit calendar.business_days_between(datetime.date(2020, 1, 1), datetime.date(2020, 1, 31))
            72.3 µs ± 4.84 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
        >>> %timeit calendar.business_days_between(datetime.date(2020, 1, 1), datetime.date(2020, 12, 31))
            93.6 µs ± 359 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
        """
        from_date = self.parse_date(from_date)
        to_date = self.parse_date(to_date)
        logger.debug(f"Calculating business days between {from_date} and {to_date}")

        # Calculate number of full weeks and remaining days
        days_between_from_to = (to_date - from_date).days
        num_full_weeks, remaining_days = divmod(days_between_from_to, 7)
        remaining_to_date = to_date - (day_interval * remaining_days)
        # First estimate for full week range based on # biz days in a week
        num_biz_days = num_full_weeks * len(self.working_days)

        # Find and remove holidays in full weeks range
        num_holidays = sum(
            1 if self.is_working_day(i) else 0
            for i in self.holidays
            if from_date <= i < remaining_to_date
        )

        # Add extra working dates in full weeks range
        num_extra_working_dates = sum(
            1 for i in self.extra_working_dates if from_date <= i < remaining_to_date
        )

        remaining_range = range((to_date - remaining_to_date).days)
        remaining_days_range = (remaining_to_date + (day_interval * i) for i in remaining_range)
        # Loop through each day in remaining_range and count if a business day
        remaining_business_days = sum(
            1 for date in remaining_days_range if self.is_business_day(date)
        )
        return num_biz_days - num_holidays + num_extra_working_dates + remaining_business_days

    def roll_forward(self, input_date: INPUT_TYPES) -> datetime.date:
        """
        Roll forward to the next business day.

        If the date given is a business day, that day will be returned.
        If the day given is a holiday ornon-working day, the next non-holiday working day will be returned.
        """
        input_date = self.parse_date(input_date)
        while not (self.is_business_day(input_date)):
            input_date += day_interval
        return input_date

    def roll_backward(self, input_date: INPUT_TYPES) -> datetime.date:
        """
        Roll backward to the previous business day.

        If the date given is a business day, that day will be returned.
        If the day given is a holiday or non-working day, the previous non-holiday working day will be returned.
        """
        input_date = self.parse_date(input_date)
        while not (self.is_business_day(input_date)):
            input_date -= day_interval
        return input_date

    def next_business_day(self, input_date: INPUT_TYPES) -> datetime.date:
        """Roll forward to the next business day regardless of whether the given date is a business day or not."""
        input_date = self.parse_date(input_date)
        input_date += day_interval
        while not (self.is_business_day(input_date)):
            input_date += day_interval
        return input_date

    def previous_business_day(self, input_date: INPUT_TYPES) -> datetime.date:
        """Roll backward to the previous business day regardless of whether the given date is a business day or not."""
        input_date = self.parse_date(input_date)
        input_date -= day_interval
        while not (self.is_business_day(input_date)):
            input_date -= day_interval
        return input_date

    def add_business_days(self, input_date: INPUT_TYPES, delta: int) -> datetime.date:
        """Add or subtract a number of business days to a date.

        If a non-business day is given, counting will start from the next business day. So:
            monday + 1 = tuesday
            friday + 1 = monday
            sunday + 1 = tuesday
            friday - 1 = thursday
            monday - 1 = friday
            sunday - 1 = thursday

        >>> calendar = Calendar.load('bacs')
        >>> %timeit calendar.add_business_days(datetime.date(2020, 1, 1), 1)
            22.6 µs ± 1.14 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
        >>> %timeit calendar.add_business_days(datetime.date(2020, 1, 1), 100)
            1.05 ms ± 7.4 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
        """
        input_date = self.parse_date(input_date)
        logger.debug(f"Adding {delta} business days to {input_date}")
        if delta == 0:
            return input_date
        elif delta < 0:
            input_date = self.roll_backward(input_date)
        else:
            input_date = self.roll_forward(input_date)

        for i in range(abs(delta)):
            if delta < 0:
                input_date = self.previous_business_day(input_date)
            else:
                input_date = self.next_business_day(input_date)
        return input_date

    def get_business_day_of_month(self, input_date: INPUT_TYPES) -> int:
        """Get the business day of the month for a given input date.

        >>> calendar = Calendar.load('bacs')
        >>> %timeit calendar.get_business_day_of_month(datetime.date(2020, 1, 1))
            48.5 µs ± 621 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
        >>> %timeit calendar.get_business_day_of_month(datetime.date(2020, 1, 31))
            77.2 µs ± 590 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
        """
        input_date = self.parse_date(input_date)
        return self.business_days_between(input_date.replace(day=1), input_date + day_interval)
