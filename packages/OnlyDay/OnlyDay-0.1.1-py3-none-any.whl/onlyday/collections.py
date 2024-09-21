"""
Collections used to tie datetime types to Day values
"""
from __future__ import annotations

import typing

from .day import Day
from .day import DATE_REPRESENTATION_TYPE

VT = typing.TypeVar('VT')
"""A generic value type"""


class DayDict(dict[Day, VT], typing.Generic[VT]):
    """
    A dictionary that keys on day

    The keys can be any type that can be converted into a Day, so if data is stored by key,
    it may still be accessed via a datetime or pandas Timestamp

    You can't necessarily use a `dict` proper unless you will only ever access by `Day` object. The hash of a Day
    object and a datetime, for instance, won't match, so you won't be able to access a `Day` keyed `dict` and expect
    to get the proper value. Through the use of a `DayDict` though, you can get the correct value for a particular day
    regardless of the type of date you give it. If the `DayDict` contains values that are valid for April 1st,
    you can get the correct value when querying with `datetime(2023, 4, 1, 13, 0, 1)` and
    `datetime(2023, 4, 1, 8, 17)`.
    """
    def __init__(
        self,
        *args: typing.Tuple[typing.Union[DATE_REPRESENTATION_TYPE, Day], VT],
        mapping: typing.Mapping[typing.Union[DATE_REPRESENTATION_TYPE, Day], VT] = None,
    ) -> None:
        super().__init__()

        for raw_key, value in args:
            self[raw_key] = value

        for raw_key, value in (mapping or {}).items():
            self[raw_key] = value

    def __setitem__(self, raw_key: typing.Union[DATE_REPRESENTATION_TYPE, Day], value: VT) -> None:
        try:
            if isinstance(raw_key, Day):
                key = raw_key
            else:
                key = Day(raw_key)
        except Exception as exception:
            raise TypeError(f"{raw_key} cannot be turned into a Day object") from exception

        super().__setitem__(key, value)

    def __getitem__(self, raw_key: typing.Union[DATE_REPRESENTATION_TYPE, Day]) -> VT:
        try:
            if isinstance(raw_key, Day):
                key = raw_key
            else:
                key = Day(raw_key)
        except Exception as exception:
            raise TypeError(f"{raw_key} cannot be turned into a Day object") from exception

        return super().__getitem__(key)
