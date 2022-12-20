from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Record():
    win: int
    loss: int
    draw: int