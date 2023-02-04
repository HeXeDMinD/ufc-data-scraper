from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class FightScore(DataModelBase):
    judge_name: str
    score_red: int
    score_blue: int
