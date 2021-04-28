import pytest
from conftest import parse_date_noniso

from business.calendar import Calendar

scenarios_list = [
    {
        "context": "starting on a business day",
        "date_1": parse_date_noniso("Mon 2/6/2014"),
        "scenarios": [
            {
                "context": "ending on a business day",
                "scenarios": [
                    {
                        "context": "including only business days",
                        "date_2": parse_date_noniso("Thu 5/6/2014"),
                        "expected": 3,
                    },
                    {
                        "context": "including only business days & weekend days",
                        "date_2": parse_date_noniso("Mon 9/6/2014"),
                        "expected": 5,
                    },
                    {
                        "context": "including only business days, weekend days & working date",
                        "date_1": parse_date_noniso("Thu 29/5/2014"),
                        "date_2": parse_date_noniso("Tue 3/6/2014"),
                        "expected": 4,
                    },
                    {
                        "context": "including only business days & holidays",
                        "date_1": parse_date_noniso("Mon 9/6/2014"),
                        "date_2": parse_date_noniso("Fri 13/6/2014"),
                        "expected": 3,
                    },
                    {
                        "context": "including business, weekend days, and holidays",
                        "date_2": parse_date_noniso("Fri 13/6/2014"),
                        "expected": 8,
                    },
                    {
                        "context": "including business, weekend, holiday days & working date",
                        "date_1": parse_date_noniso("Thu 26/6/2014"),
                        "date_2": parse_date_noniso("Tue 1/7/2014"),
                        "expected": 3,
                    },
                ],
            },
            {
                "context": "ending on a weekend day",
                "scenarios": [
                    {
                        "context": "including only business days & weekend days",
                        "date_2": parse_date_noniso("Sun 8/6/2014"),
                        "expected": 5,
                    },
                    {
                        "context": "including only business days, weekend days & working date",
                        "date_1": parse_date_noniso("Thu 29/5/2014"),
                        "date_2": parse_date_noniso("Tue 3/6/2014"),
                        "expected": 4,
                    },
                    {
                        "context": "including business, weekend days, and holidays",
                        "date_2": parse_date_noniso("Sat 14/6/2014"),
                        "expected": 9,
                    },
                    {
                        "context": "including business, weekend, holiday days & working date",
                        "date_1": parse_date_noniso("Thu 26/6/2014"),
                        "date_2": parse_date_noniso("Wed 2/7/2014"),
                        "expected": 4,
                    },
                ],
            },
            {
                "context": "ending on a holiday",
                "scenarios": [
                    {
                        "context": "including only business days & holidays",
                        "date_1": parse_date_noniso("Mon 9/6/2014"),
                        "date_2": parse_date_noniso("Thu 12/6/2014"),
                        "expected": 3,
                    },
                    {
                        "context": "including business, weekend days, and holidays",
                        "date_2": parse_date_noniso("Thu 12/6/2014"),
                        "expected": 8,
                    },
                    {
                        "context": "including business, weekend, holiday days & working date",
                        "date_1": parse_date_noniso("Wed 28/5/2014"),
                        "date_2": parse_date_noniso("Thu 12/6/2014"),
                        "expected": 12,
                    },
                ],
            },
            {
                "context": "ending on a working date",
                "date_1": parse_date_noniso("Fri 4/7/2014"),
                "scenarios": [
                    {
                        "context": "including only business days & working date",
                        "date_2": parse_date_noniso("Sat 5/7/2014"),
                        "expected": 1,
                    },
                    {
                        "context": "including business, weekend days & working date",
                        "date_2": parse_date_noniso("Tue 8/7/2014"),
                        "expected": 3,
                    },
                    {
                        "context": "including business, weekend days, holidays & working date",
                        "date_1": parse_date_noniso("Wed 25/6/2014"),
                        "date_2": parse_date_noniso("Tue 8/7/2014"),
                        "expected": 9,
                    },
                ],
            },
        ],
    },
    {
        "context": "starting on a weekend",
        "date_1": parse_date_noniso("Sat 7/6/2014"),
        "scenarios": [
            {
                "context": "ending on a business day",
                "scenarios": [
                    {
                        "context": "including only business days & weekend days",
                        "date_2": parse_date_noniso("Mon 9/6/2014"),
                        "expected": 0,
                    },
                    {
                        "context": "including business, weekend days & working date",
                        "date_1": parse_date_noniso("Sat 31/5/2014"),
                        "date_2": parse_date_noniso("Tue 3/6/2014"),
                        "expected": 2,
                    },
                    {
                        "context": "including business, weekend days, and holidays",
                        "date_2": parse_date_noniso("Fri 13/6/2014"),
                        "expected": 3,
                    },
                    {
                        "context": "including business, weekend, holiday days & working date",
                        "date_1": parse_date_noniso("Sat 31/5/2014"),
                        "date_2": parse_date_noniso("Fri 13/6/2014"),
                        "expected": 9,
                    },
                ],
            },
            {
                "context": "ending on a weekend day",
                "scenarios": [
                    {
                        "context": "including only business days & weekend days",
                        "date_2": parse_date_noniso("Sun 8/6/2014"),
                        "expected": 0,
                    },
                    {
                        "context": "including business, weekend days & working date",
                        "date_1": parse_date_noniso("Sat 31/5/2014"),
                        "date_2": parse_date_noniso("Sun 8/6/2014"),
                        "expected": 6,
                    },
                    {
                        "context": "including business, weekend days, and holidays",
                        "date_2": parse_date_noniso("Sat 14/6/2014"),
                        "expected": 4,
                    },
                    {
                        "context": "including business, weekend, holiday days & working date",
                        "date_1": parse_date_noniso("Sat 31/5/2014"),
                        "date_2": parse_date_noniso("Sun 14/6/2014"),
                        "expected": 10,
                    },
                ],
            },
            {
                "context": "ending on a holiday",
                "scenarios": [
                    {
                        "context": "including business, weekend days, and holidays",
                        "date_2": parse_date_noniso("Thu 12/6/2014"),
                        "expected": 3,
                    },
                    {
                        "context": "including business, weekend days & working date",
                        "date_1": parse_date_noniso("Sat 31/5/2014"),
                        "date_2": parse_date_noniso("Thu 12/6/2014"),
                        "expected": 9,
                    },
                ],
            },
            {
                "context": "ending on a working date",
                "date_1": parse_date_noniso("Sat 31/5/2014"),
                "scenarios": [
                    {
                        "context": "including only weekend days & working date",
                        "date_2": parse_date_noniso("Sat 2/6/2014"),
                        "expected": 1,
                    },
                    {
                        "context": "including business, weekend days & working date",
                        "date_2": parse_date_noniso("Tue 4/6/2014"),
                        "expected": 3,
                    },
                    {
                        "context": "including business, weekend days, holidays & working date",
                        "date_2": parse_date_noniso("Fri 13/6/2014"),
                        "expected": 9,
                    },
                ],
            },
        ],
    },
    {
        "context": "starting on a holiday",
        "date_1": parse_date_noniso("Thu 12/6/2014"),
        "scenarios": [
            {
                "context": "ending on a business day",
                "scenarios": [
                    {
                        "context": "including only business days & holidays",
                        "date_2": parse_date_noniso("Fri 13/6/2014"),
                        "expected": 0,
                    },
                    {
                        "context": "including business, weekend days, and holidays",
                        "date_2": parse_date_noniso("Thu 19/6/2014"),
                        "expected": 3,
                    },
                    {
                        "context": "including business, weekend days, holidays & working date",
                        "date_1": parse_date_noniso("Fri 27/6/2014"),
                        "date_2": parse_date_noniso("Tue 1/7/2014"),
                        "expected": 2,
                    },
                ],
            },
            {
                "context": "ending on a weekend day",
                "scenarios": [
                    {
                        "context": "including business, weekend days, and holidays",
                        "date_2": parse_date_noniso("Sun 15/6/2014"),
                        "expected": 1,
                    },
                    {
                        "context": "including business, weekend days, holidays & working date",
                        "date_1": parse_date_noniso("Fri 27/6/2014"),
                        "date_2": parse_date_noniso("Sun 29/6/2014"),
                        "expected": 1,
                    },
                ],
            },
            {
                "context": "ending on a holiday",
                "scenarios": [
                    {
                        "context": "including only business days & holidays",
                        "date_1": parse_date_noniso("Wed 18/6/2014"),
                        "date_2": parse_date_noniso("Fri 20/6/2014"),
                        "expected": 1,
                    },
                    {
                        "context": "including business, weekend days, and holidays",
                        "date_2": parse_date_noniso("Wed 18/6/2014"),
                        "expected": 3,
                    },
                    {
                        "context": "including business/weekend days, holidays & working date",
                        "date_1": parse_date_noniso("27/5/2014"),
                        "date_2": parse_date_noniso("Thu 12/6/2014"),
                        "expected": 12,
                    },
                ],
            },
            {
                "context": "ending on a working date",
                "date_1": parse_date_noniso("Fri 27/6/2014"),
                "scenarios": [
                    {
                        "context": "including only holiday & working date",
                        "date_2": parse_date_noniso("Sun 29/6/2014"),
                        "expected": 1,
                    },
                    {
                        "context": "including holiday, weekend days & working date",
                        "date_2": parse_date_noniso("Mon 30/6/2014"),
                        "expected": 1,
                    },
                    {
                        "context": "including business, weekend days, holidays & working date",
                        "date_2": parse_date_noniso("Wed 2/7/2014"),
                        "expected": 3,
                    },
                ],
            },
        ],
    },
    {
        "context": "starting on a working date",
        "date_1": parse_date_noniso("Sun 1/6/2014"),
        "scenarios": [
            {
                "context": "ending on a business day",
                "scenarios": [
                    {
                        "context": "including only working date & working day",
                        "date_2": parse_date_noniso("Wed 4/6/2014"),
                        "expected": 3,
                    },
                    {
                        "context": "including working date, working & weekend days",
                        "date_2": parse_date_noniso("Tue 10/6/2014"),
                        "expected": 7,
                    },
                    {
                        "context": "including working date, working & weekend days & holiday",
                        "date_2": parse_date_noniso("Fri 13/6/2014"),
                        "expected": 9,
                    },
                ],
            },
            {
                "context": "ending on a weekend day",
                "date_1": parse_date_noniso("Sat 28/6/2014"),
                "scenarios": [
                    {
                        "context": "including only working date & weekend day",
                        "date_2": parse_date_noniso("Sun 29/6/2014"),
                        "expected": 1,
                    },
                    {
                        "context": "including working date, weekend & working days",
                        "date_1": parse_date_noniso("Sat 5/7/2014"),
                        "date_2": parse_date_noniso("Wed 9/7/2014"),
                        "expected": 3,
                    },
                    {
                        "context": "including working date, weekend & working days & holiday",
                        "date_2": parse_date_noniso("Fri 4/7/2014"),
                        "expected": 4,
                    },
                ],
            },
            {
                "context": "ending on a holiday",
                "date_1": parse_date_noniso("Sat 28/6/2014"),
                "scenarios": [
                    {
                        "context": "including only working date & holiday",
                        "holidays": ["Mon 2/6/2014"],
                        "date_1": parse_date_noniso("Sun 1/6/2014"),
                        "date_2": parse_date_noniso("Mon 2/6/2014"),
                        "expected": 1,
                    },
                    {
                        "context": "including working date, holiday & weekend day",
                        "holidays": ["Mon 30/6/2014"],
                        "date_2": parse_date_noniso("Mon 30/6/2014"),
                        "expected": 1,
                    },
                    {
                        "context": "including working date, holiday, weekend & working days",
                        "date_2": parse_date_noniso("Thu 3/7/2014"),
                        "expected": 4,
                    },
                ],
            },
            {
                "context": "ending on a working date",
                "date_1": parse_date_noniso("Fri 27/6/2014"),
                "scenarios": [
                    {
                        "context": "including working dates, weekend & working days",
                        "date_1": parse_date_noniso("Sat 28/6/2014"),
                        "date_2": parse_date_noniso("Sat 5/7/2014"),
                        "expected": 5,
                    },
                ],
            },
        ],
    },
    {
        "context": "other",
        "date_1": parse_date_noniso("Thu 19/6/2014"),
        "scenarios": [
            {
                "context": "if a calendar has a holiday on a non-working (weekend) day",
                "scenarios": [
                    {
                        "context": "for a range less than a week long",
                        "date_1": parse_date_noniso("Thu 19/6/2014"),
                        "date_2": parse_date_noniso("Tue 24/6/2014"),
                        "expected": 2,
                    },
                    {
                        "context": "for a range more than a week long",
                        "date_1": parse_date_noniso("Mon 16/6/2014"),
                        "date_2": parse_date_noniso("Tue 24/6/2014"),
                        "expected": 4,
                    },
                ],
            },
        ],
    },
]


scenarios = {}
for context_1 in scenarios_list:
    for context_2 in context_1["scenarios"]:
        for context_3 in context_2["scenarios"]:
            scenarios[
                f"{context_1['context']} + {context_2['context']} + {context_3['context']}"
            ] = (
                context_3.get("date_1", (context_2.get("date_1", context_1["date_1"]))),
                context_3["date_2"],
                context_3.get("holidays"),
                context_3["expected"],
            )


extra_working_dates = ["Sun 2014-06-01", "Sat 2014-06-28", "Sat 2014-07-05"]


@pytest.fixture
def calendar():
    return Calendar(
        holidays=[
            "Tue 2014-05-27",
            "Thu 2014-06-12",
            "Wed 2014-06-18",
            "Fri 2014-06-20",
            "Sun 2014-06-22",
            "Fri 2014-06-27",
            "Thu 2014-07-03",
        ],
        extra_working_dates=extra_working_dates,
    )


@pytest.mark.parametrize(
    "date_1, date_2, holidays, expected", scenarios.values(), ids=list(scenarios.keys()),
)
def test_scenario_business_days_between(calendar, date_1, date_2, holidays, expected):
    if holidays:
        calendar_override = Calendar(holidays=holidays, extra_working_dates=extra_working_dates)
        result = calendar_override.business_days_between(date_1, date_2)
    else:
        result = calendar.business_days_between(date_1, date_2)
    assert result == expected
