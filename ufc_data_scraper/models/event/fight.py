from ufc_data_scraper.models.base import BaseModel
from ufc_data_scraper.models.event.result import Result
from ufc_data_scraper.models.event.weight_class import WeightClass
from ufc_data_scraper.models.event.accolade import Accolade
from ufc_data_scraper.models.event.rule_set import RuleSet

class Fight(BaseModel):
    def __init__(
        self,
        fight_order: int,
        referee_name: str,
        fighters_stats: list,
        result: Result,
        weight_class: WeightClass,
        accolades: Accolade,
        rule_set: RuleSet,
        fight_scores: list,
    ) -> None:

        self.fight_order = fight_order
        self.referee_name = referee_name

        self.fighters_stats = fighters_stats
        self.result = result
        self.weight_class = weight_class
        self.accolades = accolades
        self.rule_set = rule_set

        self.fight_scores = fight_scores

    def __str__(self) -> str:
        try:
            fighter_1_name = self.fighters_stats[0].fighter.name
        except AttributeError:
            fighter_1_name = "Missing Fighter"

        try:
            fighter_2_name = self.fighters_stats[1].fighter.name
        except AttributeError:
            fighter_2_name = "Missing Fighter"

        return f"{fighter_1_name} vs {fighter_2_name}"