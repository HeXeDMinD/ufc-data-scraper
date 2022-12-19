from models.base import BaseModel


class WinMethod(BaseModel):
    def __init__(
        self,
        knockout: int,
        knockout_per: int,
        decision: int,
        decision_per: int,
        submission: int,
        submission_per: int,
        average_fight_time: str,
    ) -> None:

        self.knockout = knockout
        self.knockout_per = knockout_per
        self.decision = decision
        self.decision_per = decision_per
        self.submission = submission
        self.submission_per = submission_per

        self.average_fight_time = average_fight_time