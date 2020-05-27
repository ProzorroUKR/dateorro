from datetime import datetime, time, timedelta
from dateorro.messages import ZERO_DELTA_MESSAGE, FULL_DATE_DELTA_MESSAGE


def calc_datetime(dt, delta, accelerator=None):
    """
    Calculate date with time delta.

        :param dt: initial datetime object
        :param delta: timedelta object to increase dt
        :param accelerator: acceleration number
        :return: result datetime object
    """
    return dt + (delta / (accelerator or 1))


def calc_working_datetime(dt, delta, midnight=True, calendar=None):
    """
    Calculate working date with time delta.

        :param dt: initial datetime object
        :param delta: timedelta object to increase dt
        :param midnight: boolean to allow midnight
            of non working day (eg. 00:00 of Saturday)
        :param calendar: working days calendar
        :return: result datetime object

    Example usage::

        >>> calc_working_datetime(
        ...     datetime(2018, 1, 5, 12, 0),
        ...     timedelta(calendar=1),
        ...     calendar={
        ...        '2018-01-04': True,
        ...        '2018-01-07': False
        ...     }
        ... )
        datetime.datetime(2018, 1, 8, 12, 0)

        >>> calc_working_datetime(
        ...     datetime(2018, 1, 4),
        ...     timedelta(calendar=1),
        ...     midnight=True,
        ...     calendar={
        ...        '2018-01-04': True,
        ...        '2018-01-07': False
        ...     }
        ... )
        datetime.datetime(2018, 1, 6, 0, 0)

        >>> calc_working_datetime(
        ...     datetime(2018, 1, 4),
        ...     timedelta(calendar=1),
        ...     midnight=False,
        ...     calendar={
        ...        '2018-01-04': True,
        ...        '2018-01-07': False
        ...     }
        ... )
        datetime.datetime(2018, 1, 8, 0, 0)

    Example calendar meaning::

        2018-01-04 - Thu (become non working)
        2018-01-05 - Fri
        2018-01-06 - Sat (weekend)
        2018-01-07 - Sun (become working)
        2018-01-08 - Mon
    """
    total_seconds = delta.total_seconds()
    if total_seconds == 0:
        raise ValueError(ZERO_DELTA_MESSAGE)
    if total_seconds != delta.days * 24 * 60 * 60:
        raise ValueError(FULL_DATE_DELTA_MESSAGE)
    calendar = calendar or {}
    backwards = total_seconds < 0
    dt = calc_nearest_working_datetime(dt, backwards, calendar)
    for _ in range(abs(delta.days) - 1):
        dt = calc_next_working_datetime(dt, backwards, calendar)
    if midnight and not backwards and dt.time() == time(0):
        dt = calc_next_datetime(dt, backwards)
    else:
        dt = calc_next_working_datetime(dt, backwards, calendar)
    return dt


def calc_nearest_working_datetime(dt, backwards=False, calendar=None):
    """
    Calculate nearest working datetime.

        :param dt: initial datetime object
        :param backwards: time direction boolean
        :param calendar: working days calendar
        :return: result datetime object
    """
    calendar = calendar or {}
    if check_working_datetime(dt, calendar):
        return dt
    dt = datetime.combine(dt.date(), time(0, tzinfo=dt.tzinfo))
    if not backwards:
        dt += timedelta(1)
    while not check_working_datetime(dt, calendar):
        dt = calc_next_datetime(dt, backwards)
    if backwards:
        dt += timedelta(1)
    return dt


def calc_next_datetime(dt, backwards=False):
    """
    Calculate next datetime with 1 day (24 hours) delta.

        :param dt: initial datetime object
        :param backwards: time direction boolean
        :return: result datetime object
    """
    return dt + timedelta(1 if not backwards else -1)


def calc_next_working_datetime(dt, backwards=False, calendar=None):
    """
    Calculate next working datetime with 1 day (24 hours) delta.

        :param dt: initial datetime object
        :param backwards: time direction boolean
        :param calendar: working days calendar
        :return: result datetime object
    """
    dt = calc_next_datetime(dt, backwards)
    while not check_working_datetime(dt, calendar or {}):
        dt = calc_next_datetime(dt, backwards)
    return dt


def check_working_datetime(dt, calendar=None):
    """
    Check if date is working.

        :param dt: initial datetime object
        :param calendar: working days calendar
        :return: result datetime object

    Example usage::

        >>> check_working_datetime(
        ...     datetime(2018, 1, 4)
        ... )
        True

        >>> check_working_datetime(
        ...     datetime(2018, 1, 4),
        ...     calendar={
        ...        '2018-01-04': True,
        ...        '2018-01-07': False
        ...     }
        ... )
        False

    Example calendar meaning::

        2018-01-04 - Thu (become non working)
        2018-01-05 - Fri
        2018-01-06 - Sat (weekend)
        2018-01-07 - Sun (become working)
        2018-01-08 - Mon
    """
    calendar = calendar or {}
    date_str = dt.date().isoformat()
    return not any(
        [
            calendar.get(date_str, True) and dt.isoweekday() in [6, 7],
            calendar.get(date_str, False),
        ]
    )


def calc_normalized_datetime(dt, ceil=False):
    """
    Calculate normalized date (eg. 2019-01-01 12:20 -> 2019-01-01 00:00).

        :param dt: initial datetime object
        :param ceil: ceil boolean
        :return: result datetime object

    Example usage::

        >>> calc_normalized_datetime(
        ...     datetime(2018, 1, 5, 12, 0)
        ... )
        datetime.datetime(2018, 1, 5, 0, 0)

        >>> calc_normalized_datetime(
        ...     datetime(2018, 1, 5, 12, 0), ceil=True
        ... )
        datetime.datetime(2018, 1, 6, 0, 0)

    """
    if dt.time() != time(0):
        normalized = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        if ceil:
            return normalized + timedelta(1)
        return normalized
    return dt
