# encoding: utf-8
"""Test utility functions."""
from unittest import TestCase
import os

from uc.utils import parse_result_page
from requests.exceptions import HTTPError

DATA_DIR = "tests/data"

class TestUtils(TestCase):

    def setUp(self):
        pass

    def test_parse_result_page(self):
        file_path = os.path.join(DATA_DIR, "branschstatistik.html")
        with open(file_path) as f:
            content = f.read()
            data = parse_result_page(content)
