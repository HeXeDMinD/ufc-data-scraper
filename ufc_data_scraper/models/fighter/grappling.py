from ufc_data_scraper.models.base import BaseModel


class Grappling(BaseModel):
    def __init__(
        self,
        takedown_accuracy: int,
        takedowns_landed: int,
        takedowns_attempted: int,
        takedowns_average: float,
        takedown_defence: int,
        submission_average: float,
    ) -> None:

        self.takedown_accuracy = takedown_accuracy
        self.takedowns_landed = takedowns_landed
        self.takedowns_attempted = takedowns_attempted
        self.takedowns_average = takedowns_average
        self.takedown_defence = takedown_defence
        self.submission_average = submission_average

    def __str__(self) -> str:
        return self.takedown_accuracy