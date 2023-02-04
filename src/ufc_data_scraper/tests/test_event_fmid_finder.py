import pytest

import requests
import pytz

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from ufc_data_scraper.scraper.fmid_finder import (
    _page_has_event_links,
    _valid_event_page,
    get_event_urls,
    _get_last_fmid,
    _get_event_data,
    _get_event_date,
    _convert_scraped_date,
    _scrape_event_fmid,
    _brute_force_event_fmid,
    get_event_fmid,
)


class TestEventFmidFinder:
    def test_page_has_event_links_has_links(self):
        test_page = """
            <div class="c-card-event--result__info">
                <h3 class="c-card-event--result__headline">
                    <a href="/event/ufc-287">Pereira vs Adesanya 2</a>
                </h3>
                <div class="c-card-event--result__date tz-change-data" data-locale="en" data-main-card="Sun, Apr 9 / 4:00 AM SAST" data-main-card-timestamp="1681005600" data-prelims-card="Sun, Apr 9 / 2:00 AM SAST" data-prelims-card-timestamp="1680998400" data-early-card="Sun, Apr 9 / 12:15 AM SAST" data-early-card-timestamp="1680992100" data-card-event-metric="0" data-card-event-title="Main Card">
                    <a href="/event/ufc-287">Sun, Apr 9 / 4:00 AM SAST / Main Card</a>
                </div>
                <div class="e-p--small c-card-event--result__location"></div>
            </div>
        """

        assert _page_has_event_links(test_page) is True

    def test_page_has_event_links_no_links(self):
        test_page = """
            <div class="c-card-event--result__info">
                <h3>
                    <a href="/event/ufc-287">Pereira vs Adesanya 2</a>
                </h3>
                <div class="c-card-event--result__date tz-change-data" data-locale="en" data-main-card="Sun, Apr 9 / 4:00 AM SAST" data-main-card-timestamp="1681005600" data-prelims-card="Sun, Apr 9 / 2:00 AM SAST" data-prelims-card-timestamp="1680998400" data-early-card="Sun, Apr 9 / 12:15 AM SAST" data-early-card-timestamp="1680992100" data-card-event-metric="0" data-card-event-title="Main Card">
                    <a href="/event/ufc-287">Sun, Apr 9 / 4:00 AM SAST / Main Card</a>
                </div>
                <div class="e-p--small c-card-event--result__location"></div>
            </div>
        """

        assert _page_has_event_links(test_page) is False

    def test_page_has_event_links_empty_page(self):
        test_page = ""

        assert _page_has_event_links(test_page) is False

    def test_valid_event_page_valid_page(self):
        test_page = """
            <div class="c-hero__headline-suffix tz-change-inner" data-locale="en" data-timestamp="1670727600" data-metric="0">Sun, Dec 11 / 5:00 AM SAST</div>
        """

        assert _valid_event_page(test_page) is True

    def test_valid_event_page_invalid_page(self):
        test_page = """
            <div class="c-card-event--result__info">
                <h3>
                    <a href="/event/ufc-287">Pereira vs Adesanya 2</a>
                </h3>
                <div class="c-card-event--result__date tz-change-data" data-locale="en" data-main-card="Sun, Apr 9 / 4:00 AM SAST" data-main-card-timestamp="1681005600" data-prelims-card="Sun, Apr 9 / 2:00 AM SAST" data-prelims-card-timestamp="1680998400" data-early-card="Sun, Apr 9 / 12:15 AM SAST" data-early-card-timestamp="1680992100" data-card-event-metric="0" data-card-event-title="Main Card">
                    <a href="/event/ufc-287">Sun, Apr 9 / 4:00 AM SAST / Main Card</a>
                </div>
                <div class="e-p--small c-card-event--result__location"></div>
            </div>
        """

        assert _valid_event_page(test_page) is False

    def test_valid_event_page_empty_page(self):
        test_page = ""

        assert _valid_event_page(test_page) is False

    def test_get_event_urls(self):
        # test whether function actually returns urls.
        test_page_num = 0
        actual = get_event_urls(test_page_num)

        assert isinstance(actual, list)
        assert len(actual) > 0

    def test_get_event_urls_invalid_page(self):
        # test whether function actually returns urls.
        test_page_num = 99999
        actual = get_event_urls(test_page_num)

        assert actual is None

    def test_get_last_fmid(self):
        # test whether function actually returns an fmid.
        actual = _get_last_fmid()

        assert isinstance(actual, int)
        assert actual > 0

    def test_get_event_data(self):
        # test whether function actually returns data.
        test_fmid = 1124
        actual = _get_event_data(test_fmid)

        assert isinstance(actual, dict)
        assert len(actual) > 0

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
        actual = _get_event_date(test_soup)

        assert actual is None

    def test_convert_scraped_date(self):
        test_date = "Sat, Dec 10 / 10:00 PM EST"
        # Use current year since this is only used for upcoming events
        date_now = datetime.now()
        year = date_now.year
        expected = datetime(
            year=year, month=12, day=11, hour=3, minute=0, tzinfo=pytz.timezone("GMT")
        )
        actual = _convert_scraped_date(test_date)

        assert isinstance(actual, datetime)
        assert actual == expected

    def test_convert_scraped_date_next_year(self):
        date_now = datetime.now() - timedelta(days=30)
        test_date = datetime.strftime(date_now, "%a, %b %d / %I:%M %p EST")

        expected = date_now + timedelta(days=365)

        actual = _convert_scraped_date(test_date)

        assert actual.year == expected.year

    def test_scrape_event_fmid(self):
        test_url = "https://www.ufc.com/event/ufc-282"
        expected = 1124
        actual = _scrape_event_fmid(requests.get(test_url))

        assert actual == expected

    def test_scrape_event_fmid_no_fmid_on_page(self):
        test_url = "https://www.google.com"
        actual = _scrape_event_fmid(requests.get(test_url))

        assert actual is None

    def test_brute_force_event_fmid(self):
        event_urls = get_event_urls(page_num=0)
        test_url = event_urls[0]

        actual = _brute_force_event_fmid(requests.get(test_url))

        assert actual is not None

    def test_get_event_fmid(self):
        test_url = "https://www.ufc.com/event/ufc-282"
        expected = 1124
        actual = get_event_fmid(test_url)

        assert actual == expected

    def test_get_event_fmid_not_valid_event_url(self):
        test_url = "https://www.google.com"

        with pytest.raises(Exception, match=r"Url is not a valid event url."):
            get_event_fmid(test_url)
