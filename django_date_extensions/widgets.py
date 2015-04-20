from datetime import date
from django.conf import settings

from django.utils import dateformat
from django.forms import widgets

OUTPUT_FORMAT_DAY_MONTH_YEAR = getattr(settings, 'DATE_EXTENSIONS_OUTPUT_FORMAT_DAY_MONTH_YEAR', "jS F Y")


class PrettyDateInput(widgets.Input):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif isinstance(value, date):
            value = dateformat.format(value, OUTPUT_FORMAT_DAY_MONTH_YEAR)
        return super(PrettyDateInput, self).render(name, value, attrs)

