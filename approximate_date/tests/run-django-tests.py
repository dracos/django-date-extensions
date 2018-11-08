#!/usr/bin/env python

import os
import sys
from pathlib import Path

sys.path.pop(0)
sys.path.insert(0, (str(Path(__file__).resolve().parents[2])))

import django
from django.conf import settings
from django.test.utils import get_runner


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'approximate_date.tests.django.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(["approximate_date.tests.django"])
    sys.exit(bool(failures))
