from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class StrikePosition(DataModelBase):
    standing: int
    standing_per: int
    clinch: int
    clinch_per: int
    ground: int
    ground_per: int
