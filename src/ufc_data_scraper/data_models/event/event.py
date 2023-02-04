from datetime import datetime

from dataclasses import dataclass

from ufc_data_scraper.data_models.event.location import Location
from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class Event(DataModelBase):
    fmid: int
    event_url: str
    name: str
    date: datetime
    status: str
    location: Location
    card_segments: list
