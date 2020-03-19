# encoding: utf-8
"""Tests for browsing the api."""
from unittest import TestCase
import re
from datetime import datetime
from statscraper import DimensionValue

from uc.scraper import UCScraper


class TestUCScraper(TestCase):

    def setUp(self):
        self.scraper = UCScraper()

    def test_list_datasets(self):
        assert len(self.scraper.items) == 3

    def test_allowed_values(self):
        dataset = self.scraper.items["Kommunstatistik"]
        dimension = dataset.dimensions["month"]
        assert len(dimension.allowed_values) > 0
        # make sure label is parseable as year-month
        datetime.strptime(dimension.allowed_values[0].label, "%Y-%m")

    def test_latest_month(self):
        dataset = self.scraper.items["Kommunstatistik"]
        latest_month = dataset.latest_month
        assert isinstance(latest_month, DimensionValue)


    def test_basic_query(self):
        for dataset in self.scraper.items:
            res = dataset.fetch()

    def test_query_time_range(self):
        dataset = self.scraper.items["Kommunstatistik"]
        res = dataset.fetch({"from": "2019-01", "to": "2019-02"})
        assert res.pandas["month"].unique().tolist() == ["2019-01", "2019-02"]
