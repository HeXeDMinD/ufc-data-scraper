from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class Result(DataModelBase):
    method: str
    ending_round: int
    ending_time: str
    ending_strike: str
    ending_target: str
    ending_position: str
    ending_submission: str
    ending_notes: str
    fight_of_the_night: bool
