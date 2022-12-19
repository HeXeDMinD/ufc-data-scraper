from models.base import BaseModel

from models.fighter.strike_position import StrikePosition
from models.fighter.strike_target import StrikeTarget


class Striking(BaseModel):
    def __init__(
        self,
        striking_accuracy: int,
        strikes_landed: int,
        strikes_attempted: int,
        strikes_average: float,
        strikes_absorbed_average: float,
        striking_defence: int,
        knockdown_average: float,
        strike_position: StrikePosition,
        strike_target: StrikeTarget,
    ) -> None:

        self.striking_accuracy = striking_accuracy
        self.strikes_landed = strikes_landed
        self.strikes_attempted = strikes_attempted
        self.strikes_average = strikes_average
        self.strikes_absorbed_average = strikes_absorbed_average
        self.striking_defence = striking_defence

        self.knockdown_average = knockdown_average

        self.strike_position = strike_position
        self.strike_target = strike_target