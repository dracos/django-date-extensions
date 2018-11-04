from __future__ import absolute_import

import os
import unittest
from datetime import date, datetime

from django import forms
from django import VERSION as DJANGO_VERSION
from django.db import models

from django_date_extensions.fields import ApproximateDateField
from django_date_extensions.types import ApproximateDate


os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'


class ApproxDateModel(models.Model):
    start = ApproximateDateField()
    can_be_null = ApproximateDateField(null=True)

    def __unicode__(self):
        return u'%s' % str(self.start)


class ApproxDateForm(forms.ModelForm):
    class Meta:
        model = ApproxDateModel
        fields = ('start', 'can_be_null')


class PastAndFuture(unittest.TestCase):

    def test_setting_both(self):
        self.assertRaises(ValueError, ApproximateDate, past=True, future=True)

    def test_setting_with_dates(self):
        self.assertRaises(ValueError, ApproximateDate, future=True, year=2000)
        self.assertRaises(ValueError, ApproximateDate, past=True,   year=2000)


class CompareDates(unittest.TestCase):

    def test_compare(self):

        past = ApproximateDate(past=True)
        past_too = ApproximateDate(past=True)
        y_past = ApproximateDate(year=2000)
        y_future = ApproximateDate(year=2100)
        future = ApproximateDate(future=True)
        future_too = ApproximateDate(future=True)

        # check that we can be compared to None, '' and u''
        for bad_val in ('', u'', None):
            self.assertFalse(y_past in (bad_val,))
            self.assertFalse(y_past == bad_val)
            self.assertTrue(y_past != bad_val)

        # sanity check
        self.assertTrue(y_past == y_past)
        self.assertTrue(y_future == y_future)

        self.assertFalse(y_past != y_past)
        self.assertFalse(y_future != y_future)

        self.assertTrue(y_past != y_future)
        self.assertTrue(y_future != y_past)

        self.assertTrue(y_future > y_past)
        self.assertTrue(y_future >= y_past)
        self.assertFalse(y_past > y_future)
        self.assertFalse(y_past >= y_future)

        self.assertTrue(y_past < y_future)
        self.assertTrue(y_past <= y_future)
        self.assertFalse(y_future < y_past)
        self.assertFalse(y_future <= y_past)

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
        # TODO more challenging tests
        """
        You can compare Approximate date objects to regular date ones.
        """
        self.assertEqual(ApproximateDate(2008, 9, 3), date(2008, 9, 3))
        self.assertTrue(ApproximateDate(2008, 9, 3) < date(2009, 9, 3))
        self.assertTrue(ApproximateDate(2007) < date(2007, 9, 3))


class ApproxDateFiltering(unittest.TestCase):
    def setUp(self):
        for year in [2000, 2001, 2002, 2003, 2004]:
            ApproxDateModel.objects.create(start=ApproximateDate(year=year))

    def test_filtering_with_python_date(self):
        qs = ApproxDateModel.objects.filter(start__gt=date.today())
        # force evaluate queryset
        list(qs)

    def test_filtering_with_python_datetime(self):
        qs = ApproxDateModel.objects.filter(start__gt=datetime.now())
        # force evaluate queryset
        list(qs)


class TestApproximateDateField(unittest.TestCase):
    def test_deconstruction(self):
        f = ApproximateDateField()
        name, path, args, kwargs = f.deconstruct()
        new_instance = ApproximateDateField(*args, **kwargs)
        self.assertEqual(f.max_length, new_instance.max_length)

    def test_empty_fields(self):
        a1 = ApproxDateModel.objects.create(start="")

        if DJANGO_VERSION[0] < 2:
            self.assertEqual(0, ApproxDateModel.objects.filter(start=None).count())
        else:
            self.assertEqual(1, ApproxDateModel.objects.filter(start=None).count())
        self.assertEqual(1, ApproxDateModel.objects.filter(start=a1.start).count())
        self.assertEqual(1, ApproxDateModel.objects.filter(start="").count())
        self.assertEqual(1, ApproxDateModel.objects.filter(start=a1.start or "").count())


class TestDatabaseSorting(unittest.TestCase):
    def setUp(self):
        ApproxDateModel.objects.all().delete()

    def test_sequence(self):
        dates_order = (
            ApproximateDate(year=1),
            ApproximateDate(year=2),
            ApproximateDate(year=2, month=2),
            ApproximateDate(year=2, month=2, day=4),
            ApproximateDate(year=2, month=12),
        )

        for _date in dates_order:
            ApproxDateModel.objects.create(start=_date)

        query_result = ApproxDateModel.objects.order_by('start')
        for i, obj in enumerate(query_result):
            self.assertIsInstance(obj.start, ApproximateDate)
            self.assertEqual(obj.start, dates_order[i])

        query_result = ApproxDateModel.objects.order_by('-start')
        result_length = len(query_result)
        self.assertEqual(result_length, len(dates_order))
        for i, obj in enumerate(query_result):
            self.assertEqual(obj.start, dates_order[result_length-i-1])


class ApproximateDateFormTesting(unittest.TestCase):
    def test_form(self):
        ApproxDateForm()


class TestApproximateDate(unittest.TestCase):

    def test_from_string(self):
        cases = (
            ('9.5.1945', '%d.%m.%Y', {'year': 1945, 'month': 5, 'day': 9}),
            ('5.1945', '%m.%Y', {'year': 1945, 'month': 5}),
            ('1945', '%Y', {'year': 1945}),
            ('future', '%Y', {'future': True}),
            ('past', '%Y', {'past': True}),
        )
        for case in cases:
            self.assertEqual(ApproximateDate.from_string(case[0], case[1]),
                             ApproximateDate(**case[2]))

        with self.assertRaises(ValueError):
            ApproximateDate.from_string('9.5.1945', '%d.%Y')

    def test_format(self):
        self.assertEqual('*{:%m}*'.format(ApproximateDate(year=1945, month=5)), '*05*')

    def test_string(self):
        cases = (
            (ApproximateDate(year=1945), '1945'),
            (ApproximateDate(year=1945, month=5), '1945-05'),
            (ApproximateDate(year=1945, month=5, day=9), '1945-05-09'),
            (ApproximateDate(future=True), 'future'),
            (ApproximateDate(past=True), 'past'),
        )

        for case in cases:
            self.assertEqual(str(case[0]), case[1])

    def test_repr(self):
        self.assertEqual(repr(ApproximateDate(past=True)), 'ApproximateDate(past)')
        self.assertEqual(repr(ApproximateDate(year=1945)), 'ApproximateDate(1945)')


if __name__ == "__main__":
    unittest.main()
