from ufc_data_scraper.scraper.fighter_scraper import FighterScraper
from ufc_data_scraper.models.fighter import Fighter

from ufc_data_scraper.scraper.event_fmid_finder import FmidFinder
from ufc_data_scraper.scraper.event_scraper import EventScraper
from ufc_data_scraper.models.event import Event

from ufc_data_scraper.scraper.utils import get_incorrect_urls


def get_event_fmid(event_url: str) -> int:
    """Gets event fmids from url, fmid can be used as API query.

    Returns:
        int: Event FMID, can be used as API query.
    """

    fmid_finder = FmidFinder()

    return fmid_finder.get_event_fmid(event_url)


def scrape_fighter_url(fighter_url: str) -> Fighter:
    """Scrapes fighter page.

    Args:
        fighter_url (str): UFC Fighter page.

    >>> fighter = scrape_fighter_url("https://www.ufc.com/athlete/jan-blachowicz")

    Returns:
        Fighter: Returns fighter object.
    """

    incorrect_urls = get_incorrect_urls()

    fighter_scraper = FighterScraper(fighter_url, incorrect_urls)

    return fighter_scraper.scrape_fighter()


def scrape_event_url(event_url: str) -> Event:
    """Scrapes event page.

    Args:
        event_url (str): UFC Event page.

    >>> event = scrape_event_url("https://www.ufc.com/event/ufc-282")

    Returns:
        Event: Returns event object.
    """

    event_fmid = get_event_fmid(event_url)

    event_scraper = EventScraper(event_fmid)

    return event_scraper.scrape_event()


def scrape_event_fmid(event_fmid: int) -> Event:
    """Scrapes event fmid.

    Args:
        event_fmid (int): UFC Event FMID.

    >>> event = scrape_event_fmid(1124)

    Returns:
        Event: Returns event object.
    """

    event_scraper = EventScraper(event_fmid)

    return event_scraper.scrape_event()
