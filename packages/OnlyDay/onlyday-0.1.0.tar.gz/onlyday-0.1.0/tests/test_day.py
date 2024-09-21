import unittest
import typing
from datetime import datetime
from datetime import timedelta

from onlyday import Day

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


def all_are_equal(sequence: typing.Sequence) -> bool:
    """
    Check to see if all items in the sequence are equivalent

    :param sequence: The collection of values to compare
    :return: True if all items in the sequence are equal
    """
    for comparative_index in range(len(sequence) - 1):
        value_to_check = sequence[comparative_index]
        for comparison_index, value_to_compare in enumerate(sequence[comparative_index + 1:]):
            if value_to_check != value_to_compare:
                print(
                    f"value at index {comparative_index} is not equal to the value at index "
                    f"{comparison_index + comparative_index}: {value_to_check} != {value_to_compare}"
                )
                return False

    return True


class DayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_datetime = datetime(year=2023, month=11, day=24)

        self.date_adjustment = timedelta(days=10)

        self.previous_datetime = self.test_datetime - self.date_adjustment
        self.next_datetime = self.test_datetime + self.date_adjustment

        self.test_day = Day(self.test_datetime)
        self.previous_test_day = Day(self.previous_datetime)
        self.next_test_day = Day(self.next_datetime)

    def test_creation(self):
        # The test day isn't on a leap year and is after February 21st. This has to be shifted to account for that
        # extra day. This is only needed when giving an absolute day number
        absolute_leap_year_day = int(self.test_datetime.strftime("%j")) + 1

        day_from_string = Day(f'{self.test_datetime.year}-{self.test_datetime.month}-{self.test_datetime.day}')
        day_from_short_dict = Day({'day': self.test_datetime.day, 'month': self.test_datetime.month})
        day_from_full_dict = Day({
            "day": self.test_datetime.day,
            "month": str(self.test_datetime.month),
            "year": str(self.test_datetime.year)
        })

        day_from_day_int_dict = Day({"day": absolute_leap_year_day})
        day_from_month_abbreviation_dict = Day(
            {
                "day": self.test_datetime.day,
                "month": self.test_datetime.strftime("%b"),
                "year": 2020
            }
        )
        day_from_month_name_dict = Day({"day": self.test_datetime.day, "month": self.test_datetime.strftime("%B")})

        day_from_int = Day(absolute_leap_year_day)

        day_from_datetime = Day(self.test_datetime)
        day_from_timestamp = Day.from_epoch(1700855463.340028)

        day_from_single_value_sequence = Day([329.4])
        day_from_two_value_sequence = Day([11, 24])
        day_from_three_value_sequence = Day([2023, 11, 24])

        if _HAS_NUMPY:
            day_from_datetime64 = Day(numpy.datetime64(self.test_datetime))
        else:
            day_from_datetime64 = None

        if _HAS_PANDAS:
            day_from_pandas_timestamp = Day(pandas.Timestamp(self.test_datetime))
        else:
            day_from_pandas_timestamp = None

        all_days = [
            day_from_string,
            day_from_short_dict,
            day_from_full_dict,
            day_from_day_int_dict,
            day_from_month_abbreviation_dict,
            day_from_month_name_dict,
            day_from_int,
            day_from_datetime,
            day_from_timestamp,
            day_from_single_value_sequence,
            day_from_two_value_sequence,
            day_from_three_value_sequence
        ]

        if day_from_datetime64 is not None:
            all_days.append(day_from_datetime64)

        if day_from_pandas_timestamp:
            all_days.append(day_from_pandas_timestamp)

        self.assertTrue(all_are_equal(all_days))

        self.assertTrue(all([day.day_number == 329 for day in all_days]))

    def test_comparisons(self):
        self.assertEqual(self.test_day, self.test_day)
        self.assertEqual(self.test_day, self.test_datetime)

        self.assertGreater(self.test_day, self.previous_test_day)
        self.assertGreater(self.test_day, self.previous_datetime)

        self.assertGreaterEqual(self.test_day, self.previous_test_day)
        self.assertGreaterEqual(self.test_day, self.previous_datetime)

        self.assertGreaterEqual(self.test_day, self.test_day)
        self.assertGreaterEqual(self.test_day, self.test_datetime)

        self.assertLess(self.test_day, self.next_test_day)
        self.assertLess(self.test_day, self.next_datetime)

        self.assertLessEqual(self.test_day, self.next_test_day)
        self.assertLessEqual(self.test_day, self.next_datetime)

        self.assertLessEqual(self.test_day, self.test_day)
        self.assertLessEqual(self.test_day, self.test_datetime)

        self.assertGreater(self.next_test_day, self.previous_test_day)
        self.assertGreater(self.next_test_day, self.previous_datetime)

        self.assertGreaterEqual(self.next_test_day, self.previous_test_day)
        self.assertGreaterEqual(self.next_test_day, self.previous_datetime)

        self.assertLess(self.previous_test_day, self.next_test_day)
        self.assertLess(self.previous_test_day, self.next_datetime)

        self.assertLessEqual(self.previous_test_day, self.next_test_day)
        self.assertLessEqual(self.previous_test_day, self.next_datetime)

    def test_operations(self):
        self.assertEqual(self.test_day, self.test_day - timedelta(0))
        self.assertEqual(self.test_day, self.test_day + timedelta(0))
        self.assertEqual(self.test_day + self.date_adjustment, self.next_test_day)
        self.assertEqual(self.test_day + self.date_adjustment, self.next_datetime)
        self.assertEqual(self.test_day - self.date_adjustment, self.previous_test_day)
        self.assertEqual(self.test_day - self.date_adjustment, self.previous_test_day)
        self.assertEqual(self.test_day - self.next_test_day, -self.date_adjustment)
        self.assertEqual(self.test_day + self.next_test_day, self.date_adjustment)
        self.assertEqual(self.test_day - self.previous_test_day, self.date_adjustment)
        self.assertEqual(self.test_day + self.previous_test_day, self.date_adjustment)
        self.assertEqual(self.previous_test_day + self.test_day, self.date_adjustment)
        self.assertEqual(self.previous_test_day - self.test_day, -self.date_adjustment)
        self.assertEqual(self.next_test_day + self.test_day, self.date_adjustment)
        self.assertEqual(self.next_test_day - self.test_day, self.date_adjustment)
        self.assertEqual(self.next_test_day - self.previous_test_day, 2 * self.date_adjustment)
        self.assertEqual(self.next_test_day + self.previous_test_day, 2 * self.date_adjustment)
        self.assertEqual(self.previous_test_day + self.next_test_day, 2 * self.date_adjustment)
        self.assertEqual(self.previous_test_day - self.next_test_day, -2 * self.date_adjustment)


if __name__ == '__main__':
    unittest.main()
