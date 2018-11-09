""" This module contains Python types. """

from __future__ import absolute_import

from datetime import date, datetime
from functools import total_ordering


FULLY_QUALIFYING_CODES = ('%c', '%j', 'x', '%X')
MONTHS_DAY_CODE = '%d'
MONTH_CODES = ('%b', '%B', '%m')
WEEKS_DAY_CODES = ('%a', '%A', '%w')
YEARS_WEEK_CODES = ('%U', '%W')


class ApproximateDate:
    def __init__(self, *constraints):
        self.constraints = set(constraints)

    def possible_dates(self):
        raise NotImplementedError



@total_ordering
class VagueDate:
    """A date object that accepts 0 for month or day to mean we don't
       know when it is within that month/year."""

    def __init__(self, year=0, month=0, day=0):
        # TODO support negative years
        if year and month and day:
            date(year, month, day)
        elif year and month:
            date(year, month, 1)
        elif year and day:
            raise ValueError("You cannot specify just a year and a day")
        elif year:
            date(year, 1, 1)
        else:
            raise ValueError("You must specify a year")

        self.year = year
        self.month = month
        self.day = day

    def __format__(self, format_spec):
        return self._date_dummy.__format__(format_spec)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, str(self))

    def __str__(self):
        format = '%04Y'
        if self.month:
            format += '-%02m'
            if self.day:
                format += '-%02d'
        return self.__format__(format)

    def __eq__(self, other):
        if isinstance(other, (date, datetime)):
            return (self.year, self.month, self.day) ==\
                   (other.year, other.month, other.day)

        if not isinstance(other, VagueDate):
            return False

        return (self.year, self.month, self.day) ==\
               (other.year, other.month, other.day)

    def __lt__(self, other):
        if other is None:
            return False

        return (self.year, self.month, self.day) < (other.year, other.month, other.day)

    @property
    def _date_dummy(self):
        return date(year=self.year, month=max(1, self.month), day=max(1, self.day))

    @classmethod
    def from_date(cls, value):
        return cls(year=value.year, month=value.month, day=value.day)

    @classmethod
    def from_datetime(cls, value):
        return cls.from_date(value.date())

    @classmethod
    def from_string(cls, date_string, format):
        relevant_attributes = ['year']

        if any(x in format for x in FULLY_QUALIFYING_CODES) or \
                (any(x in format for x in YEARS_WEEK_CODES) and
                 any(x in format for x in WEEKS_DAY_CODES)):
            relevant_attributes.extend(('month', 'day'))
        else:
            if any(x in format for x in MONTH_CODES):
                relevant_attributes.append('month')
                if MONTHS_DAY_CODE in format:
                    relevant_attributes.append('day')

        parsed_date = datetime.strptime(date_string, format).date()
        return cls(**{k: getattr(parsed_date, k) for k in relevant_attributes})

    @property
    def is_precise(self):
        return bool(self.day)


__all__ = (VagueDate.__name__,)
