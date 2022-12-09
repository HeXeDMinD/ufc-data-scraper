## Project description

# UFC Data Scraper
**UFC Data Scraper** is a simple webscraping library.

## Scrape fighter pages
Easily scrape a fighters page and get a more convenient Fighter object to work with.

    >>> from ufc_data_scraper import ufc_scraper
    >>> fighter_url = "https://www.ufc.com/athlete/jan-blachowicz"
    >>> fighter = ufc_scraper.scrape_fighter_url(fighter_url)
	>>> type(fighter)
	'Fighter'
    >>> fighter_dict = fighter.to_dict()
or convert that Fighter object into a dictionary.
## Scrape event pages
Easily scrape an event page and get a more convenient Event object to work with.

Know the events internal event id(fmid)?

    >>> from ufc_data_scraper import ufc_scraper
    >>> event_fmid = 1124
    >>> event_data = ufc_scraper.scrape_event_fmid(1124)

or leave it to the library to figure out.

    >>> from ufc_data_scraper import ufc_scraper
    >>> event_url = "https://www.ufc.com/event/ufc-282"
    >>> event = ufc_scraper.scrape_event_url(event_url)
    >>> type(event)
	'Event'
 
    >>> event_dict = event.to_dict()

or convert that Event object into a dictionary.