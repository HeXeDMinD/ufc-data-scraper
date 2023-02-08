from datetime import datetime

from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase

from ufc_data_scraper.data_models.event.location import Location
from ufc_data_scraper.data_models.event.card_segment import CardSegment


@dataclass(frozen=True, order=True)
class Event(DataModelBase):
    fmid: int
    event_url: str
    name: str
    date: datetime
    status: str
    location: Location
    card_segments: list[CardSegment]
