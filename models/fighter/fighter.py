from models.base import BaseModel

from models.fighter.record import Record
from models.fighter.win_method import WinMethod
from models.fighter.physical_stats import PhysicalStats
from models.fighter.striking import Striking
from models.fighter.grappling import Grappling


class Fighter(BaseModel):
    def __init__(
        self,
        fighter_url: str,
        name: str,
        nickname: str,
        status: str,
        ranking: str,
        pfp_ranking: str,
        weight_class: str,
        home_city: str,
        home_country: str,
        gym: str,
        fighting_style: str,
        record: Record,
        win_method: WinMethod,
        physical_stats: PhysicalStats,
        striking: Striking,
        grappling: Grappling,
    ) -> None:

        super().__init__()

        self.fighter_url = fighter_url

        self.name = name
        self.nickname = nickname

        self.status = status
        self.ranking = ranking
        self.pfp_ranking = pfp_ranking
        self.weight_class = weight_class

        self.home_city = home_city
        self.home_country = home_country

        self.gym = gym
        self.fighting_style = fighting_style

        self.record = record
        self.win_method = win_method
        self.physical_stats = physical_stats
        self.striking = striking
        self.grappling = grappling

    def __str__(self) -> str:
        return self.name
