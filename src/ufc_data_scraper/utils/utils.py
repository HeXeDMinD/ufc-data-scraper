import pytz
import requests

from datetime import datetime


def convert_date(date: str) -> datetime | None:
    """Converts API response date into usable format.

    Args:
        date (str): Date in simple string format.

    Returns:
        datetime: Datetime object of supplied string, localized to GMT.
    """

    if not date:
        return None

    date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%MZ")

    return pytz.timezone("GMT").localize(date_obj)


def get_incorrect_urls() -> dict | None:
    """Retrieves the latest incorrect urls from GitHub file.

    Returns:
        dict: Dictionary of incorrect fighter urls with their correct counterpart.
    """

    data_url = "https://raw.githubusercontent.com/HeXeDMinD/ufc-data-scraper/main/src/ufc_data_scraper/data/incorrect_urls.json"

    site_response = requests.get(data_url)

    if site_response.status_code != 200:
        return None

    return site_response.json()


def get_incorrect_names() -> dict | None:
    """Retrieves the latest incorrect names from GitHub file.

    Returns:
        dict: Dictionary of incorrect fighter names with their correct counterpart.
    """

    data_url = "https://raw.githubusercontent.com/HeXeDMinD/ufc-data-scraper/main/src/ufc_data_scraper/data/incorrect_names.json"

    site_response = requests.get(data_url)

    if site_response.status_code != 200:
        return None

    return site_response.json()
