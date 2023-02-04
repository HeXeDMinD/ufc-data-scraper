from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class StrikeTarget(DataModelBase):
    head: int
    head_per: int
    body: int
    body_per: int
    leg: int
    leg_per: int
