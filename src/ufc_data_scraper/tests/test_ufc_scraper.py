from ufc_data_scraper import scrape_fighter_url, scrape_event_url, scrape_event_fmid

from ufc_data_scraper.data_models import Fighter, Event


class TestUfcScraper:
    def test_scrape_fighter_url(self):
        test_url = "https://www.ufc.com/athlete/ali-alqaisi"  # Retired fighter
        actual = scrape_fighter_url(test_url)

        assert isinstance(actual, Fighter)

    def test_scrape_event_url(self):
        test_url = "https://www.ufc.com/event/ufc-282"
        actual = scrape_event_url(test_url)

        assert isinstance(actual, Event)

    def test_scrape_event_fmid(self):
        test_fmid = 1124  # Completed Event
        actual = scrape_event_fmid(test_fmid)

        assert isinstance(actual, Event)
