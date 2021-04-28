import pytest
from conftest import parse_date_noniso

from business.calendar import Calendar

scenarios_list = [
    {
        "context": "month starts on a business day",
        "scenarios": [
            {
                "context": "including first day",
                "input_date": parse_date_noniso("Tue 1/7/2014"),
                "expected": 1,
            },
            {
                "context": "including holidays & weekend days",
                "input_date": parse_date_noniso("Sun 6/7/2014"),
                "expected": 3,
            },
            {
                "context": "including last day",
                "input_date": parse_date_noniso("Thu 31/7/2014"),
                "expected": 22,
            },
        ],
    },
    {
        "context": "month starts on a holiday",
        "scenarios": [
            {
                "context": "including first day",
                "input_date": parse_date_noniso("Thu 1/5/2014"),
                "expected": 0,
            },
            {
                "context": "including last day",
                "input_date": parse_date_noniso("Sat 31/5/2014"),
                "expected": 21,
            },
        ],
    },
    {
        "context": "month starts on a Sunday",
        "scenarios": [
            {
                "context": "including first day",
                "input_date": parse_date_noniso("Sun 1/6/2014"),
                "expected": 0,
            },
            {
                "context": "including last day",
                "input_date": parse_date_noniso("Mon 30/6/2014"),
                "expected": 21,
            },
        ],
    },
    {
        "context": "month starts on a weekend + working date",
        "scenarios": [
            {
                "context": "including first day",
                "input_date": parse_date_noniso("Sat 1/11/2014"),
                "expected": 1,
            },
            {
                "context": "including last day",
                "input_date": parse_date_noniso("Mon 30/11/2014"),
                "expected": 21,
            },
        ],
    },
]


scenarios = {}
for context_1 in scenarios_list:
    for context_2 in context_1["scenarios"]:
        scenarios[f"{context_1['context']} + {context_2['context']}"] = (
            context_2["input_date"],
            context_2["expected"],
        )


@pytest.fixture
def calendar():
    return Calendar(
        holidays=["Thu 2014-05-01", "Thu 2014-07-03"],
        extra_working_dates=["Sat 2014-11-01"],
    )


@pytest.mark.parametrize(
    "input_date, expected",
    scenarios.values(),
    ids=list(scenarios.keys()),
)
def test_scenario_get_business_day_of_month(calendar, input_date, expected):
    result = calendar.get_business_day_of_month(input_date)
    assert result == expected
