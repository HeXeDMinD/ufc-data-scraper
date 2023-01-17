from dataclasses import dataclass

from ufc_data_scraper.data_models.base import Base


@dataclass(frozen=True, order=True)
class WeightClass(Base):
    description: str
    abbreviation: str
    weight: str
