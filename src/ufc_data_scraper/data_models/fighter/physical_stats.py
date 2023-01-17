from dataclasses import dataclass

from ufc_data_scraper.data_models.base import Base


@dataclass(frozen=True, order=True)
class PhysicalStats(Base):
    age: int
    height: float
    weight: float
    reach: float
    leg_reach: float
