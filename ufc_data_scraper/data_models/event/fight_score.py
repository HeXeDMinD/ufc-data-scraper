from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class FightScore():
    judge_name: str
    score_red: int
    score_blue: int