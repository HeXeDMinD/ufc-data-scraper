from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class Grappling(DataModelBase):
    takedown_accuracy: int
    takedowns_landed: int
    takedowns_attempted: int
    takedowns_average: float
    takedown_defence: int
    submission_average: float
