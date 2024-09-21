"""
Creates common reusable code
"""
from __future__ import annotations

import typing
import inspect
from datetime import date
from datetime import datetime


try:
    import numpy
    _HAS_NUMPY = True
except:
    _HAS_NUMPY = False

try:
    import pandas
    _HAS_PANDAS = True
except:
    _HAS_PANDAS = False


MONTH_NAMES: typing.Final[typing.Mapping[str, int]] = {
    datetime(year=2020, month=month_num, day=1).strftime("%B").lower(): month_num
    for month_num in range(1, 13)
}

MONTH_ABBREVIATIONS: typing.Final[typing.Mapping[str, int]] = {
    datetime(year=2020, month=month_num, day=1).strftime("%b").lower(): month_num
    for month_num in range(1, 13)
}


def month_by_name(name: str) -> int:
    if isinstance(name, int):
        return name

    name = name.lower()
    if name in MONTH_NAMES:
        return MONTH_NAMES[name]
    elif name in MONTH_ABBREVIATIONS:
        return MONTH_ABBREVIATIONS[name]

    raise KeyError(f"'{name}' is not a valid month name or abbreviation")


def is_month_name(name: str) -> bool:
    if not isinstance(name, str):
        return False

    name = name.lower()
    return name in MONTH_NAMES or name in MONTH_ABBREVIATIONS


def is_sequence_type(value: typing.Any) -> bool:
    """
    Checks to see if a value is one that can be interpreted as a collection of values

    Why not just use `isinstance(value, typing.Sequence)`? Strings, bytes, and maps ALL count as sequences

    Args:
        value: The value to check

    Returns:
        Whether the passed value is a sequence
    """
    is_collection = value is not None
    is_collection = is_collection and not isinstance(value, (str, bytes, typing.Mapping))
    is_collection = is_collection and isinstance(value, typing.Sequence)

    return is_collection


def value_in_range(
    value: typing.Union[int, float],
    lower_bound: typing.Union[int, float],
    upper_bound: typing.Union[int, float],
    lower_inclusive: bool = None,
    upper_inclusive: bool = None
) -> bool:
    if lower_inclusive is None:
        lower_inclusive = True

    if upper_inclusive is None:
        upper_inclusive = True

    if lower_inclusive:
        above_lower_bound = value >= lower_bound
    else:
        above_lower_bound = value > lower_bound

    if upper_inclusive:
        below_upper_bound = value <= upper_bound
    else:
        below_upper_bound = value < upper_bound

    return above_lower_bound and below_upper_bound


def value_is_number(value: typing.Any) -> bool:
    """
    Whether the passed in value may be interpreted as a number

    Args:
        value: The value to check

    Returns:
        Whether the value may be interpreted as a number
    """
    if isinstance(value, str) and value.isnumeric():
        return True
    elif isinstance(value, bytes) and value.decode().isnumeric():
        return True
    elif _HAS_NUMPY and hasattr(type(value), "__mro__") and numpy.number in inspect.getmro(type(value)):
        return True

    return isinstance(value, int) or isinstance(value, float) or isinstance(value, complex)


def month_and_day_are_valid(month_number: typing.Union[int, str, float], day_of_month: typing.Union[int, str, float]):
    if isinstance(month_number, str) and not (month_number.isdigit() or is_month_name(month_number)):
        raise ValueError(
            f"Cannot determine a day number from a month and day - the passed in month must be numeric. "
            f"Received {month_number}"
        )
    elif is_month_name(month_number):
        month_number = month_by_name(month_number)
    elif isinstance(month_number, str):
        month_number = int(float(month_number))

    if isinstance(day_of_month, str) and not day_of_month.isdigit():
        raise ValueError(
            f"Cannot determine a day number from a month and day - the passed in day must be numeric. "
            f"Received {day_of_month}"
        )
    elif isinstance(day_of_month, str):
        day_of_month = int(float(day_of_month))

    if not isinstance(day_of_month, (int, float)) or not value_in_range(day_of_month, 1, 31):
        raise ValueError(
            f"A Day object may not be created - a valid month number was given but '{day_of_month}' "
            f"was passed as a day number, which isn't valid"
        )
    elif not isinstance(month_number, (int, float)):
        raise TypeError(
            f"Can only create a Day from a Month and Day number if a month and day number is passed. "
            f"Received ({month_number}: {type(month_number)}, {day_of_month}: {type(day_of_month)}"
        )
    elif not value_in_range(month_number, 1, 12):
        raise ValueError(f"The only valid month numbers are from 1-12. Received {month_number}")


def day_month_sequence_is_valid(day_month_sequence: typing.Sequence[typing.Union[int, float, str]]):
    valid_value_types = (int, float, str)

    if not is_sequence_type(day_month_sequence):
        raise TypeError(
            f"Cannot convert a sequence of values into a Day - received "
            f"'{day_month_sequence}: {type(day_month_sequence)}' which isn't valid"
        )

    if len(day_month_sequence) == 0:
        raise ValueError(f"Cannot convert a sequence of values into a Day - no values were contained.")

    if len(day_month_sequence) == 1:
        year = None
        year_index = None
        month_number = None
        month_index = None
        day_index = 0
        day = day_month_sequence[day_index]
    elif len(day_month_sequence) == 2:
        year_index = None
        month_index = 0
        day_index = 1

        year = None
        month_number = day_month_sequence[month_index]
        day = day_month_sequence[day_index]
    else:
        year_index = 0
        month_index = 1
        day_index = 2

        year, month_number, day = day_month_sequence[:3]

    if isinstance(year, str) and not value_is_number(year):
        raise ValueError(f"Cannot convert {day_month_sequence} into a Day - index {year_index} must be numeric")

    month_type_is_valid = month_number is None or isinstance(month_number, valid_value_types)

    if not (month_type_is_valid or is_month_name(month_number)):
        raise ValueError(f"Cannot convert {day_month_sequence} into a Day - index {month_index} must be numeric")

    if isinstance(month_number, str) and not (value_is_number(month_number) or is_month_name(month_number)):
        raise ValueError(f"Cannot convert {day_month_sequence} into a Day - index {month_index} must be numeric")
    elif is_month_name(month_number):
        month_number = month_by_name(month_number)
    elif isinstance(month_number, str):
        month_number = int(float(month_number))

    if isinstance(day, str) and not value_is_number(day) or not isinstance(day, (int, float, str)):
        raise ValueError(f"Cannot convert {day_month_sequence} into a Day - index {day_index} must be numeric")
    elif isinstance(day, str):
        day = int(float(day))

    if month_number is not None and not value_in_range(month_number, 1, 12):
        raise ValueError(
            f"Cannot convert a sequence of values into a Day - "
            f"the value of the month was out of range: '{month_number}'"
        )

    if not value_in_range(day, 1, 366) and month_number is None:
        raise ValueError(
            f"Cannot convert a sequence of values into a Day - "
            f"the value for the day must be between 1 and 366 inclusive. Received '{day}'"
        )
    elif not value_in_range(day, 1, 31) and month_number is not None:
        raise ValueError(
            f"Cannot convert a sequence of values into a Day - "
            f"the value for the day must be between 1 and 31 inclusive. Received '{day}'"
        )


def date_map_is_valid(
    date_map: typing.Mapping[typing.Union[typing.Literal["day"], typing.Literal['month'], typing.Literal['year']], int]
):
    if not isinstance(date_map, typing.Mapping):
        raise TypeError(f"Input data must be a mapping if a day is to be created from it. Received '{date_map}'")

    if "day" not in date_map:
        raise KeyError(f"A day must be defined if a mapping will be used to construct a Day. Received '{date_map}'")

    year = date_map.get("year", None)
    month = date_map.get('month', None)
    day = date_map['day']

    if year is not None and not isinstance(year, (int, float, str)):
        raise TypeError(
            f"Cannot create a day from a mapping - the year value is an incorrect type. "
            f"Received {year}: {type(year)}"
        )
    elif isinstance(year, str) and not value_is_number(year):
        raise TypeError(
            f"Cannot create a day from a mapping - the year value is must be numeric. "
            f"Received {year}: {type(year)}"
        )

    if month is not None and not isinstance(month, (int, float, str)):
        raise TypeError(
            f"Cannot create a day from a mapping - the month value is an incorrect type. "
            f"Received {month}: {type(month)}"
        )
    elif isinstance(month, str) and not (value_is_number(month) or is_month_name(month)):
        raise TypeError(
            f"Cannot create a day from a mapping - the month value is must be numeric. "
            f"Received {month}: {type(month)}"
        )
    elif month is not None and not is_month_name(month) and not value_in_range(int(float(month)), 1, 12):
        raise ValueError(
            f"Cannot create a day from a mapping - the month value is out of range ([1, 12]). Received {month}"
        )

    if day is not None and not isinstance(day, (int, float, str)):
        raise TypeError(
            f"Cannot create a day from a mapping - the month value is an incorrect type. "
            f"Received {day}: {type(day)}"
        )
    elif isinstance(day, str) and not value_is_number(day):
        raise TypeError(
            f"Cannot create a day from a mapping - the month value is must be numeric. "
            f"Received {day}: {type(day)}"
        )
    elif month is not None and not value_in_range(int(float(day)), 1, 31):
        raise ValueError(
            f"Cannot create a day from a mapping - the day value is out of range ([1, 31]). Received {day}"
        )
    elif not value_in_range(int(float(day)), 1, 366):
        raise ValueError(
            f"Cannot create a day from a mapping - the day value is out of range ([1, 366]). Received {day}"
        )


def datetime64_to_datetime(value) -> datetime:
    if _HAS_NUMPY:
        timestamp = ((value - numpy.datetime64("1970-01-01T00:00:00")) / numpy.timedelta64(1, 's'))
        return datetime.fromtimestamp(timestamp)
    else:
        raise NotImplementedError(f"Cannot convert a numpy datetime64 value to a datetime - numpy is not available")


def timestamp_to_datetime(value) -> datetime:
    if _HAS_PANDAS:
        return datetime(
            year=value.year,
            month=value.month,
            day=value.day,
            hour=value.hour,
            minute=value.minute,
            second=value.second
        )
    else:
        raise NotImplementedError(f"Cannot convert a pandas timestamp value to a datetime - pandas is not available")


def datetime_value_to_date(value) -> date:
    if isinstance(value, date):
        return value
    elif isinstance(value, datetime) or _HAS_PANDAS and isinstance(value, pandas.Timestamp):
        return value.date()
    elif _HAS_NUMPY and isinstance(value, numpy.datetime64):
        return datetime64_to_datetime(value).date()

    raise TypeError(
        f"'{value}: {type(value)}' could not be interpretted as a date value - only datetime.date, datetime.datetime, "
        f"numpy.datetime64, and pandas.Timestamp are valid"
    )


def date_value_to_datetime(value) -> datetime:
    if isinstance(value, datetime):
        return value
    elif isinstance(value, date) or _HAS_PANDAS and isinstance(value, pandas.Timestamp):
        return datetime(
            year=value.year,
            month=value.month,
            day=value.day
        )
    elif _HAS_NUMPY and isinstance(value, numpy.datetime64):
        return datetime64_to_datetime(value)

    raise TypeError(
        f"'{value}: {type(value)}' could not be interpreted as a datetime value - "
        f"only datetime.date, datetime.datetime, numpy.datetime64, and pandas.Timestamp are valid"
    )