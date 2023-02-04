from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class WinMethod(DataModelBase):
    knockout: int
    knockout_per: int
    decision: int
    decision_per: int
    submission: int
    submission_per: int
    average_fight_time: str
