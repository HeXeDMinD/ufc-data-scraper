from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase

from ufc_data_scraper.data_models.fighter.strike_target import StrikeTarget
from ufc_data_scraper.data_models.fighter.strike_position import StrikePosition


@dataclass(frozen=True, order=True)
class Striking(DataModelBase):
    striking_accuracy: int
    strikes_landed: int
    strikes_attempted: int
    strikes_average: float
    strikes_absorbed_average: float
    striking_defence: int
    knockdown_average: float
    strike_target: StrikeTarget
    strike_position: StrikePosition
