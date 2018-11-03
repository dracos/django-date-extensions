""" This module contains Python types. """

from __future__ import absolute_import

from datetime import date, datetime
from functools import total_ordering

from django.utils import dateformat

from django_date_extensions import settings


FULLY_QUALIFYING_CODES = ('%c', '%j', 'x', '%X')
MONTHS_DAY_CODE = '%d'
MONTH_CODES = ('%b', '%B', '%m')
WEEKS_DAY_CODES = ('%a', '%A', '%w')
YEARS_WEEK_CODES = ('%U', '%W')

FUTURE, PAST = 'future', 'past'


@total_ordering
class ApproximateDate:
    """A date object that accepts 0 for month or day to mean we don't
       know when it is within that month/year."""

    def __init__(self, year=0, month=0, day=0, future=False, past=False):
        if future and past:
            raise ValueError("Can't be both future and past")
        elif future or past:
            if year or month or day:
                raise ValueError("Future or past dates can have no year, month or day")
        elif year and month and day:
            date(year, month, day)
        elif year and month:
            date(year, month, 1)
        elif year and day:
            raise ValueError("You cannot specify just a year and a day")
        elif year:
            date(year, 1, 1)
        else:
            raise ValueError("You must specify a year")

        self.future = future
        self.past = past
        self.year = year
        self.month = month
        self.day = day

    def __repr__(self):
        if self.future or self.past:
            return str(self)
        return "{year:04d}-{month:02d}-{day:02d}".format(year=self.year, month=self.month, day=self.day)

    # TODO this shouldn't depend on Django settings and utils to be usable outside a
    # Django project
    def __str__(self):
        if self.future:
            return FUTURE
        if self.past:
            return PAST
        elif self.year and self.month and self.day:
            return dateformat.format(self, settings.OUTPUT_FORMAT_DAY_MONTH_YEAR)
        elif self.year and self.month:
            return dateformat.format(self, settings.OUTPUT_FORMAT_MONTH_YEAR)
        elif self.year:
            return dateformat.format(self, settings.OUTPUT_FORMAT_YEAR)

    def __eq__(self, other):
        if isinstance(other, (date, datetime)):
            return (self.year, self.month, self.day) ==\
                   (other.year, other.month, other.day)

        if not isinstance(other, ApproximateDate):
            return False

        return (self.year, self.month, self.day, self.future, self.past) ==\
               (other.year, other.month, other.day, other.future, other.past)

    def __lt__(self, other):
        if other is None:
            return False

        if isinstance(other, ApproximateDate):
            if self.future or other.future:
                return not self.future
            if self.past or other.past:
                return not other.past

        return (self.year, self.month, self.day) < (other.year, other.month, other.day)

    # REMOVE
    def __len__(self):
        return len(self.__repr__())

    @classmethod
    def from_string(cls, date_string, format):
        if date_string == PAST:
            return cls(past=True)
        if date_string == FUTURE:
            return cls(future=True)

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


__all__ = (ApproximateDate.__name__,)
