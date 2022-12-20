import requests
import pytz

from bs4 import BeautifulSoup
from datetime import datetime

from ufc_data_scraper.scraper.fmid_finder import (
    _page_is_valid,
    _get_event_urls,
    _get_last_fmid,
    _get_event_data,
    _get_event_date,
    _convert_scraped_date,
    _scrape_event_fmid,
    get_event_fmid,
)


class TestEventFmidFinder:
    def test_page_is_valid_valid_page(self):
        test_page = "<h3></h3>"
        test_soup = BeautifulSoup(test_page, "html.parser")
        expected = True

        assert _page_is_valid(test_soup) == expected

    def test_page_is_valid_invalid_page(self):
        test_page = "<h2></h2>"
        test_soup = BeautifulSoup(test_page, "html.parser")
        expected = False

        assert _page_is_valid(test_soup) == expected

    def test_page_is_valid_empty_page(self):
        test_page = ""
        test_soup = BeautifulSoup(test_page, "html.parser")
        expected = False

        assert _page_is_valid(test_soup) == expected

    def test_get_event_urls_type(self):
        test_page_num = 0
        expected = list
        actual = _get_event_urls(test_page_num)

        assert type(actual) == expected

    def test_get_event_urls_length(self):
        # test whether function actually returns urls.
        test_page_num = 0
        expected = 0
        actual = _get_event_urls(test_page_num)

        assert len(actual) > expected

    def test_get_last_fmid_type(self):
        expected = int
        actual = _get_last_fmid()

        assert type(actual) == expected

    def test_get_last_fmid(self):
        # test whether function actually returns an fmid.
        expected = 0
        actual = _get_last_fmid()

        assert actual > expected

    def test_get_event_data_type(self):
        test_fmid = 1124
        expected = dict
        actual = _get_event_data(test_fmid)

        assert type(actual) == expected

    def test_get_event_data(self):
        # test whether function actually returns data.
        test_fmid = 1124
        expected = 0
        actual = _get_event_data(test_fmid)

        assert len(actual) > expected

    def test_get_event_date(self):
        test_event_url = "https://www.ufc.com/event/ufc-282"
        test_response = requests.get(test_event_url)
        test_soup = BeautifulSoup(test_response.content, "html.parser")
        expected = "Sat, Dec 10 / 10:00 PM EST"
        actual = _get_event_date(test_soup)

        assert actual == expected

    def test_get_event_date_invalid_page(self):
        invalid_page = ""
        test_soup = BeautifulSoup(invalid_page, "html.parser")
        expected = None
        actual = _get_event_date(test_soup)

        assert actual == expected

    def test_convert_scraped_date_type(self):
        test_date = "Sat, Dec 10 / 10:00 PM EST"
        expected = datetime
        actual = _convert_scraped_date(test_date)

        assert type(actual) == expected

    def test_convert_scraped_date(self):
        test_date = "Sat, Dec 10 / 10:00 PM EST"
        expected = datetime(
            year=2022, month=12, day=11, hour=3, minute=0, tzinfo=pytz.timezone("GMT")
        )
        actual = _convert_scraped_date(test_date)

        assert actual == expected

    def test_scrape_event_fmid(self):
        test_event_url = "https://www.ufc.com/event/ufc-282"
        expected = 1124
        actual = _scrape_event_fmid(test_event_url)

        assert actual == expected

    def test_get_event_fmid(self):
        test_url = "https://www.ufc.com/event/ufc-282"
        expected = 1124
        actual = get_event_fmid(test_url)

        assert actual == expected
