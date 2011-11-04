from datetime import date
from django.utils import dateformat
from django.forms import widgets

class PrettyDateInput(widgets.Input):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif isinstance(value, date):
            value = dateformat.format(value, "jS F Y")
        return super(PrettyDateInput, self).render(name, value, attrs)

