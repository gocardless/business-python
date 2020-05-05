# Business (Python)

[![circleci-badge](https://circleci.com/gh/gocardless/business-python.svg?style=shield)](https://app.circleci.com/pipelines/github/gocardless/business-python) [![pypi-badge](https://badge.fury.io/py/business-python.svg)](https://badge.fury.io/py/business-python)

Date calculations based on business calendars. (Python 3.6+)

Python implementation of https://github.com/gocardless/business

## Documentation

To get business, simply:

```bash
$ pip install business-python
```

## Version 2.0.0 breaking changes

In version 2.0.0 we have removed the bundled calendars. If you still need these they are available on [v1.0.1](https://github.com/gocardless/business-python/tree/74fe7e4068e0f16b68e7478f8b5ca1cc52f9a7d0/business/data).

### Migration

- Download/create calendars to a directory within your project eg: `lib/calendars`
- Change your code to include the `load_path` for your calendars
- Continue using `.load("my_calendar")` as usual

```python
# lib/calendars contains yml files
Calendar.load_paths = ['lib/calendars']
calendar = Calendar.load("my_calendar")
```

### Getting started

Get started with business by creating an instance of the calendar class, passing in a hash that specifies which days of the week are considered working days, and which days are holidays.

```python
from business.calendar import Calendar

calendar = Calendar(
  working_days=["monday", "tuesday", "wednesday", "thursday", "friday"],
  # array items are either parseable date strings, or real datetime.date objects
  holidays=["January 1st, 2020", "April 10th, 2020"],
  extra_working_dates=[],
)
```

`extra_working_dates` key makes the calendar to consider a weekend day as a working day.

If `working_days` is missing, then common default is used (mon-fri).
If `holidays` is missing, "no holidays" assumed.
If `extra_working_dates` is missing, then no changes in `working_days` will happen.

Elements of `holidays` and `extra_working_dates` may be either strings that `Calendar.parse_date()` can understand, or YYYY-MM-DD (which is considered as a Date by Python YAML itself).

#### Calendar YAML file example

```yaml
# lib/calendars/my_calendar.yml
working_days:
  - Monday
  - Sunday
holidays:
  - 2017-01-08 # Same as January 8th, 2017
extra_working_dates:
  - 2020-12-26 # Will consider 26 Dec 2020 (A Saturday), a working day
```

The `load_cache` method allows a thread safe way to avoid reloading the same calendar multiple times, and provides a performant way to dynamically load calendars for different requests.

#### Using business-python

Define your calendars in a folder eg: `lib/calendars` and set this directory  on `Calendar.load_paths=`

```python
Calendar.load_paths = ['lib/calendars']
calendar = Calendar.load_cache("my_calendar")
```

### Input data types

The `parse_date` method is used to process the input date(s) in each method and return a `datetime.date` object.

```python
Calendar.parse_date("2019-01-01")
# => datetime.date(2019, 1, 1)
```

Supported data types are:

- `datetime.date`
- `datetime.datetime`
- `pandas.Timestamp` (treated as `datetime.datetime`)
- date string parseable by [`dateutil.parser.parse`](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse)

`numpy.datetime64` is not supported, but can be converted to `datetime.date`:

```python
numpy.datetime64('2014-06-01T23:00:05.453000000').astype('M8[D]').astype('O')
# =>  datetime.date(2014, 6, 1)
```

### Checking for business days

To check whether a given date is a business day (falls on one of the specified working days or extra working dates, and is not a holiday), use the `is_business_day` method on `Calendar`.

```python
calendar.is_business_day("Monday, 8 June 2020")
# => true
calendar.is_business_day("Sunday, 7 June 2020")
# => false
```

### Business day arithmetic

> For our purposes, date-based calculations are sufficient. Supporting time-based calculations as well makes the code significantly more complex. We chose to avoid this extra complexity by sticking solely to date-based mathematics.

The `add_business_days` method is used to perform business day arithmetic on dates.

```python
input_date = Calendar.parse_date("Thursday, 12 June 2014")
calendar.add_business_days(input_date, 4).strftime("%A, %d %B %Y")
# => "Wednesday, 18 June 2014"
calendar.add_business_days(input_date, -4).strftime("%A, %d %B %Y")
# => "Friday, 06 June 2014"
```

The `roll_forward` and `roll_backward` methods snap a date to a nearby business day. If provided with a business day, they will return that date. Otherwise, they will advance (forward for `roll_forward` and backward for `roll_backward`) until a business day is found.

```python
input_date = Calendar.parse_date("Saturday, 14 June 2014")
calendar.roll_forward(input_date).strftime("%A, %d %B %Y")
# => "Monday, 16 June 2014"
calendar.roll_backward(input_date).strftime("%A, %d %B %Y")
# => "Friday, 13 June 2014"
```

In contrast, the `next_business_day` and `previous_business_day` methods will always move to a next or previous date until a business day is found, regardless if the input provided is a business day.

```python
input_date = Calendar.parse_date("Monday, 9 June 2014")
calendar.roll_forward(input_date).strftime("%A, %d %B %Y")
# => "Monday, 09 June 2014"
calendar.next_business_day(input_date).strftime("%A, %d %B %Y")
# => "Tuesday, 10 June 2014"
calendar.previous_business_day(input_date).strftime("%A, %d %B %Y")
# => "Friday, 06 June 2014"
```

To count the number of business days between two dates, pass the dates to `business_days_between`. This method counts from start of the first date to start of the second date. So, assuming no holidays, there would be two business days between a Monday and a Wednesday.

```python
from datetime import timedelta

input_date = Calendar.parse_date("Saturday, 14 June 2014")
calendar.business_days_between(input_date, input_date + timedelta(days=7))
# => 5
```

The `get_business_day_of_month` method return the running total of business days for a given date in that month. This method counts the number of business days from the start of the first day of the month to the given input date.

```python
input_date = Calendar.parse_date("Thursday, 12 June 2014")
calendar.get_business_day_of_month(input_date)
# => 9
```
## License & Contributing

- This is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
- Bug reports and pull requests are welcome on GitHub at https://github.com/gocardless/business-python.

GoCardless ♥ open source. If you do too, come [join us](https://gocardless.com/about/jobs).
