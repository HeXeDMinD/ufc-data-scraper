import json
import concurrent.futures
import requests
import pytz

from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime, timedelta

from ufc_data_scraper.exceptions import InvalidEventUrl, MissingEventFMID

from ufc_data_scraper.utils import convert_date


def _page_has_event_links(site_content: str) -> bool:
    """Checks if page has event links.

    Args:
        site_content (str): Site raw response content.

    Returns:
        bool: Whether page has event links.
    """

    soup = BeautifulSoup(site_content, "html.parser")

    return soup.find("h3", class_="c-card-event--result__headline") and True or False


def _valid_event_page(site_content: str) -> bool:
    """Checks if page is a valid event page.

    Args:
        site_content (str): Site raw response content.

    Returns:
        bool: Whether page is a valid event page.
    """

    soup = BeautifulSoup(site_content, "html.parser")

    return (
        soup.find("div", class_="c-hero__headline-suffix tz-change-inner")
        and True
        or False
    )


def get_event_urls(page_num: int) -> list[str]:
    """Queries events with page_num and adds event urls to list.

    Args:
        page_num (int): Page number for query.

    Returns:
        list[str]: List of event urls returned from query.
    """

    page_query = {"page": page_num}

    site_response = requests.get("http://www.ufc.com/events", params=page_query)

    if site_response.status_code != 200 or not _page_has_event_links(
        site_response.content
    ):
        return

    only_headlines = SoupStrainer(
        "h3", attrs={"class": "c-card-event--result__headline"}
    )
    soup = BeautifulSoup(site_response.text, "html.parser", parse_only=only_headlines)

    headlines = list(soup)

    event_urls = []

    for item in headlines:
        url = item.find("a")["href"]
        url = f"http://www.ufc.com{url}"
        if url not in event_urls:
            event_urls.append(url)

    return event_urls


def _get_last_fmid() -> int:
    """Returns last available fmid from UFC events page.

    Returns:
        int: Latest FMID from queried event urls.
    """

    recent_events = get_event_urls(page_num=0)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(
                _scrape_event_fmid,
                requests.get(event_url),
            )
            for event_url in recent_events
        ]

    event_fmids = [future.result() for future in futures if future.result()]

    return max(event_fmids)


def _get_event_data(event_fmid: int) -> dict:
    """Queries private API and returns json data in dict format.

    Args:
        event_fmid (int): FMID to query.

    Returns:
        dict: Event data json in dict format
    """

    events_endpoint = (
        f"http://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{event_fmid}.json"
    )
    site_response = requests.get(events_endpoint)

    if site_response.status_code != 200:
        return None

    return site_response.json().get("LiveEventDetail")


def _get_event_date(soup: BeautifulSoup) -> str:
    """Returns event date.

    Args:
        soup (BeautifulSoup): BeautifulSoup object of page response.

    Returns:
        str: Event date in simple string format or None if it cannot be scraped.
        >>> "Sun, Dec 18 / 2:00 AM SAST"
    """

    target = soup.select(
        "#block-mainpagecontent > div > div.c-hero > div.c-hero__container > div > div.c-hero__bottom-text > div.c-hero__headline-suffix.tz-change-inner"
    )
    if len(target) < 1:
        return None

    return target[0].get_text().strip()


def _convert_scraped_date(date: str) -> datetime:
    """Converts scraped event date into usable format.

    Args:
        date (str): Date in simple string format.

    Returns:
        datetime: Datetime object of supplied string, localized to GMT.
    """

    # Website does not provide year; use current year
    date_now = datetime.now()
    year = date_now.year

    date = date.split(",")[1].strip()
    date = " ".join(date.split()[:-1])
    date = f"{year} {date}"

    tz = pytz.timezone("EST")

    date_time_obj = datetime.strptime(date, "%Y %b %d / %I:%M %p")

    # Check for wrap around and match years
    # Since this is only used for upcoming events we don't need to roll back
    if date_time_obj.month < date_now.month:
        date_time_obj += timedelta(days=365)

    date_time_obj = date_time_obj.replace(tzinfo=tz)

    date_time_obj = date_time_obj.astimezone(pytz.timezone("GMT"))

    return date_time_obj


def _scrape_event_fmid(site_response: requests.models.Response) -> int:
    """Gets event fmid from response, fmid can be used as API query.

    Args:
        site_response (requests.models.Response): Url response to scrape for event fmid.

    Returns:
        int: Event FMID, can be used as API query or None if it cannot be scraped.
    """

    only_script = SoupStrainer("script", attrs={"type": "application/json"})
    soup = BeautifulSoup(site_response.content, "html.parser", parse_only=only_script)

    try:
        site_scripts = json.loads(list(soup)[-1].text)
        fmid = int(site_scripts["eventLiveStats"]["event_fmid"])
    except (KeyError, IndexError):
        fmid = None

    return fmid


def _brute_force_event_fmid(site_response: requests.models.Response) -> int:
    """Attempt to brute force guess the event fmid if it is not available from the event url.

    Args:
        site_response (requests.models.Response): Url response to guess fmid from.

    Returns:
        int: Event FMID, can be used as API query or None if it cannot be acquired.
    """

    current_fmid = _get_last_fmid() - 10

    while True:
        data = _get_event_data(current_fmid)

        if not data or (data and len(data) < 1):
            break

        soup = BeautifulSoup(site_response.content, "html.parser")

        scraped_date = _get_event_date(soup)
        if scraped_date:
            scraped_date = _convert_scraped_date(scraped_date)
            api_date = convert_date(data["StartTime"])
            if abs(scraped_date - api_date) <= timedelta(days=2):
                return current_fmid

        current_fmid += 1

    return None


def get_event_fmid(event_url: str) -> int:
    """Gets event fmids from url, fmid can be used as API query.

    Returns:
        int: Event FMID, can be used as API query.
    """

    site_response = requests.get(event_url)

    site_response.raise_for_status()

    if not _valid_event_page(site_response.content):
        raise InvalidEventUrl

    fmid = _scrape_event_fmid(site_response) or _brute_force_event_fmid(site_response)
    if not fmid:
        raise MissingEventFMID(f"FMID could not be found for {event_url}")

    return fmid
