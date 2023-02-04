from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class RuleSet(DataModelBase):
    description: str
    possible_rounds: int
