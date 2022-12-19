from ufc_data_scraper.models.base import BaseModel


class RuleSet(BaseModel):
    def __init__(self, description: str, possible_rounds: str) -> None:
        self.description = description
        self.possible_rounds = possible_rounds

    def __str__(self) -> str:
        return self.description