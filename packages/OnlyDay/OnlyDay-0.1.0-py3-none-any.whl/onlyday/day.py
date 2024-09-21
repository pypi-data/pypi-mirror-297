"""
Defines the `Day` data structure
"""
from __future__ import annotations

import typing

from datetime import datetime
from datetime import date
from datetime import timedelta
from datetime import tzinfo

from dateutil.parser import parse as parse_date

from .utilities import date_map_is_valid
from .utilities import date_value_to_datetime
from .utilities import datetime64_to_datetime
from .utilities import day_month_sequence_is_valid
from .utilities import is_month_name
from .utilities import is_sequence_type
from .utilities import month_and_day_are_valid
from .utilities import month_by_name
from .utilities import value_is_number

_HAS_NUMPY = False
_HAS_PANDAS = False

try:
    import numpy
    _HAS_NUMPY = True
except:
    pass

try:
    import pandas
    _HAS_PANDAS = True
except:
    pass


_LEAP_YEAR = 2020


DATE_DICTIONARY = typing.Mapping[
    typing.Union[
        typing.Literal["day"],
        typing.Literal["month"],
        typing.Literal["year"]
    ], typing.Union[int, str]
]
"""
What is to be expected of a dictionary representing a day - the only allowable keys should be 'day', 'month', or 
'year'. 'day' is required, while 'month' and 'year' are appreciated but optional
"""


if _HAS_NUMPY and _HAS_PANDAS:
    datetime_types: typing.Final[typing.Tuple[typing.Type, ...]] = (date, datetime, numpy.datetime64, pandas.Timestamp)
    DATE_REPRESENTATION_TYPE = typing.Union[
        str,
        pandas.Timestamp,
        numpy.datetime64,
        datetime,
        date,
        int,
        DATE_DICTIONARY,
        typing.Sequence[typing.Union[str, int, float]]
    ]
    """The types of objects that may refer to a day"""

    def day_from_datetime_type(datetime_value: typing.Union[datetime_types]) -> int:
        if not isinstance(datetime_value, datetime_types):
            raise TypeError(
                f"Can only retrieve the day from a datetime type if the passed value is a datetime type. "
                f"Received '{type(datetime_value)}'"
            )

        if isinstance(datetime_value, (datetime, date, numpy.core.datetime64)):
            datetime_value = pandas.Timestamp(datetime_value)

        is_leap_year = datetime_value.is_leap_year
        post_leap_day = datetime(datetime_value.year, month=3, day=1, tzinfo=datetime_value.tzinfo)
        if not is_leap_year and datetime_value >= post_leap_day:
            return datetime_value.dayofyear + 1

        return datetime_value.dayofyear
elif _HAS_NUMPY:
    datetime_types: typing.Final[typing.Tuple[typing.Type, ...]] = (date, datetime, numpy.datetime64)
    DATE_REPRESENTATION_TYPE = typing.Union[
        str,
        numpy.datetime64,
        datetime,
        date,
        int,
        DATE_DICTIONARY,
        typing.Sequence[typing.Union[str, int, float]]
    ]
    """The types of objects that may refer to a day"""

    def day_from_datetime_type(datetime_value: typing.Union[datetime_types]) -> int:
        if not isinstance(datetime_value, datetime_types):
            raise TypeError(
                f"Can only retrieve the day from a datetime type if the passed value is a datetime type. "
                f"Received '{type(datetime_value)}'"
            )

        if isinstance(datetime_value, numpy.core.datetime64):
            datetime_value = datetime64_to_datetime(datetime_value)

        is_leap_year = datetime_value.year % 4 == 0
        month = datetime_value.month

        day_of_year = int(datetime_value.strftime("%j"))

        if not is_leap_year and month >= 3:
            day_of_year += 1

        return day_of_year
else:
    datetime_types: typing.Final[typing.Tuple[typing.Type, ...]] = (datetime, date)
    DATE_REPRESENTATION_TYPE = typing.Union[
        str,
        datetime,
        date,
        int,
        DATE_DICTIONARY,
        typing.Sequence[typing.Union[str, int, float]]
    ]
    """The types of objects that may refer to a day"""

    def day_from_datetime_type(datetime_value: typing.Union[datetime_types]) -> int:
        if not isinstance(datetime_value, datetime_types):
            raise TypeError(
                f"Can only retrieve the day from a datetime type if the passed value is a datetime type. "
                f"Received '{type(datetime_value)}'"
            )

        is_leap_year = datetime_value.year % 4 == 0
        month = datetime_value.month

        day_of_year = int(datetime_value.strftime("%j"))

        if not is_leap_year and month >= 3:
            day_of_year += 1

        return day_of_year


if _HAS_PANDAS:
    def day_from_month_and_day(
        month_number: typing.Union[int, float, str],
        day_of_month: typing.Union[int, float, str]
    ) -> int:
        month_and_day_are_valid(month_number, day_of_month)

        if isinstance(month_number, str):
            month_number = int(float(month_number))

        if isinstance(day_of_month, str):
            day_of_month = int(float(day_of_month))

        return pandas.Timestamp(year=_LEAP_YEAR, month=int(month_number), day=int(day_of_month)).dayofyear

    def day_from_sequence(datetime_value: typing.Sequence[typing.Union[str, int, float]]) -> int:
        day_month_sequence_is_valid(datetime_value)

        if len(datetime_value) == 1:
            return day_from_datetime_type(datetime.strptime(f"{_LEAP_YEAR}-{datetime_value[0]}", "%Y-%j"))
        elif len(datetime_value) == 2:
            return pandas.Timestamp(
                year=_LEAP_YEAR,
                month=int(float(datetime_value[0])),
                day=int(float(datetime_value[1]))
            ).dayofyear

        datetime_value = pandas.Timestamp(
            year=int(float(datetime_value[0])),
            month=int(float(datetime_value[1])),
            day=int(float(datetime_value[2]))
        )

        if datetime_value.is_leap_year or datetime_value.month < 3:
            return datetime_value.dayofyear

        return datetime_value.dayofyear + 1
else:
    def day_from_month_and_day(
        month_number: typing.Union[int, float, str],
        day_of_month: typing.Union[int, float, str]
    ) -> int:
        month_and_day_are_valid(month_number, day_of_month)

        if isinstance(month_number, str):
            month_number = month_by_name(month_number) if is_month_name(month_number) else int(float(month_number))

        if isinstance(day_of_month, str):
            day_of_month = int(float(day_of_month))

        return int(datetime(year=_LEAP_YEAR, month=int(month_number), day=int(day_of_month)).strftime("%j"))

    def day_from_sequence(datetime_value: typing.Sequence[typing.Union[str, int, float]]) -> int:
        day_month_sequence_is_valid(datetime_value)

        if len(datetime_value) == 1:
            return day_from_datetime_type(datetime.strptime(f"{_LEAP_YEAR}-{int(float(datetime_value[0]))}", "%Y-%j"))
        elif len(datetime_value) == 2:
            year = _LEAP_YEAR
            month = datetime_value[0]

            if is_month_name(month):
                month = month_by_name(month)
            else:
                month = int(float(month))

            day = int(float(datetime_value[1]))
        else:
            year = int(float(datetime_value[0]))
            month = datetime_value[1]

            if is_month_name(month):
                month = month_by_name(month)
            else:
                month = int(float(month))

            day = int(float(datetime_value[2]))

        return day_from_datetime_type(datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d"))


def day_from_map(datetime_value: DATE_DICTIONARY) -> int:
    date_map_is_valid(datetime_value)

    year = int(float(datetime_value.get("year", _LEAP_YEAR)))
    month = datetime_value.get("month") if "month" in datetime_value else None
    day = int(float(datetime_value['day']))

    if month:
        if is_month_name(month):
            month = month_by_name(month)
        return day_from_datetime_type(datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d"))

    return day_from_datetime_type(datetime.strptime(f"{year}-{day}", "%Y-%j"))


class Day:
    """
    A simple wrapper around an integer value between 1 and 366 to represent a consistent number of a day of a year

    These takes leap year into account, where 2021/5/23 will have the same value as 2020/5/23
    """
    __slots__ = ['__day']

    @classmethod
    def from_epoch(cls, timestamp: float, timezone: tzinfo = None) -> Day:
        date_from_timestamp = datetime.fromtimestamp(timestamp, tz=timezone)
        return cls(date_from_timestamp)

    LEAP_DAY_OR_FIRST_OF_MARCH = 60
    """
    The 60th day of the year is either the 1st of March or the leap day (February 29th). 
    Keep track of this number since it will be required in order to determine if a value to ensure that any day post 
    February 28th has the correct day number
    """

    _LEAP_YEAR = 2020
    """
    A numeric leap year - used during datetime conversions to ensure that the correct number of days are accounted for
    """

    def __init__(
        self,
        day: DATE_REPRESENTATION_TYPE = None,
        *,
        month_number: int = None,
        day_of_month_number: int = None
    ):
        """
        Constructor

        :param day: a representation of a date and time or simple representations of a day
        :param month_number: The number of the month to represent
        :param day_of_month_number: The number of the day within the year to represent
        """
        if month_number is not None or day_of_month_number is not None:
            day = day_from_month_and_day(month_number=month_number, day_of_month=day_of_month_number)
        elif is_sequence_type(day):
            day = day_from_sequence(day)

        # If the value is a string that represents a number, convert it to a float -
        # converting it straight to an int might cause problems but converting from a float to an int is fine
        if isinstance(day, str) and value_is_number(day):
            day = float(day)

        # If we have a float we can assume its a day of the year,
        # so go ahead and convert it to the correct type - an int
        if isinstance(day, float):
            day = int(day)

        # The range for valid days are between (0, 366] - check that validity to fail sooner rather than later
        if isinstance(day, int) and (day < 1 or day > 366):
            raise ValueError(f"'{day}' cannot be used as a day number - only days between 1 and 366 are allowable.")

        if isinstance(day, typing.Mapping):
            day = day_from_map(day)

        if isinstance(day, str):
            day = parse_date(day)

        if isinstance(day, datetime_types):
            day = day_from_datetime_type(day)

        self.__day = day

    @property
    def day_number(self) -> int:
        """
        The number of the day of the year; consistent between leap and non-leap years

        Note: This number will not always point to the true day of the year number. All values post-February 28th
        on non-leap years will be increased by 1 to make the value consistent across leap and non-leap years.

        Returns:
            The number of the day of the year; consistent between leap and non-leap years.
        """
        return self.__day

    def to_datetime(self) -> datetime:
        this_year = datetime.now().year
        not_leap_year = datetime.now().year % 4 != 0

        # The day will have been adjusted if this weren't a leap year and was at or after the last day in February,
        # so reverse the adjustment to get the right date
        if not_leap_year and self.__day >= self.LEAP_DAY_OR_FIRST_OF_MARCH:
            day = self.__day - 1
        else:
            day = self.__day

        return datetime.strptime(f"{this_year}-{day}", "%Y-%j")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        this_year = datetime.now().year
        not_leap_year = datetime.now().year % 4 != 0

        # The day will have been adjusted if this weren't a leap year and was at or after the last day in February,
        # so reverse the adjustment to get the right date
        if not_leap_year and self.__day >= self.LEAP_DAY_OR_FIRST_OF_MARCH:
            day = self.__day - 1
        else:
            day = self.__day

        parsed_date = datetime.strptime(f"{this_year}-{day}", "%Y-%j")
        representation = parsed_date.strftime("%B %d")
        return representation

    def __eq__(self, other) -> bool:
        if not isinstance(other, Day):
            other = Day(other)

        return self.__day == other.day_number

    def __ge__(self, other) -> bool:
        if not isinstance(other, Day):
            other = Day(other)

        return self.__day >= other.day_number

    def __le__(self, other) -> bool:
        if not isinstance(other, Day):
            other = Day(other)

        return self.__day <= other.day_number

    def __gt__(self, other) -> bool:
        if not isinstance(other, Day):
            other = Day(other)

        return self.__day > other.day_number

    def __lt__(self, other) -> bool:
        if not isinstance(other, Day):
            other = Day(other)

        return self.__day < other.day_number

    @typing.overload
    def __add__(self, other: timedelta) -> Day:
        ...

    @typing.overload
    def __add__(self, other: typing.Union[datetime_types + (Day,)]) -> timedelta:
        ...

    def __add__(self, other: typing.Union[datetime_types + (Day, timedelta)]) -> typing.Union[Day, timedelta]:
        if not isinstance(other, datetime_types + (Day, timedelta)):
            raise TypeError(f"'{other}: {type(other)}' cannot be added to {self}")

        if isinstance(other, timedelta):
            return Day(self.to_datetime() + other)

        if isinstance(other, Day):
            return abs(other.to_datetime() - self.to_datetime())

        return abs(date_value_to_datetime(other) - self.to_datetime())

    @typing.overload
    def __sub__(self, other: timedelta) -> Day:
        ...

    @typing.overload
    def __sub__(self, other: typing.Union[datetime_types + (Day,)]) -> timedelta:
        ...

    def __sub__(self, other: typing.Union[datetime_types + (Day, timedelta)]) -> typing.Union[Day, timedelta]:
        if not isinstance(other, datetime_types + (Day, timedelta)):
            raise TypeError(f"'{other}: {type(other)}' cannot be subtracted from {self}")

        if isinstance(other, timedelta):
            return Day(self.to_datetime() - other)

        if isinstance(other, Day):
            return self.to_datetime() - other.to_datetime()

        return self.to_datetime() - date_value_to_datetime(other)

    def __hash__(self):
        return hash(self.__day)
