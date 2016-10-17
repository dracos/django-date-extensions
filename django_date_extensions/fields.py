import datetime
import time
import re
from functools import total_ordering

import django
from django.utils.six import with_metaclass
from django.db import models
from django import forms
from django.forms import ValidationError
from django.utils import dateformat

from . import settings
from .widgets import PrettyDateInput

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_date_extensions\.fields\.ApproximateDateField"])
except ImportError:
    pass

PREFIX_RE = re.compile('^(?i)[a-zA-Z]+[.,]?$')


@total_ordering
class ApproximateDate(object):
    """A date object that accepts 0 for month or day to mean we don't
       know when it is within that month/year."""
    def __init__(self, year=0, month=0, day=0, future=False, past=False, prefix=None, string_format=None):
        if string_format:
            if year or month or day or future or past or prefix:
                raise ValueError("String format can have no year, month, day, prefix, future or past")
            elif string_format.lower() not in settings.STRING_FORMATS:
                raise ValueError("Invalid string format `{0}`".format(string_format))
        elif future and past:
            raise ValueError("Can't be both future and past")
        elif future or past:
            if year or month or day or prefix:
                raise ValueError("Future or past dates can have no year, month, day or prefix")
        elif year and month and day:
            datetime.date(year, month, day)
        elif year and month:
            datetime.date(year, month, 1)
        elif year and day:
            raise ValueError("You cannot specify just a year and a day")
        elif year:
            datetime.date(year, 1, 1)
        else:
            raise ValueError("You must specify a year")

        # validate prefix
        if prefix:
            if not settings.ALLOWED_PREFIX:
                raise ValueError("Prefix not allowed")
            elif month or day or string_format:
                raise ValueError("Prefix can only be set with Year only date")
            elif not PREFIX_RE.match(prefix):
                raise ValueError("Prefix value can only contains alphabets and can have maximum of 5 characters")
            elif prefix.lower() not in settings.ALLOWED_PREFIX:
                raise ValueError("Prefix '{0}' not allowed".format(prefix))

        self.future = future
        self.past = past
        self.year = year
        self.month = month
        self.day = day
        self.prefix = prefix
        self.string_format = string_format

    def __repr__(self):
        if self.future or self.past or self.prefix or self.string_format:
            return str(self)
        return "{year:04d}-{month:02d}-{day:02d}".format(year=self.year, month=self.month, day=self.day)

    def __str__(self):
        if self.future:
            return 'future'
        elif self.past:
            return 'past'
        elif self.string_format:
            return self.string_format
        elif self.year and self.month and self.day:
            return dateformat.format(self, settings.OUTPUT_FORMAT_DAY_MONTH_YEAR)
        elif self.year and self.month:
            return dateformat.format(self, settings.OUTPUT_FORMAT_MONTH_YEAR)
        elif self.year and self.prefix:
            return '{0} {1}'.format(self.prefix, dateformat.format(self, settings.OUTPUT_FORMAT_YEAR))
        elif self.year:
            return dateformat.format(self, settings.OUTPUT_FORMAT_YEAR)

    def __eq__(self, other):
        if isinstance(other, (datetime.date, datetime.datetime)):
            return (self.year, self.month, self.day) ==\
                   (other.year, other.month, other.day)

        if not isinstance(other, ApproximateDate):
            return False

        return (self.year, self.month, self.day, self.future, self.past, self.prefix, self.string_format) ==\
               (other.year, other.month, other.day, other.future, other.past, other.prefix, self.string_format)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if other is None:
            return False

        if isinstance(other, ApproximateDate):
            if self.future or other.future:
                return not self.future
            if self.past or other.past:
                return not other.past

        return (self.year, self.month, self.day) < (other.year, other.month, other.day)

    def __len__(self):
        return len(self.__repr__())


ansi_date_re = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')
prefix_date_re = re.compile(r'^([a-zA-Z]+[.,]?) (\d{4})$')
prefix_date_reverse_re = re.compile(r'^(\d{4}) ([a-zA-Z]+[,.]?)$')

if django.VERSION < (1, 8,):
    FIELD_BASE = with_metaclass(models.SubfieldBase, models.CharField)
else:
    FIELD_BASE = models.CharField


class ApproximateDateField(FIELD_BASE):
    """A model field to store ApproximateDate objects in the database
       (as a CharField because MySQLdb intercepts dates from the
       database and forces them to be datetime.date()s."""
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ApproximateDateField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in (None, ''):
            return None
        if isinstance(value, ApproximateDate):
            return value

        if value == 'future':
            return ApproximateDate(future=True)
        if value == 'past':
            return ApproximateDate(past=True)

        prefix = None

        if isinstance(value, (datetime.date, datetime.datetime)):
            year, month, day = value.year, value.month, value.day
        else:
            prefix_date = prefix_date_re.search(value)
            prefix_date_reverse = prefix_date_reverse_re.search(value)
            ansi_date = ansi_date_re.search(value)
            if not prefix_date and not ansi_date and not prefix_date_reverse:
                raise ValidationError('Enter a valid date in YYYY-MM-DD format.')

            if prefix_date:
                prefix, year = value.split(' ')
                year, month, day = map(int, [year, 0, 0])
            elif prefix_date_reverse:
                year, prefix = value.split(' ')
                year, month, day = map(int, [year, 0, 0])
            else:
                year, month, day = map(int, value.split('-'))

        try:
            return ApproximateDate(year, month, day, prefix=prefix)
        except ValueError as e:
            msg = 'Invalid date: %s' % str(e)
            raise ValidationError(msg)

    def from_db_value(self, value, expression=None, connection=None, context=None):
        return self.to_python(value)

    # note - could rename to 'get_prep_value' but would break 1.1 compatability
    def get_db_prep_value(self, value, connection=None, prepared=False):
        if value in (None, ''):
            return ''
        if isinstance(value, ApproximateDate):
            if value.prefix:
                return '{0} {1}'.format(value.year, value.prefix)
            return repr(value)
        if isinstance(value, (datetime.date, datetime.datetime)):
            return dateformat.format(value, "Y-m-d")
        if value == 'future':
            return 'future'
        if value == 'past':
            return 'past'

        if value.lower() in settings.STRING_FORMATS:
            return value

        prefix_date = prefix_date_re.search(value)
        prefix_date_reverse = prefix_date_reverse_re.search(value)
        ansi_date = ansi_date_re.search(value)
        if not prefix_date and not prefix_date_reverse and not ansi_date:
            raise ValidationError('Enter a valid date in YYYY-MM-DD format.')
        if prefix_date_reverse:
            value = '{0} {1}'.format(prefix_date_reverse.group(2), prefix_date_reverse.group(1))
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': ApproximateDateFormField}
        defaults.update(kwargs)
        return super(ApproximateDateField, self).formfield(**defaults)

#    def get_db_prep_lookup(self, lookup_type, value):
#        pass


# TODO: Expand to work more like my PHP strtotime()-using function
class ApproximateDateFormField(forms.fields.Field):
    def __init__(self, max_length=10, *args, **kwargs):
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
        value = re.sub('(?<=\d)(st|nd|rd|th)', '', value.strip())
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

        prefix = None
        match = prefix_date_re.search(value)
        if match:
            prefix = match.group(1)
            value = match.group(2)

        for year_format in settings.YEAR_INPUT_FORMATS:
            try:
                return ApproximateDate(time.strptime(value, year_format)[0], 0, 0, prefix=prefix)
            except ValueError:
                continue

        if value.lower() in settings.STRING_FORMATS:
            return ApproximateDate(string_format=value)

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
        value = re.sub('(?<=\d)(st|nd|rd|th)', '', value.strip())
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
