from dataclasses import dataclass

from ufc_data_scraper.data_models.base import Base


@dataclass(frozen=True, order=True)
class Location(Base):
    venue: str
    city: str
    country: str
    tricode: str
