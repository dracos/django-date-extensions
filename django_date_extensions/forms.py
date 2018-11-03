from __future__ import absolute_import

import datetime
import re
import time

from django.core.exceptions import ValidationError
from django.utils import dateformat

from django_date_extensions import settings
from django_date_extensions.types import ApproximateDate




# TODO use ApproximateDate.from_string
class ApproximateDateFormField(Field):
    def __init__(self, max_length=10, empty_value='', *args, **kwargs):
        super(ApproximateDateFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(ApproximateDateFormField, self).clean(value)
        if value in (None, ''):
            return None
        if value == 'future':
            return ApproximateDate(future=True)
        if value == 'past':
            return ApproximateDate(past=True)
        if isinstance(value, ApproximateDate):
            return value
        value = re.sub(r'(?<=\d)(st|nd|rd|th)', '', value.strip())
        for date_format in settings.DATE_INPUT_FORMATS:
            try:
                return ApproximateDate(*time.strptime(value, date_format)[:3])
            except ValueError:
                continue
        for month_format in settings.MONTH_INPUT_FORMATS:
            try:
                match = time.strptime(value, month_format)
                return ApproximateDate(match[0], match[1], 0)
            except ValueError:
                continue
        for year_format in settings.YEAR_INPUT_FORMATS:
            try:
                return ApproximateDate(time.strptime(value, year_format)[0], 0, 0)
            except ValueError:
                continue
        raise ValidationError('Please enter a valid date.')


class PrettyDateField(Field):
    """ PrettyDateField - same as DateField but accepts slightly more input, like
        :class:`ApproximateDateFormField` above. If initialised with future=True, it
        will assume a date without year means the current year (or the next year if the
        day is before the current date). If future=False, it does the same but in the
        past. """

    def __init__(self, future=None, *args, **kwargs):
        self.future = future
        super().__init__(*args, **kwargs)

    def clean(self, value):
        """
        Validates that the input can be converted to a date. Returns a Python
        datetime.date object.
        """
        super().clean(value)
        if value in (None, ''):
            return None
        if value == 'future':
            return ApproximateDate(future=True)
        if value == 'past':
            return ApproximateDate(past=True)
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value
        value = re.sub(r'(?<=\d)(st|nd|rd|th)', '', value.strip())
        for date_input_format in settings.DATE_INPUT_FORMATS:
            try:
                return datetime.date(*time.strptime(value, date_input_format)[:3])
            except ValueError:
                continue

        if self.future is None:
            raise ValidationError('Please enter a valid date.')

        # Allow year to be omitted. Do the sensible thing, either past or future.
        for day_month_input_format in settings.DAY_MONTH_INPUT_FORMATS:
            try:
                t = time.strptime(value, day_month_input_format)
                month, day, yday = t[1], t[2], t[7]
                year = datetime.date.today().year
                if self.future and yday < int(datetime.date.today().strftime('%j')):
                    year += 1
                if not self.future and yday > int(datetime.date.today().strftime('%j')):
                    year -= 1
                return datetime.date(year, month, day)
            except ValueError:
                continue

        raise ValidationError('Please enter a valid date.')

    def prepare_value(self, value):
        if value is None:
            return ''
        elif isinstance(value, str):
            return value
        elif isinstance(value, datetime.date):
            return dateformat.format(value, settings.OUTPUT_FORMAT_DAY_MONTH_YEAR)
        else:
            raise TypeError('Unexpected type: {}'.format(value.__class__))


__all__ = (ApproximateDateFormField.__name__, PrettyDateField.__name__)
