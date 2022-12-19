from models.base import BaseModel


class WeightClass(BaseModel):
    def __init__(self, description: str, abbreviation: str, weight: str) -> None:
        self.description = description
        self.abbreviation = abbreviation
        self.weight = weight

    def __str__(self) -> str:
        return self.description