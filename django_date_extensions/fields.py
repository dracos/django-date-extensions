from __future__ import absolute_import

from datetime import date, datetime

from django.db import models

from django_date_extensions.forms import ApproximateDateFormField
from django_date_extensions.types import ApproximateDate


FORMAT_STRINGS = ('%Y', '%Y-%m', '%Y-%m-%d')


class ApproximateDateField(models.CharField):
    """A model field to store ApproximateDate objects in the database
       (as a CharField because MySQLdb intercepts dates from the
       database and forces them to be datetime.date()s."""

    description = "An approximate date"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    # from db
    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return self.to_python(value)

    # from forms and serialized data
    def to_python(self, value):
        if value in ('', None):
            return None
        if isinstance(value, ApproximateDate):
            return value
        return ApproximateDate.from_string(value, FORMAT_STRINGS[value.count('-')])

    # to db
    def get_prep_value(self, value):
        if isinstance(value, str):
            # ensure it is a valid value
            value = self.to_python(value)

        if value is None:
            return ''

        elif isinstance(value, datetime):
            value = ApproximateDate.from_datetime(value)

        elif isinstance(value, date):
            value = ApproximateDate.from_date(value)

        return str(value)

    # to serialized_data
    def value_to_string(self, obj):
        return self.get_prep_value(self.value_from_object(obj))

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', ApproximateDateFormField)
        return super(ApproximateDateField, self).formfield(**kwargs)


__all__ = (ApproximateDateField.__name__,)
