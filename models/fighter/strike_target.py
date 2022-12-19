from models.base import BaseModel


class StrikeTarget(BaseModel):
    def __init__(
        self,
        head: int,
        head_per: int,
        body: int,
        body_per: int,
        leg: int,
        leg_per: int,
    ) -> None:

        self.head = head
        self.head_per = head_per
        self.body = body
        self.body_per = body_per
        self.leg = leg
        self.leg_per = leg_per