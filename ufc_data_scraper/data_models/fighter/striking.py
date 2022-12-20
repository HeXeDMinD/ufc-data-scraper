from dataclasses import dataclass

from ufc_data_scraper.data_models.fighter.strike_position import StrikePosition
from ufc_data_scraper.data_models.fighter.strike_target import StrikeTarget


@dataclass(frozen=True, order=True)
class Striking():
    striking_accuracy: int
    strikes_landed: int
    strikes_attempted: int
    strikes_average: float
    strikes_absorbed_average: float
    striking_defence: int
    knockdown_average: float
    strike_position: StrikePosition
    strike_target: StrikeTarget