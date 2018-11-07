from __future__ import absolute_import

from datetime import date, datetime

from django.db import models

from django_date_extensions.forms import ApproximateDateFormField
from django_date_extensions.types import ApproximateDate
from django_date_extensions.utils import (
    unprecise_date_as_signed_int,
    unprecise_date_from_signed_int,
)


FORMAT_STRINGS = ("%Y", "%Y-%m", "%Y-%m-%d")


class ApproximateDateField(models.IntegerField):
    """ A model field to store ApproximateDate objects in the database. """

    description = "An approximate date"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # from db
    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return unprecise_date_from_signed_int(value)

    # from forms and serialized data
    def to_python(self, value):
        if value in ("", None):
            return None
        if isinstance(value, ApproximateDate):
            return value
        return ApproximateDate.from_string(value, FORMAT_STRINGS[value.count("-")])

    # to db
    def get_prep_value(self, value):
        if isinstance(value, str):
            # ensure it is a valid value
            value = self.to_python(value)

        if value is None:
            return None

        elif isinstance(value, datetime):
            value = ApproximateDate.from_datetime(value)

        elif isinstance(value, date):
            value = ApproximateDate.from_date(value)

        return unprecise_date_as_signed_int(value)

    # to serialized_data
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        if value is None:
            return ""
        assert isinstance(value, ApproximateDate)
        return str(value)

    def formfield(self, **kwargs):
        kwargs.setdefault("form_class", ApproximateDateFormField)
        return super().formfield(**kwargs)


__all__ = (ApproximateDateField.__name__,)
