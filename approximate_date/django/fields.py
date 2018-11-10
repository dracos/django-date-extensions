from datetime import date, datetime

from django.db import models

from approximate_date.types import VagueDate
from approximate_date.django.forms import VagueDateNumbersField
from approximate_date.utils import vague_date_as_signed_int, vague_date_from_signed_int


FORMAT_STRINGS = ("%Y", "%Y-%m", "%Y-%m-%d")


class VagueDateField(models.IntegerField):
    """ A model field to store VagueDate objects in the database. """

    description = "An imprecise date."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # from db
    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return vague_date_from_signed_int(value)

    # from forms and serialized data
    def to_python(self, value):
        if value in ("", None):
            return None
        if isinstance(value, VagueDate):
            return value
        return VagueDate.from_string(value, FORMAT_STRINGS[value.count("-")])

    # to db
    def get_prep_value(self, value):
        if isinstance(value, str):
            # ensure it is a valid value
            value = self.to_python(value)

        if value is None:
            return None

        elif isinstance(value, datetime):
            value = VagueDate.from_datetime(value)

        elif isinstance(value, date):
            value = VagueDate.from_date(value)

        return vague_date_as_signed_int(value)

    # to serialized_data
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        if value is None:
            return ""
        assert isinstance(value, VagueDate)
        return str(value)

    def formfield(self, **kwargs):
        kwargs.setdefault("form_class", VagueDateNumbersField)
        return super().formfield(**kwargs)


__all__ = (VagueDateField.__name__,)
