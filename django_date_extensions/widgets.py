from __future__ import absolute_import

from django.forms.widgets import NumberInput, MultiWidget
from django.utils.translation import gettext_lazy as _

from django_date_extensions.types import ApproximateDate


class NumbersInput(MultiWidget):
    is_required = False
    widgets = (
        NumberInput({'min': 0, 'style': 'width: 3.5em;', 'placeholder': _('YYYY')}),
        NumberInput({'min': 0, 'style': 'width: 2.5em;', 'max': 12, 'placeholder': _(
            'MM')}),
        NumberInput({'min': 0, 'style': 'width: 2.5em;', 'max': 31, 'placeholder': _(
            'DD')}),
    )

    def __init__(self, **kwargs):
        super().__init__(self.widgets, **kwargs)

    def decompress(self, value):
        if value is None:
            return '', '', ''
        if isinstance(value, ApproximateDate):
            result = (value.year, value.month or '', value.day or '')
            return [str(x) for x in result]

        raise NotImplementedError

    def get_context(self, *args):
        context = super().get_context(*args)

        # FIXME workaround for https://code.djangoproject.com/ticket/29205
        for subwidget in context['widget']['subwidgets']:
            subwidget['attrs']['required'] = False

        return context


__all__ = (NumbersInput.__name__,)
