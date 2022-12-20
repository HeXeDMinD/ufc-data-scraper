from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class WinMethod:
    knockout: int
    knockout_per: int
    decision: int
    decision_per: int
    submission: int
    submission_per: int
    average_fight_time: str
