# dateorro

Working/calendar date/datetime calculations

## Install

    python setup.py install

## Run tests

    python setup.py test

## Update docs

    pip install pydoc-markdown
    pydocmd simple dateorro.calculations+ > docs.md

## Update readme

    ./README.sh


# dateorro.calculations

## calc_datetime
```python
calc_datetime(dt, delta, accelerator=None)
```

Calculate date with time delta.

    :param dt: initial datetime object
    :param delta: timedelta object to increase dt
    :param accelerator: acceleration number
    :return: result datetime object

## calc_working_datetime
```python
calc_working_datetime(dt, delta, midnight=True, calendar=None)
```

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

## calc_nearest_working_datetime
```python
calc_nearest_working_datetime(dt, backwards=False, calendar=None)
```

Calculate nearest working datetime.

    :param dt: initial datetime object
    :param backwards: time direction boolean
    :param calendar: working days calendar
    :return: result datetime object

## calc_next_datetime
```python
calc_next_datetime(dt, backwards=False)
```

Calculate next datetime with 1 day (24 hours) delta.

    :param dt: initial datetime object
    :param backwards: time direction boolean
    :return: result datetime object

## calc_next_working_datetime
```python
calc_next_working_datetime(dt, backwards=False, calendar=None)
```

Calculate next working datetime with 1 day (24 hours) delta.

    :param dt: initial datetime object
    :param backwards: time direction boolean
    :param calendar: working days calendar
    :return: result datetime object

## check_working_datetime
```python
check_working_datetime(dt, calendar=None)
```

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

## calc_normalized_datetime
```python
calc_normalized_datetime(dt, ceil=False)
```

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


