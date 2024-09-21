import os
import django
from django.test import TestCase
from django.apps import apps
if not apps.ready:
    django.setup()


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(TEST_DIR, "json_files")
JSON_PATHS = [os.path.join(JSON_DIR, file) for file in os.listdir(JSON_DIR)]


class TestMapper(TestCase):

    pass