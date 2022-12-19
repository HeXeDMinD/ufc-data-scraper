from datetime import datetime

from ufc_data_scraper.models.base import BaseModel

from ufc_data_scraper.models.event.location import Location

class Event(BaseModel):
    def __init__(
        self,
        fmid: int,
        name: str,
        date: datetime,
        status: str,
        location: Location,
        card_segments: dict,
    ) -> None:

        super().__init__()

        self.fmid = fmid
        self.name = name
        self.date = date
        self.status = status

        self.location = location
        self.card_segments = card_segments

    def __str__(self) -> str:
        return self.name