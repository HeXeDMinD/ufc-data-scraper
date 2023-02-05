from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase

from ufc_data_scraper.data_models.fighter import Fighter


@dataclass(frozen=True, order=True)
class FighterStats(DataModelBase):
    fighter: Fighter
    fighter_url: str
    corner: str
    weigh_in: float
    outcome: str
    ko_of_the_night: bool
    submission_of_the_night: bool
    performance_of_the_night: bool
