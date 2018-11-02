from __future__ import absolute_import

import datetime
import re
import time

from django import forms

from django_date_extensions import settings
from django_date_extensions.types import ApproximateDate
from django_date_extensions.widgets import PrettyDateInput


ValidationError = forms.ValidationError


# TODO: Expand to work more like my PHP strtotime()-using function
class ApproximateDateFormField(forms.fields.Field):
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


# PrettyDateField - same as DateField but accepts slightly more input,
# like ApproximateDateFormField above. If initialised with future=True,
# it will assume a date without year means the current year (or the next
# year if the day is before the current date). If future=False, it does
# the same but in the past.
class PrettyDateField(forms.fields.Field):
    widget = PrettyDateInput

    def __init__(self, future=None, *args, **kwargs):
        self.future = future
        super(PrettyDateField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """
        Validates that the input can be converted to a date. Returns a Python
        datetime.date object.
        """
        super(PrettyDateField, self).clean(value)
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


__all__ = (ApproximateDateFormField.__name__, PrettyDateField.__name__)
