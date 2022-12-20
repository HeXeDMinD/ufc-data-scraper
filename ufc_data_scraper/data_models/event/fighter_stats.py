from dataclasses import dataclass

from ufc_data_scraper.data_models.fighter.fighter import Fighter


@dataclass(frozen=True, order=True)
class FighterStats:
    fighter: Fighter
    corner: str
    weigh_in: float
    outcome: str
    ko_of_the_night: bool
    submission_of_the_night: bool
    performance_of_the_night: bool
