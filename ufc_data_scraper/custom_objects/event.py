from datetime import datetime

from ufc_data_scraper.custom_objects.base_object import _BaseObject
from ufc_data_scraper.custom_objects.fighter import Fighter


class Location(_BaseObject):
    def __init__(self, venue: str, city: str, country: str, tricode: str) -> None:
        self.venue = venue
        self.city = city
        self.country = country
        self.tricode = tricode

    def __str__(self) -> str:
        return f"{self.venue} - {self.city}, {self.country}"


class Result(_BaseObject):
    def __init__(
        self,
        method: str,
        ending_round: int,
        ending_time: str,
        ending_strike: str,
        ending_target: str,
        ending_position: str,
        ending_submission: str,
        ending_notes: str,
        fight_of_the_night: bool,
    ) -> None:

        self.method = method

        self.ending_round = ending_round
        self.ending_time = ending_time

        self.ending_strike = ending_strike
        self.ending_target = ending_target
        self.ending_position = ending_position
        self.ending_submission = ending_submission
        self.ending_notes = ending_notes

        self.fight_of_the_night = fight_of_the_night

    def __str__(self) -> str:
        return self.method


class WeightClass(_BaseObject):
    def __init__(self, description: str, abbreviation: str, weight: str) -> None:
        self.description = description
        self.abbreviation = abbreviation
        self.weight = weight

    def __str__(self) -> str:
        return self.description


class Accolade(_BaseObject):
    def __init__(self, description: str, type: str) -> None:
        self.description = description
        self.type = type

    def __str__(self) -> str:
        return self.description


class RuleSet(_BaseObject):
    def __init__(self, description: str, possible_rounds: str) -> None:
        self.description = description
        self.possible_rounds = possible_rounds

    def __str__(self) -> str:
        return self.description


class FightScore(_BaseObject):
    def __init__(self, judge_name: str, score_red: int, score_blue: int) -> None:
        self.judge_name = judge_name
        self.score_red = score_red
        self.score_blue = score_blue

    def __str__(self) -> str:
        return f"{self.judge_name}: {self.score_red} - {self.score_blue}"


class FighterStats(_BaseObject):
    def __init__(
        self,
        fighter: Fighter,
        corner: str,
        weigh_in: float,
        outcome: str,
        ko_of_the_night: bool,
        submission_of_the_night: bool,
        performance_of_the_night: bool,
    ) -> None:

        self.fighter = fighter
        self.corner = corner
        self.weigh_in = weigh_in
        self.outcome = outcome

        self.ko_of_the_night = ko_of_the_night
        self.submission_of_the_night = submission_of_the_night
        self.performance_of_the_night = performance_of_the_night

    def __str__(self) -> str:
        return self.fighter.name


class Fight(_BaseObject):
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


class CardSegment(_BaseObject):
    def __init__(
        self, name: str, start_time: datetime, broadcaster: str, fights: list
    ) -> None:
        self.name = name
        self.start_time = start_time
        self.broadcaster = broadcaster

        self.fights = fights

    def __str__(self) -> str:
        return self.name


class Event(_BaseObject):
    def __init__(
        self,
        fmid: int,
        name: str,
        date: datetime,
        status: str,
        location: Location,
        card_segments: dict,
    ) -> None:

        super().__init__()

        self.fmid = fmid
        self.name = name
        self.date = date
        self.status = status

        self.location = location
        self.card_segments = card_segments

    def __str__(self) -> str:
        return self.name
