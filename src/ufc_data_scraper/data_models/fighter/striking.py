from dataclasses import dataclass

from ufc_data_scraper.data_models.fighter.strike_target import StrikeTarget
from ufc_data_scraper.data_models.fighter.strike_position import StrikePosition
from ufc_data_scraper.data_models.base import Base


@dataclass(frozen=True, order=True)
class Striking(Base):
    striking_accuracy: int
    strikes_landed: int
    strikes_attempted: int
    strikes_average: float
    strikes_absorbed_average: float
    striking_defence: int
    knockdown_average: float
    strike_target: StrikeTarget
    strike_position: StrikePosition
