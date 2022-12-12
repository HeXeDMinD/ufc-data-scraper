from ufc_data_scraper.scraper.fighter_scraper import _FighterScraper
from ufc_data_scraper.custom_objects.fighter import Fighter

from ufc_data_scraper.scraper import event_fmid_finder
from ufc_data_scraper.scraper.event_scraper import _EventScraper
from ufc_data_scraper.custom_objects.event import Event

def scrape_fighter_url(fighter_url: str) -> Fighter:
    """Scrapes fighter page.

    Args:
        fighter_url (str): UFC Fighter page.

    >>> fighter = scrape_fighter_url("https://www.ufc.com/athlete/jan-blachowicz")

    Returns:
        Fighter: Returns fighter object.
    """

    fighter_scraper = _FighterScraper(fighter_url)

    return fighter_scraper._scrape_fighter()

def scrape_event_url(event_url: str) -> Event:
    """Scrapes event page.

    Args:
        event_url (str): UFC Event page.

    >>> event = scrape_event_url("https://www.ufc.com/event/ufc-282")

    Returns:
        Event: Returns event object.
    """
    event_fmid = event_fmid_finder.find_fmid(event_url)
    event_scraper = _EventScraper(event_fmid)

    return event_scraper._scrape_event()

def scrape_event_fmid(event_fmid: int) -> Event:
    """Scrapes event fmid.

    Args:
        event_fmid (int): UFC Event FMID.

    >>> event = scrape_event_fmid(1124)

    Returns:
        Event: Returns event object.
    """

    event_scraper = _EventScraper(event_fmid)

    return event_scraper._scrape_event()