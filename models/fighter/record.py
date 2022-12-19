from models.base import BaseModel


class Record(BaseModel):
    def __init__(
        self,
        win: int,
        loss: int,
        draw: int,
    ) -> None:

        self.win = win
        self.loss = loss
        self.draw = draw

    def __str__(self) -> str:
        return f"{self.win}-{self.loss}-{self.draw}"