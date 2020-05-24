import pytest
from datetime import datetime, timedelta
from dateorro.calculations import (
    calc_datetime,
    calc_working_datetime,
    check_working_datetime,
    calc_normalized_datetime,
)
from dateorro.messages import FULL_DATE_DELTA_MESSAGE


calendar = {"2018-01-01": True, "2018-01-05": True, "2018-01-07": False}

# Test calendar:
# 2018-12-28 - Thu
# 2018-12-29 - Fri
# 2017-12-30 - Sat (weekend)
# 2017-12-31 - Sun (weekend)
# 2018-01-01 - Mon (holiday)
# 2018-01-02 - Tue
# 2018-01-03 - Wed
# 2018-01-04 - Thu
# 2018-01-05 - Fri (holiday)
# 2018-01-06 - Sat (weekend)
# 2018-01-07 - Sun (working weekend)
# 2018-01-08 - Mon


@pytest.mark.parametrize(
    "dt,delta,expected",
    [
        # Test positive delta
        (datetime(2018, 1, 1, 12), timedelta(1), datetime(2018, 1, 2, 12)),
        # Test negative delta
        (datetime(2018, 1, 1, 12), timedelta(-1), datetime(2017, 12, 31, 12)),
    ],
)
def test_calc_datetime(dt, delta, expected):
    assert calc_datetime(dt, delta) == expected


@pytest.mark.parametrize(
    "dt,delta,accelerator,expected",
    [
        # Test no acceleration
        (datetime(2018, 1, 1, 12), timedelta(1), None, datetime(2018, 1, 2, 12)),
        # Test aceeleration 1440
        (datetime(2018, 1, 1, 12), timedelta(1), 1440, datetime(2018, 1, 1, 12, 1)),
    ],
)
def test_calc_datetime_acceleration(dt, delta, accelerator, expected):
    assert calc_datetime(dt, delta, accelerator=accelerator) == expected


@pytest.mark.parametrize(
    "dt,delta,expected",
    [
        # Test starts on non working day
        (datetime(2018, 1, 1, 12), timedelta(1), datetime(2018, 1, 3, 0)),
        # Test starts on working
        (datetime(2018, 1, 2, 12), timedelta(1), datetime(2018, 1, 3, 12)),
        # Test ends before non working
        (datetime(2018, 1, 2, 12), timedelta(2), datetime(2018, 1, 4, 12)),
        # Test ends on non working
        (datetime(2018, 1, 2, 12), timedelta(3), datetime(2018, 1, 7, 12)),
        # Test ends after non working
        (datetime(2018, 1, 2, 12), timedelta(4), datetime(2018, 1, 8, 12)),
        # Test ends between working and non working midnight
        (datetime(2018, 1, 4), timedelta(1), datetime(2018, 1, 5)),
        # Test starts on non working and ends between working and non working
        (datetime(2018, 1, 1, 12, 30), timedelta(3), datetime(2018, 1, 5)),
        # Test starts on 1st of 2 non working days
        (datetime(2017, 12, 31, 12), timedelta(1), datetime(2018, 1, 3)),
        # Test backwards ends on non working midnight
        (datetime(2018, 1, 2), timedelta(-1), datetime(2017, 12, 29)),
        # Test backwards ends on non working
        (datetime(2018, 1, 7, 12), timedelta(-1), datetime(2018, 1, 4, 12)),
        # Test backwards starts on non working
        (datetime(2018, 1, 5, 12), timedelta(-1), datetime(2018, 1, 4)),
        # Test backwards starts on non working and ends between working and non working
        (datetime(2018, 1, 5, 12), timedelta(-3), datetime(2018, 1, 2)),
    ],
)
def test_calc_working_datetime(dt, delta, expected):
    assert calc_working_datetime(dt, delta, calendar=calendar) == expected


@pytest.mark.parametrize(
    "dt,delta,expected",
    [
        # Test ends between working and non working
        (datetime(2018, 1, 4), timedelta(1), datetime(2018, 1, 7)),
        # Test starts on non working and ends between working and non working
        (datetime(2018, 1, 1, 12, 30), timedelta(3), datetime(2018, 1, 7)),
    ],
)
def test_calc_working_datetime_midnight_not_allowed(dt, delta, expected):
    assert calc_working_datetime(dt, delta, False, calendar) == expected


@pytest.mark.parametrize(
    "dt,delta",
    [
        # Test with hours
        (datetime(2018, 1, 1, 12, 0, 0), timedelta(1, hours=1)),
        # Test with minutes
        (datetime(2018, 1, 1, 12, 0, 0), timedelta(1, minutes=1)),
        # Test with seconds
        (datetime(2018, 1, 1, 12, 0, 0), timedelta(1, seconds=1)),
        # Test with milliseconds
        (datetime(2018, 1, 1, 12, 0, 0), timedelta(1, milliseconds=1)),
        # Test with microseconds
        (datetime(2018, 1, 1, 12, 0, 0), timedelta(1, microseconds=1)),
    ],
)
def test_calc_working_datetime_with_time_in_delta(dt, delta):
    with pytest.raises(ValueError) as excinfo:
        calc_working_datetime(dt, delta)
    assert FULL_DATE_DELTA_MESSAGE == str(excinfo.value)


@pytest.mark.parametrize(
    "dt,expected",
    [
        # Test working day
        (datetime(2018, 1, 4), True),
        # Test weekend
        (datetime(2018, 1, 6), False),
        # Test working day on weekend
        (datetime(2018, 1, 7), True),
        # Test holiday
        (datetime(2018, 1, 5), False),
    ],
)
def test_check_working_datetime(dt, expected):
    assert check_working_datetime(dt, calendar=calendar) == expected


@pytest.mark.parametrize(
    "dt,ceil,expected",
    [
        # Test ceil
        (datetime(2018, 1, 1, 12, 0, 0), True, datetime(2018, 1, 2, 0, 0, 0)),
        # Test ceil midnight
        (datetime(2018, 1, 1, 0, 0, 0), True, datetime(2018, 1, 1, 0, 0, 0)),
        # Test not ceil
        (datetime(2018, 1, 1, 12, 0, 0), False, datetime(2018, 1, 1, 0, 0, 0)),
        # Test not ceil midnight
        (datetime(2018, 1, 1, 0, 0, 0), False, datetime(2018, 1, 1, 0, 0, 0)),
    ],
)
def test_calc_normalized_datetime(dt, ceil, expected):
    assert calc_normalized_datetime(dt, ceil=ceil) == expected
