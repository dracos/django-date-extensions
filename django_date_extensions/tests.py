from datetime import date, datetime
import unittest

from django.db import models
from django import forms

from . import settings
from .fields import ApproximateDate, ApproximateDateField, ApproximateDateFormField

settings.ALLOWED_PREFIX = ['about', 'about,', 'about.']


class ApproxDateModel(models.Model):
    start = ApproximateDateField()

    def __unicode__(self):
        return u'%s' % str(self.start)


class ApproxDateForm(forms.Form):
    start = ApproximateDateFormField()


class PastAndFuture(unittest.TestCase):

    def test_setting_both(self):
        self.assertRaises(ValueError, ApproximateDate, past=True, future=True)

    def test_setting_with_dates(self):
        self.assertRaises(ValueError, ApproximateDate, future=True, year=2000)
        self.assertRaises(ValueError, ApproximateDate, past=True,   year=2000)

    def test_stringification(self):

        self.assertEqual(str(ApproximateDate(future=True)), 'future')
        self.assertEqual(str(ApproximateDate(past=True)), 'past')

        self.assertEqual(repr(ApproximateDate(future=True)), 'future')
        self.assertEqual(repr(ApproximateDate(past=True)), 'past')


class CompareDates(unittest.TestCase):

    def test_compare(self):

        past = ApproximateDate(past=True)
        past_too = ApproximateDate(past=True)
        y_past = ApproximateDate(year=2000)
        y_future = ApproximateDate(year=2100)
        future = ApproximateDate(future=True)
        future_too = ApproximateDate(future=True)
        prefix_dt = ApproximateDate(prefix='about', year=2010)

        # check that we can be compared to None, '' and u''
        for bad_val in ('', u'', None):
            self.assertFalse(y_past in (bad_val,))
            self.assertFalse(y_past == bad_val)
            self.assertTrue(y_past != bad_val)

        # sanity check
        self.assertTrue(y_past == y_past)
        self.assertTrue(y_future == y_future)
        self.assertTrue(prefix_dt == prefix_dt)

        self.assertFalse(y_past != y_past)
        self.assertFalse(y_future != y_future)
        self.assertFalse(prefix_dt != prefix_dt)

        self.assertTrue(y_past != y_future)
        self.assertTrue(y_future != y_past)

        self.assertTrue(y_future > y_past)
        self.assertTrue(y_future >= y_past)
        self.assertFalse(y_past > y_future)
        self.assertFalse(y_past >= y_future)
        self.assertFalse(prefix_dt > prefix_dt)
        self.assertTrue(prefix_dt >= prefix_dt)

        self.assertTrue(y_past < y_future)
        self.assertTrue(y_past <= y_future)
        self.assertFalse(y_future < y_past)
        self.assertFalse(y_future <= y_past)
        self.assertFalse(prefix_dt < prefix_dt)
        self.assertTrue(prefix_dt <= prefix_dt)

        # Future dates are always greater
        self.assertTrue(y_past < future)
        self.assertTrue(y_past <= future)
        self.assertTrue(y_past != future)
        self.assertTrue(y_future < future)
        self.assertTrue(y_future <= future)
        self.assertTrue(y_future != future)

        self.assertTrue(future > y_past)
        self.assertTrue(future >= y_past)
        self.assertTrue(future != y_past)
        self.assertTrue(future > y_future)
        self.assertTrue(future >= y_future)
        self.assertTrue(future != y_future)

        # Past dates are always lesser
        self.assertTrue(y_past > past)
        self.assertTrue(y_past >= past)
        self.assertTrue(y_past != past)
        self.assertTrue(y_future > past)
        self.assertTrue(y_future >= past)
        self.assertTrue(y_future != past)

        self.assertTrue(past < y_past)
        self.assertTrue(past <= y_past)
        self.assertTrue(past != y_past)
        self.assertTrue(past < y_future)
        self.assertTrue(past <= y_future)
        self.assertTrue(past != y_future)

        # Past and future comparisons
        self.assertTrue(past < future)
        self.assertTrue(past <= future)
        self.assertTrue(past != future)

        self.assertTrue(future > past)
        self.assertTrue(future >= past)
        self.assertTrue(future != past)

        # Future and past dates are equal to themselves (so that sorting is sane)
        self.assertFalse(future < future)
        self.assertTrue(future <= future)
        self.assertTrue(future == future)
        self.assertTrue(future >= future)
        self.assertFalse(future > future)
        self.assertTrue(future == future_too)
        self.assertFalse(future != future_too)

        self.assertFalse(past < past)
        self.assertTrue(past <= past)
        self.assertTrue(past == past)
        self.assertTrue(past >= past)
        self.assertFalse(past > past)
        self.assertTrue(past == past_too)
        self.assertFalse(past != past_too)

    def test_compare_date(self):
        """
        You can compare Aproximate date objects to regular date ones.
        """
        self.assertEqual(ApproximateDate(2008, 9, 3), date(2008, 9, 3))
        self.assertTrue(ApproximateDate(2008, 9, 3) < date(2009, 9, 3))
        self.assertTrue(ApproximateDate(2007) < date(2007, 9, 3))


class Lengths(unittest.TestCase):
    known_lengths = (
        ({'year': 1999}, 10),
        ({'year': 1999, 'month': 1}, 10),
        ({'year': 1999, 'month': 1, 'day': 1}, 10),
        ({'future': True},                      6),
        ({'past': True},                        4),
    )

    def test_length(self):
        for kwargs, length in self.known_lengths:
            approx = ApproximateDate(**kwargs)
            self.assertEqual(len(approx), length)


class ApproxDateFiltering(unittest.TestCase):

    def setUp(self):
        for year in [2000, 2001, 2002, 2003, 2004]:
            if year == 2004:
                prefix = 'about'
            else:
                prefix = None
            ApproxDateModel.objects.create(start=ApproximateDate(year=year, prefix=prefix))

    def test_filtering_with_python_date(self):
        qs = ApproxDateModel.objects.filter(start__gt=date.today())
        # force evaluate queryset
        list(qs)

    def test_filtering_with_python_datetime(self):
        qs = ApproxDateModel.objects.filter(start__gt=datetime.now())
        # force evaluate queryset
        list(qs)

    def test_filtering_with_prefix_date(self):
        qs = ApproxDateModel.objects.filter(start=ApproximateDate(year=2004, prefix='about'))
        self.assertEqual(qs.count(), 1)


class PrefixDates(unittest.TestCase):
    def test_valid(self):
        ApproximateDate(year=2010, prefix='about')
        ApproximateDate(year=2010, prefix='about.')
        ApproximateDate(year=2010, prefix='about,')

    def test_invalid(self):
        self.assertRaises(ValueError, ApproximateDate, year=2015, prefix='what')
        self.assertRaises(ValueError, ApproximateDate, year=2015, prefix='about?')

    def test_stringification(self):
        self.assertEqual(str(ApproximateDate(year=2010, prefix='about')), 'about 2010')
        self.assertEqual(str(ApproximateDate(year=2010)), '2010')

    def test_with_year_month_day(self):
        self.assertRaises(ValueError, ApproximateDate, prefix='about', year=2015, month=12, day=1)

    def test_with_year_month(self):
        self.assertRaises(ValueError, ApproximateDate, prefix='about', year=2015, month=12)

    def test_with_year(self):
        self.assertRaises(ValueError, ApproximateDate, prefix='about', year=2015, month=12)

    def test_db(self):
        ApproxDateModel.objects.create(start=ApproximateDate(year=2010, prefix='about'))
        ApproxDateModel.objects.create(start=ApproximateDate(year=2010))
        ApproxDateModel.objects.create(start=ApproximateDate(year=2010, month=12, day=1))

    def test_date_with_prefix_form(self):
        form = ApproxDateForm({'start': 'about 2015'})
        self.assertTrue(form.is_valid())
        form = ApproxDateForm({'start': '2015'})
        self.assertTrue(form.is_valid())

    def test_ordering(self):
        ApproxDateModel.objects.all().delete()
        years = [2015, 2006, 2013, 2004, 2003, 1989]
        for year in years:
            ApproxDateModel.objects.create(start=ApproximateDate(year=year, prefix='about'))
        self.assertEqual(
            sorted(years),
            [o.start.year for o in ApproxDateModel.objects.all().order_by('start')]
        )
        self.assertEqual(
            sorted(years, reverse=True),
            [o.start.year for o in ApproxDateModel.objects.all().order_by('-start')]
        )


if __name__ == "__main__":
    unittest.main()
