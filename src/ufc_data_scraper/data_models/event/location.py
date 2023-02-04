from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class Location(DataModelBase):
    venue: str
    city: str
    country: str
    tricode: str
