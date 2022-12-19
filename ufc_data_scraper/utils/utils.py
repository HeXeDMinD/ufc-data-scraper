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


def get_incorrect_urls() -> dict:
    """Queries a google web app for up to date list of incorrect fighter urls.

    Returns:
        dict: Dictionary of incorrect fighter urls with their correct counterpart.
    """

    google_web_app = f"https://script.google.com/macros/s/AKfycbzYJ7dC6Xg4MSKVg7XWI5yz32Gc97ePNQnRkPs9vDz21KRD7IjFnF938aUlsouKrRy5/exec"

    site_response = requests.get(google_web_app)

    if site_response.status_code != 200:
        return None

    return {
        incorrect.lower(): correct.lower()
        for incorrect, correct in site_response.json().items()
    }
