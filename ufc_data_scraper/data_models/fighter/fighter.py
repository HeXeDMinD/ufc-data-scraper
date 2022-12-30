from dataclasses import dataclass

from ufc_data_scraper.data_models.fighter.record import Record
from ufc_data_scraper.data_models.fighter.win_method import WinMethod
from ufc_data_scraper.data_models.fighter.physical_stats import PhysicalStats
from ufc_data_scraper.data_models.fighter.striking import Striking
from ufc_data_scraper.data_models.fighter.grappling import Grappling
from ufc_data_scraper.data_models.base import Base


@dataclass(frozen=True, order=True)
class Fighter(Base):
    fighter_url: str
    name: str
    nickname: str
    status: str
    ranking: str
    pfp_ranking: str
    weight_class: str
    home_city: str
    home_country: str
    gym: str
    fighting_style: str
    record: Record
    win_method: WinMethod
    physical_stats: PhysicalStats
    striking: Striking
    grappling: Grappling
