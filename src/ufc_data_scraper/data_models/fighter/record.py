from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class Record(DataModelBase):
    win: int
    loss: int
    draw: int
