# encoding: utf-8
import requests
from datetime import date, datetime
from bs4 import BeautifulSoup
from statscraper import (BaseScraper, Collection, DimensionValue,
                         Dataset, Dimension, Result)
from uc.utils import parse_result_page

BASE_URL = "https://www.uc.se"


class UCScraper(BaseScraper):

    def _fetch_itemslist(self, current_item):
        """This scraper has only one dataset."""
        html = self._get_request("/konkursstatistik/")
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.select(".treenav a"):
            if a.text == "Summering":
                continue

            yield UCDataset(a.text, a.text, blob=a)


    def _fetch_allowed_values(self, dimension):
        """Allowed values are only implemented for regions.
        """
        if dimension.id == "month":
            soup = dimension.dataset.soup
            for year_opt_group in soup.select("#SelectedValue optgroup"):
                year = int(year_opt_group.attrs["label"])
                for i, option in enumerate(year_opt_group.select("option")):
                    month_ix = option.attrs["value"]
                    month = option.text
                    label = date(year, i+1, 1).strftime("%Y-%m")
                    yield DimensionValue(month_ix, dimension, label=label)
        else:
            raise NotImplementedError()


    def _fetch_dimensions(self, dataset):
        yield Dimension("month") # query month 2016-01
        yield Dimension("dimension") # column name
        yield Dimension("group") # "Stockholms län"
        yield Dimension("grouper") # "Län"


    def _fetch_data(self, dataset, query):
        """Make the actual query.
        :param query:
        """
        # get latest month by default
        if query is None:
            query = "latest_month"

        months = []
        if query == "latest_month":
            months.append(dataset.latest_month)
        elif isinstance(query, dict):
            since = query.get("from", "2000-01")
            to = query.get("to", datetime.now().strftime("%Y-%m"))
            months = [x for x in dataset.dimensions["month"].allowed_values
             if since <= x.label and x.label <= to]

        for month in months:
            self.log.info(f"Fecthing data from {month.label}")
            url = BASE_URL + "/BankruptcyStatisticsCategoryPage/GetStatistics"
            html = self._post_request(url, {"selectedvalue": month.value})
            for res in parse_result_page(html):
                value = res["value"]
                res.pop("value")
                res["month"] = month.label
                yield Result(value, res)

    ###
    # HELPER METHODS
    ###
    def _get_request(self, url):
        """ Get html from url
        """
        url = BASE_URL + url
        self.log.info(u"/GET {}".format(url))
        r = requests.get(url)
        if hasattr(r, 'from_cache'):
            if r.from_cache:
                self.log.info("(from cache)")

        r.raise_for_status()

        return r.text

    def _post_request(self, url, payload):
        self.log.info(u"/POST {} with {}".format(url, payload))
        r = requests.post(url, payload)
        r.raise_for_status()

        return r.text



    @property
    def log(self):
        if not hasattr(self, "_logger"):
            self._logger = PrintLogger()
        return self._logger



class UCDataset(Dataset):

    @property
    def latest_month(self):
        """Get the latest available year."""

        return self.dimensions["month"].allowed_values[0]



    @property
    def url(self):
        return self.blob.attrs["href"]

    @property
    def html(self):
        if not hasattr(self, "_html"):
            self._html = self.scraper._get_request(self.url)
        return self._html


    @property
    def soup(self):
        if not hasattr(self, "_soup"):
            self._soup = BeautifulSoup(self.html, 'html.parser')
        return self._soup




class PrintLogger():
    """ Empyt "fake" logger
    """

    def log(self, msg, *args, **kwargs):
        print(msg)

    def debug(self, msg, *args, **kwargs):
        print(msg)

    def info(self, msg, *args, **kwargs):
        print(msg)

    def warning(self, msg, *args, **kwargs):
        print(msg)

    def error(self, msg, *args, **kwargs):
        print(msg)

    def critical(self, msg, *args, **kwargs):
        print(msg)
