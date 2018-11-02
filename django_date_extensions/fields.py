from __future__ import absolute_import

import datetime
import re

from django.db import models
from django.forms import ValidationError
from django.utils import dateformat

from django_date_extensions.forms import ApproximateDateFormField
from django_date_extensions.types import ApproximateDate


ansi_date_re = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')


class ApproximateDateField(models.CharField):
    """A model field to store ApproximateDate objects in the database
       (as a CharField because MySQLdb intercepts dates from the
       database and forces them to be datetime.date()s."""

    description = "An approximate date"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ApproximateDateField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ApproximateDateField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def to_python(self, value):
        if isinstance(value, ApproximateDate):
            return value

        return self.from_db_value(value)

    def from_db_value(self, value, expression=None, connection=None, context=None):
        if value in (None, ''):
            return ''

        if value == 'future':
            return ApproximateDate(future=True)
        if value == 'past':
            return ApproximateDate(past=True)

        if not ansi_date_re.search(value):
            raise ValidationError('Enter a valid date in YYYY-MM-DD format.')

        year, month, day = map(int, value.split('-'))
        try:
            return ApproximateDate(year, month, day)
        except ValueError as e:
            msg = 'Invalid date: %s' % str(e)
            raise ValidationError(msg)

    def get_prep_value(self, value):
        if value in (None, ''):
            return ''
        if isinstance(value, ApproximateDate):
            return repr(value)
        if isinstance(value, datetime.date):
            return dateformat.format(value, "Y-m-d")
        if value == 'future':
            return 'future'
        if value == 'past':
            return 'past'
        if not ansi_date_re.search(value):
            raise ValidationError('Enter a valid date in YYYY-MM-DD format.')
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', ApproximateDateFormField)
        return super(ApproximateDateField, self).formfield(**kwargs)


__all__ = (ApproximateDateField.__name__)
