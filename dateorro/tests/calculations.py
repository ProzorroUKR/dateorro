import pytest
from datetime import datetime, timedelta
from dateorro.calculations import calc_working_datetime, calc_normalized_datetime
from dateorro.messages import FULL_DATE_DELTA_MESSAGE


calendar = {"2018-01-01": True, "2018-01-05": True}

# Test calendar:
# 2018-12-28 - Thu
# 2018-12-29 - Fri (holiday)
# 2017-12-30 - Sat (weekend)
# 2017-12-31 - Sun (weekend)
# 2018-01-01 - Mon (holiday)
# 2018-01-02 - Tue
# 2018-01-03 - Wed
# 2018-01-04 - Thu
# 2018-01-05 - Fri (holiday)
# 2018-01-06 - Sat (weekend)
# 2018-01-07 - Sun (weekend)
# 2018-01-08 - Mon


@pytest.mark.parametrize(
    "dt,delta,expected",
    [
        (
            # Test starts on non working day
            datetime(2018, 1, 1, 12, 0, 0),
            timedelta(days=1),
            datetime(2018, 1, 3, 0, 0, 0),
        ),
        (
            # Test starts on working
            datetime(2018, 1, 2, 12, 0, 0),
            timedelta(days=1),
            datetime(2018, 1, 3, 12, 0, 0),
        ),
        (
            # Test ends before non working
            datetime(2018, 1, 2, 12, 0, 0),
            timedelta(days=2),
            datetime(2018, 1, 4, 12, 0, 0),
        ),
        (
            # Test ends on non working
            datetime(2018, 1, 2, 12, 0, 0),
            timedelta(days=3),
            datetime(2018, 1, 8, 12, 0, 0),
        ),
        (
            # Test ends after non working
            datetime(2018, 1, 2, 12, 0, 0),
            timedelta(days=4),
            datetime(2018, 1, 9, 12, 0, 0),
        ),
        (
            # Test starts on non working and ends between working and non working
            datetime(2018, 1, 1, 12, 30, 0),
            timedelta(days=3),
            datetime(2018, 1, 5, 0, 0, 0),
        ),
        (
            # Test starts on 1st of 2 non working days
            datetime(2017, 12, 31, 12, 0, 0),
            timedelta(days=1),
            datetime(2018, 1, 3, 0, 0, 0),
        ),
        (
            # Test backwards ends on non working
            datetime(2018, 1, 8, 12, 0, 0),
            timedelta(days=-1),
            datetime(2018, 1, 4, 12, 0, 0),
        ),
        (
            # Test backwards starts on non working
            datetime(2018, 1, 5, 12, 0, 0),
            timedelta(days=-1),
            datetime(2018, 1, 4, 0, 0, 0),
        ),
        (
            # Test backwards starts on non working end on non working
            datetime(2018, 1, 5, 12, 0, 0),
            timedelta(days=-3),
            datetime(2018, 1, 2, 0, 0, 0),
        ),
    ],
)
def test_calc_working_datetime(dt, delta, expected):
    assert calc_working_datetime(dt, delta, calendar=calendar) == expected


@pytest.mark.parametrize(
    "dt,delta",
    [
        (datetime(2018, 1, 1, 12, 0, 0), timedelta(days=1, hours=1)),
        (datetime(2018, 1, 1, 12, 0, 0), timedelta(days=1, minutes=1)),
        (datetime(2018, 1, 1, 12, 0, 0), timedelta(days=1, seconds=1)),
        (datetime(2018, 1, 1, 12, 0, 0), timedelta(days=1, milliseconds=1)),
        (datetime(2018, 1, 1, 12, 0, 0), timedelta(days=1, microseconds=1)),
    ],
)
def test_calc_working_datetime_with_time_in_delta(dt, delta):
    dt = datetime(2018, 1, 1, 12, 0, 0)
    delta = timedelta(days=1, hours=1)
    with pytest.raises(ValueError) as excinfo:
        calc_working_datetime(dt, delta)
    assert FULL_DATE_DELTA_MESSAGE == str(excinfo.value)


@pytest.mark.parametrize(
    "dt,ceil,expected",
    [
        (datetime(2018, 1, 1, 12, 0, 0), True, datetime(2018, 1, 2, 0, 0, 0)),
        (datetime(2018, 1, 1, 12, 0, 0), False, datetime(2018, 1, 1, 0, 0, 0)),
    ],
)
def test_calc_normalized_datetime(dt, ceil, expected):
    assert calc_normalized_datetime(dt, ceil=ceil) == expected
