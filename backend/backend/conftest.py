import os
import sys

import django

# Add the project root directory to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")


def pytest_configure():
    django.setup()
