from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class PhysicalStats(DataModelBase):
    age: int
    height: float
    weight: float
    reach: float
    leg_reach: float
