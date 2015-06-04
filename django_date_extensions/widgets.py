from datetime import date

from django.utils import dateformat
from django.forms import widgets

from . import settings


class PrettyDateInput(widgets.Input):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif isinstance(value, date):
            value = dateformat.format(value, settings.OUTPUT_FORMAT_DAY_MONTH_YEAR)
        return super(PrettyDateInput, self).render(name, value, attrs)
