from models.base import BaseModel


class StrikePosition(BaseModel):
    def __init__(
        self,
        standing: int,
        standing_per: int,
        clinch: int,
        clinch_per: int,
        ground: int,
        ground_per: int,
    ) -> None:

        self.standing = standing
        self.standing_per = standing_per
        self.clinch = clinch
        self.clinch_per = clinch_per
        self.ground = ground
        self.ground_per = ground_per
