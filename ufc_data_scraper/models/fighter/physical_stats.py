from ufc_data_scraper.models.base import BaseModel


class PhysicalStats(BaseModel):
    def __init__(
        self,
        age: int,
        height: float,
        weight: float,
        reach: float,
        leg_reach: float,
    ) -> None:

        self.age = age
        self.height = height
        self.weight = weight
        self.reach = reach
        self.leg_reach = leg_reach

    def __str__(self) -> str:
        return f"{self.height}, {self.weight}"