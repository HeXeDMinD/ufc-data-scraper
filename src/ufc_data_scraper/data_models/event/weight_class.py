from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class WeightClass(DataModelBase):
    description: str
    abbreviation: str
    weight: str
