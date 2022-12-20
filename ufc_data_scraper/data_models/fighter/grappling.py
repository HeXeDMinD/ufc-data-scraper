from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Grappling():
    takedown_accuracy: int
    takedowns_landed: int
    takedowns_attempted: int
    takedowns_average: float
    takedown_defence: int
    submission_average: float