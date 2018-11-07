# TODO cythonize

from django_date_extensions.types import ApproximateDate


DAY_OFFSET = 0
DAY_WIDTH = 5
DAY_MASK = 2 ** DAY_WIDTH - 1
MONTH_OFFSET = DAY_OFFSET + DAY_WIDTH
MONTH_WIDTH = 4
MONTH_MASK = 2 ** MONTH_WIDTH - 1
YEAR_OFFSET = MONTH_OFFSET + MONTH_WIDTH
YEAR_WIDTH = 31 - MONTH_WIDTH - DAY_WIDTH

MAX_YEAR_VALUE = 2 ** YEAR_WIDTH - 1
PAST = -(2 ** 31)
FUTURE = 2 ** 31 - 1


def unprecise_date_as_signed_int(value):
    assert isinstance(value, ApproximateDate), type(value)

    if value.past:
        return PAST
    if value.future:
        return FUTURE

    abs_year = abs(value.year)

    if abs_year > MAX_YEAR_VALUE:
        raise ValueError("Year {} can't be stored in the database.")

    result = (
        abs_year << YEAR_OFFSET | value.month << MONTH_OFFSET | value.day << DAY_OFFSET
    )
    if value.year < 0:
        result *= -1

    assert PAST < result < FUTURE
    return result


def unprecise_date_from_signed_int(value):
    assert isinstance(value, int)

    if value == FUTURE:
        return ApproximateDate(future=True)
    if value == PAST:
        return ApproximateDate(past=True)

    abs_value = abs(value)
    day = abs_value & DAY_MASK
    abs_value >>= DAY_WIDTH
    month = abs_value & MONTH_MASK
    abs_value >>= MONTH_WIDTH
    year = abs_value * (value // abs_value)

    return ApproximateDate(year=year, month=month, day=day)
