from datetime import datetime
from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class CardSegment(DataModelBase):
    name: str
    start_time: datetime
    broadcaster: str

    fights: list
