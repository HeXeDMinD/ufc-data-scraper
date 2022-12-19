from models.base import BaseModel

from models.fighter.fighter import Fighter

class FighterStats(BaseModel):
    def __init__(
        self,
        fighter: Fighter,
        corner: str,
        weigh_in: float,
        outcome: str,
        ko_of_the_night: bool,
        submission_of_the_night: bool,
        performance_of_the_night: bool,
    ) -> None:

        self.fighter = fighter
        self.corner = corner
        self.weigh_in = weigh_in
        self.outcome = outcome

        self.ko_of_the_night = ko_of_the_night
        self.submission_of_the_night = submission_of_the_night
        self.performance_of_the_night = performance_of_the_night

    def __str__(self) -> str:
        return self.fighter.name