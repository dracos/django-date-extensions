from __future__ import absolute_import

import unittest
from datetime import date, datetime

from django import forms
from django.db import IntegrityError
from django.test import TestCase

from approximate_date.django.fields import VagueDateField
from approximate_date.tests.django.models import TestModel
from approximate_date.types import VagueDate


class TestVagueDateFiltering(TestCase):
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


class TestVagueDateField(TestCase):
    def test_deconstruction(self):
        f = VagueDateField()
        name, path, args, kwargs = f.deconstruct()
        new_instance = VagueDateField(*args, **kwargs)
        self.assertEqual(f.null, new_instance.null)

    def test_nullable(self):
        x = TestModel(start=VagueDate(year=2018), can_be_null=None)
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

        query_result = TestModel.objects.order_by("start")
        for i, obj in enumerate(query_result):
            self.assertIsInstance(obj.start, VagueDate)
            self.assertEqual(obj.start, dates_order[i])

        query_result = TestModel.objects.order_by("-start")
        result_length = len(query_result)
        self.assertEqual(result_length, len(dates_order))
        for i, obj in enumerate(query_result):
            self.assertEqual(obj.start, dates_order[result_length - i - 1])


class TestForm(TestCase):
    def test_form(self):
        class ApproxDateForm(forms.ModelForm):
            class Meta:
                model = TestModel
                fields = ("start", "can_be_null")

        ApproxDateForm().as_p()


if __name__ == "__main__":
    unittest.main()
