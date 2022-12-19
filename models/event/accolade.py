from models.base import BaseModel


class Accolade(BaseModel):
    def __init__(self, description: str, type: str) -> None:
        self.description = description
        self.type = type

    def __str__(self) -> str:
        return self.description