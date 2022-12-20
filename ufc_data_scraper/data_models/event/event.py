from datetime import datetime

from dataclasses import dataclass

from ufc_data_scraper.data_models.event.location import Location


@dataclass(frozen=True, order=True)
class Event:
    fmid: int
    name: str
    date: datetime
    status: str
    location: Location
    card_segments: dict
