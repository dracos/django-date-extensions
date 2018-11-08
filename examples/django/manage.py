#!/usr/bin/env python
import os
import sys
from pathlib import Path


sys.path.pop(0)
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "examples.django.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
