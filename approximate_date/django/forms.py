from __future__ import absolute_import

import re
import time

from django.core.exceptions import ValidationError
from django.forms.fields import Field, IntegerField, MultiValueField

from approximate_date.django import settings
from approximate_date.django.widgets import NumbersInput
from approximate_date.types import VagueDate


# TODO provide localized error messages


class VagueDateNumbersField(MultiValueField):
    """ This field's widget renders the inputs as number widgets. """
    widget = NumbersInput

    def __init__(self, **kwargs):
        fields = (
            IntegerField(required=False),
            IntegerField(required=False, min_value=0, max_value=12),
            IntegerField(required=False, min_value=0, max_value=31)
        )
        super().__init__(fields, **{**kwargs, 'require_all_fields': False})

    def compress(self, data_list):
        if not data_list or data_list[0] is None:
            return None

        try:
            return VagueDate(
                year=data_list[0] or 0,
                month=data_list[1] or 0,
                day=data_list[2] or 0
            )
        except ValueError as e:
            raise ValidationError(e)


# TODO use VagueDate.from_string
class VagueDateTextField(Field):
    def clean(self, value):
        super(VagueDateTextField, self).clean(value)
        if value in (None, ''):
            return None
        if isinstance(value, VagueDate):
            return value
        value = re.sub(r'(?<=\d)(st|nd|rd|th)', '', value.strip())
        for date_format in settings.DATE_INPUT_FORMATS:
            try:
                return VagueDate(*time.strptime(value, date_format)[:3])
            except ValueError:
                continue
        for month_format in settings.MONTH_INPUT_FORMATS:
            try:
                match = time.strptime(value, month_format)
                return VagueDate(match[0], match[1], 0)
            except ValueError:
                continue
        for year_format in settings.YEAR_INPUT_FORMATS:
            try:
                return VagueDate(time.strptime(value, year_format)[0], 0, 0)
            except ValueError:
                continue
        raise ValidationError('Please enter a valid date.')


__all__ = (VagueDateNumbersField.__name__, VagueDateTextField.__name__)
