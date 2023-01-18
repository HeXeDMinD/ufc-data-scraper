import pytz
import requests

from datetime import datetime


def convert_date(date: str) -> datetime:
    """Converts API response date into usable format.

    Args:
        date (str): Date in simple string format.

    Returns:
        datetime: Datetime object of supplied string, localized to GMT.
    """

    date_obj = None

    if date:
        date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%MZ")
        date_obj = pytz.timezone("GMT").localize(date_obj)

    return date_obj


def get_incorrect_urls() -> dict[str, str]:
    """Grabs latest incorrect urls from github file.

    Returns:
        dict: Dictionary of incorrect fighter urls with their correct counterpart.
    """

    data_url = "https://raw.githubusercontent.com/HeXeDMinD/ufc-data-scraper/main/src/ufc_data_scraper/data/incorrect_urls.json"

    site_response = requests.get(data_url)

    if site_response.status_code != 200:
        return None

    return site_response.json()
