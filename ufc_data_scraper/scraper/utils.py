import pytz

from datetime import datetime

def _convert_date(date: str) -> datetime:
    """Localizes API response date to GMT.

    Returns:
        str: date_obj
    """

    date_obj = None

    if date:
        date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%MZ")
        date_obj = pytz.timezone("GMT").localize(date_obj)

    return date_obj