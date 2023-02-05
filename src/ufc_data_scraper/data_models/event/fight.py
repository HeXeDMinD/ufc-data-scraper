from dataclasses import dataclass

from ufc_data_scraper.data_models.base import DataModelBase

from ufc_data_scraper.data_models.event.fighter_stats import FighterStats
from ufc_data_scraper.data_models.event.result import Result
from ufc_data_scraper.data_models.event.weight_class import WeightClass
from ufc_data_scraper.data_models.event.accolade import Accolade
from ufc_data_scraper.data_models.event.rule_set import RuleSet
from ufc_data_scraper.data_models.event.fight_score import FightScore


@dataclass(frozen=True, order=True)
class Fight(DataModelBase):
    fight_order: int
    referee_name: str
    fighters_stats: list[FighterStats]
    result: Result
    weight_class: WeightClass
    accolades: Accolade
    rule_set: RuleSet
    fight_scores: list[FightScore]