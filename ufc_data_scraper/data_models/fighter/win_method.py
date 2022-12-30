from dataclasses import dataclass

from ufc_data_scraper.data_models.base import Base


@dataclass(frozen=True, order=True)
class WinMethod(Base):
    knockout: int
    knockout_per: int
    decision: int
    decision_per: int
    submission: int
    submission_per: int
    average_fight_time: str
