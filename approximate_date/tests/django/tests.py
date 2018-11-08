from __future__ import absolute_import

import unittest
from datetime import date, datetime

from django import forms
from django.db import IntegrityError
from django.test import TestCase

from approximate_date.django.fields import VagueDateField
from approximate_date.tests.django.models import TestModel
from approximate_date.types import VagueDate


class ApproxDateForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = ('start', 'can_be_null')


class PastAndFuture(TestCase):

    def test_setting_both(self):
        self.assertRaises(ValueError, VagueDate, past=True, future=True)

    def test_setting_with_dates(self):
        self.assertRaises(ValueError, VagueDate, future=True, year=2000)
        self.assertRaises(ValueError, VagueDate, past=True, year=2000)


class CompareDates(TestCase):

    def test_compare(self):

        past = VagueDate(past=True)
        past_too = VagueDate(past=True)
        y_past = VagueDate(year=2000)
        y_future = VagueDate(year=2100)
        future = VagueDate(future=True)
        future_too = VagueDate(future=True)

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
        self.assertEqual(VagueDate(2008, 9, 3), date(2008, 9, 3))
        self.assertTrue(VagueDate(2008, 9, 3) < date(2009, 9, 3))
        self.assertTrue(VagueDate(2007) < date(2007, 9, 3))


class ApproxDateFiltering(TestCase):
    def setUp(self):
        for year in [2000, 2001, 2002, 2003, 2004]:
            TestModel.objects.create(start=VagueDate(year=year))

    def test_filtering_with_python_date(self):
        qs = TestModel.objects.filter(start__gt=date.today())
        # force evaluate queryset
        list(qs)

    def test_filtering_with_python_datetime(self):
        qs = TestModel.objects.filter(start__gt=datetime.now())
        # force evaluate queryset
        list(qs)


class TestApproximateDateField(TestCase):
    def test_deconstruction(self):
        f = VagueDateField()
        name, path, args, kwargs = f.deconstruct()
        new_instance = VagueDateField(*args, **kwargs)
        self.assertEqual(f.null, new_instance.null)

    def test_nullable(self):
        x = TestModel(start=VagueDate(future=True), can_be_null=None)
        x.save()
        with self.assertRaises(IntegrityError):
            x.start = None
            x.save()


class TestDatabaseSorting(TestCase):
    def setUp(self):
        TestModel.objects.all().delete()

    def test_sequence(self):
        dates_order = (
            VagueDate(year=1),
            VagueDate(year=2),
            VagueDate(year=2, month=2),
            VagueDate(year=2, month=2, day=4),
            VagueDate(year=2, month=12),
        )

        for _date in dates_order:
            TestModel.objects.create(start=_date)

        query_result = TestModel.objects.order_by('start')
        for i, obj in enumerate(query_result):
            self.assertIsInstance(obj.start, VagueDate)
            self.assertEqual(obj.start, dates_order[i])

        query_result = TestModel.objects.order_by('-start')
        result_length = len(query_result)
        self.assertEqual(result_length, len(dates_order))
        for i, obj in enumerate(query_result):
            self.assertEqual(obj.start, dates_order[result_length-i-1])


class ApproximateDateFormTesting(TestCase):
    def test_form(self):
        ApproxDateForm()


class TestApproximateDate(TestCase):

    def test_from_string(self):
        cases = (
            ('9.5.1945', '%d.%m.%Y', {'year': 1945, 'month': 5, 'day': 9}),
            ('5.1945', '%m.%Y', {'year': 1945, 'month': 5}),
            ('1945', '%Y', {'year': 1945}),
            ('future', '%Y', {'future': True}),
            ('past', '%Y', {'past': True}),
        )
        for case in cases:
            self.assertEqual(VagueDate.from_string(case[0], case[1]),
                             VagueDate(**case[2]))

        with self.assertRaises(ValueError):
            VagueDate.from_string('9.5.1945', '%d.%Y')

    def test_format(self):
        self.assertEqual('*{:%m}*'.format(VagueDate(year=1945, month=5)), '*05*')

    def test_string(self):
        cases = (
            (VagueDate(year=1945), '1945'),
            (VagueDate(year=1945, month=5), '1945-05'),
            (VagueDate(year=1945, month=5, day=9), '1945-05-09'),
            (VagueDate(future=True), 'future'),
            (VagueDate(past=True), 'past'),
        )

        for case in cases:
            self.assertEqual(str(case[0]), case[1])

    def test_repr(self):
        self.assertEqual(repr(VagueDate(past=True)), 'VagueDate(past)')
        self.assertEqual(repr(VagueDate(year=1945)), 'VagueDate(1945)')


if __name__ == "__main__":
    unittest.main()
