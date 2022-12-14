import pytz

from datetime import datetime


def _convert_date(date: str) -> datetime:
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
