from datetime import datetime

from models.base import BaseModel


class CardSegment(BaseModel):
    def __init__(
        self, name: str, start_time: datetime, broadcaster: str, fights: list
    ) -> None:
        self.name = name
        self.start_time = start_time
        self.broadcaster = broadcaster

        self.fights = fights

    def __str__(self) -> str:
        return self.name