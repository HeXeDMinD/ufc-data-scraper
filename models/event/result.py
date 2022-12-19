from models.base import BaseModel


class Result(BaseModel):
    def __init__(
        self,
        method: str,
        ending_round: int,
        ending_time: str,
        ending_strike: str,
        ending_target: str,
        ending_position: str,
        ending_submission: str,
        ending_notes: str,
        fight_of_the_night: bool,
    ) -> None:

        self.method = method

        self.ending_round = ending_round
        self.ending_time = ending_time

        self.ending_strike = ending_strike
        self.ending_target = ending_target
        self.ending_position = ending_position
        self.ending_submission = ending_submission
        self.ending_notes = ending_notes

        self.fight_of_the_night = fight_of_the_night

    def __str__(self) -> str:
        return self.method