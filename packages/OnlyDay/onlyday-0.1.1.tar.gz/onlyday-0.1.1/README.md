# OnlyDay
Python library that introduces a Day datatype that is universal across every year.

A day representing November 3rd will represent the same year-less day across every year. A `Day` object representing
November 3rd is valid for both 2020-11-03 and 2022-11-03.


```python
from datetime import datetime

from onlyday import Day

first_date = datetime(year=2022, month=11, day=3)

first_day = Day(first_date)
second_day = Day("1999-11-03")

assert first_day == second_day
assert first_day == first_date
assert second_day == first_date
```

[Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/) are both supported but aren't necessary.