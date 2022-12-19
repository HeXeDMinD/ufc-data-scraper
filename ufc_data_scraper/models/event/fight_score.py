from ufc_data_scraper.models.base import BaseModel


class FightScore(BaseModel):
    def __init__(self, judge_name: str, score_red: int, score_blue: int) -> None:
        self.judge_name = judge_name
        self.score_red = score_red
        self.score_blue = score_blue

    def __str__(self) -> str:
        return f"{self.judge_name}: {self.score_red} - {self.score_blue}"