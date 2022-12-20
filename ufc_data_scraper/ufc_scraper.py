from ufc_data_scraper.scraper import get_event_fmid, FighterScraper, EventScraper

from ufc_data_scraper.data_models import Fighter, Event


def scrape_fighter_url(fighter_url: str) -> Fighter:
    """Scrapes fighter page.

    Args:
        fighter_url (str): UFC Fighter page.

    >>> fighter = scrape_fighter_url("https://www.ufc.com/athlete/jan-blachowicz")

    Returns:
        Fighter: Returns fighter object.
    """

    fighter_scraper = FighterScraper(fighter_url)

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
