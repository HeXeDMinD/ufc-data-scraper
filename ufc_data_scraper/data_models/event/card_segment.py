from datetime import datetime

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class CardSegment:
    name: str
    start_time: datetime
    broadcaster: str

    fights: list
