import requests
import pytz

from datetime import datetime

from ufc_data_scraper.scraper.classes.event import *
from ufc_data_scraper.scraper.classes.fighter import *
from ufc_data_scraper.scraper.fighter_scraper import _FighterScraper

class _EventScraper:
    def __init__(self, event_fmid: int) -> None:
        self._event_fmid = event_fmid
        self._event_data = self._get_event_data()
    
    def _get_event_data(self) -> dict:
        """Returns event api response as dict."""

        events_endpoint = f"http://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{self._event_fmid}.json"
        event_response = requests.get(events_endpoint)

        event_response.raise_for_status()

        return event_response.json().get("LiveEventDetail")

    def _convert_date(self, date: str) -> datetime:
        """Localizes API response date to GMT.

        Returns:
            str: date_obj
        """

        date_obj = None

        if date:
            date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%MZ")

            date_obj = pytz.timezone("GMT").localize(date_obj)

        return date_obj

    def _get_location_obj(self) -> Location:
        # TODO - Documentation
        location_data = self._event_data.get("Location")

        keys = ["Venue", "City", "Country", "TriCode"]
        location_data = {key.lower(): location_data[key] or "TBD" for key in keys}

        return Location(**location_data)

    def _get_fighter_name(self, fighter: dict):
        fighter_name = ""
        first_name = fighter.get("Name").get("FirstName")
        last_name = fighter.get("Name").get("LastName")
        if first_name == "":
            fighter_name = last_name
        elif last_name == "":
            fighter_name = first_name
        else:
            fighter_name = f"{first_name} {last_name}"
        return fighter_name

    def _get_fight_scores(self, fight: dict) -> list:
        fight_results = fight.get("Result")
        
        fight_scores = []
        
        for score in fight_results.get("FightScores"):
            judge_name = f"{score.get('JudgeFirstName')} {score.get('JudgeLastName')}"
            score_red = score.get("Fighters")[0].get("Score")
            score_blue = score.get("Fighters")[1].get("Score")
            
            fight_score = FightScore(judge_name, score_red, score_blue)
            
            fight_scores.append(fight_score)
            
        return fight_scores

    def _get_referee_name(self, fight: dict) -> str:
        """Returns fights referee object."""

        referee_name = ""

        referee = fight.get("Referee")
        if referee.get("FirstName"):
            referee_name = f"{referee.get('FirstName')} {referee.get('LastName')}"

        return referee_name

    def _get_fighter_url(self, fighter: dict) -> str:
        fighter_url = fighter.get("UFCLink")
        
        if not fighter_url:
            fighter_name = self._get_fighter_name(fighter)
            fighter_url = f"https://www.ufc.com/athlete/{fighter_name.replace(' ', '-')}"
        
        return fighter_url
    
    def _get_fighter_obj(self, fighter_url: str) -> Fighter:
        try:
            fighter_scraper = _FighterScraper(fighter_url)
            fighter = fighter_scraper._scrape_fighter()
        except requests.exceptions.HTTPError:
            fighter = None
            
        return fighter

    def _get_fighters_stats(self, fighter: dict) -> FighterStats:
        fighter_url = self._get_fighter_url(fighter)
        
        fighter_stats_data = {
            "fighter": self._get_fighter_obj(fighter_url) or fighter_url,
            "corner": fighter.get("Corner"),
            "weigh_in": fighter.get("WeighIn"),
            "outcome": fighter.get("Outcome").get("Outcome") or "TBD",
            "ko_of_the_night": fighter.get("KOOfTheNight"),
            "submission_of_the_night": fighter.get("SubmissionOfTheNight"),
            "performance_of_the_night": fighter.get("PerformanceOfTheNight"),
        }
        
        fighters_stats = FighterStats(**fighter_stats_data)
        
        return fighters_stats
    
    def _parse_fighters(self, fight: dict) -> list:
        fighters = fight.get("Fighters")
        
        return [self._get_fighters_stats(fighter) for fighter in fighters]
        
    def _get_result(self, fight: dict) -> Result:
        """Parses fight and returns result object."""

        fight_results = fight.get("Result")

        ending_round = fight_results.get("EndingRound")
        fight_of_the_night = fight_results.get("FightOfTheNight")

        keys = [
            "Method",
            "EndingTime",
            "EndingStrike",
            "EndingTarget",
            "EndingPosition",
            "EndingSubmission",
            "EndingNotes",
        ]
        fight_results = {key: fight_results[key] or "" for key in keys}

        fight_results["EndingRound"] = ending_round or 0
        fight_results["FightOfTheNight"] = fight_of_the_night

        result_obj = Result(
            method=fight_results.get("Method"),
            ending_round=fight_results.get("EndingRound"),
            ending_time=fight_results.get("EndingTime"),
            ending_strike=fight_results.get("EndingStrike"),
            ending_target=fight_results.get("EndingTarget"),
            ending_position=fight_results.get("EndingPosition"),
            ending_submission=fight_results.get("EndingSubmission"),
            ending_notes=fight_results.get("EndingNotes"),
            fight_of_the_night=fight_results.get("FightOfTheNight"),
        )

        return result_obj

    def _get_weight_class_obj(self, fight: dict) -> WeightClass:
        """Returns fight weight class object."""

        weight_class = fight.get("WeightClass")

        description = weight_class.get("Description")
        abbreviation = weight_class.get("Abbreviation")

        weight = weight_class.get("Weight")
        if not weight:
            weight = weight_class.get("CatchWeight")

        return WeightClass(description, abbreviation, weight)

    def _get_accolades_obj(self, fight: dict) -> Accolade:
        """Returns fights accolades object."""

        accolade_obj = None

        accolades = fight.get("Accolades")
        if len(accolades) > 0:
            accolade = accolades[0]
            type = accolade.get("Type")
            description = accolade.get("Name")
            accolade_obj = Accolade(description, type)

        return accolade_obj

    def _get_rule_set_obj(self, fight: dict) -> RuleSet:
        """Returns fights rule_set object."""

        rule_set = fight.get("RuleSet")
        
        description=rule_set.get("Description")
        possible_rounds=rule_set.get("PossibleRounds")

        return RuleSet(description, possible_rounds)

    def _parse_fight(self, fight: dict) -> Fight:
        fight_order = fight.get("FightOrder")
        referee_name = self._get_referee_name(fight)

        fighters_stats = self._parse_fighters(fight)
        result = self._get_result(fight)

        weight_class_obj = self._get_weight_class_obj(fight)
        accolades_obj = self._get_accolades_obj(fight)
        rule_set_obj = self._get_rule_set_obj(fight)

        fight_scores = self._get_fight_scores(fight)

        fight = Fight(
            fight_order,
            referee_name,
            fighters_stats,
            result,
            weight_class_obj,
            accolades_obj,
            rule_set_obj,
            fight_scores,
        )

        return fight

    def _get_card_segments(self) -> list:
        # TODO - Documentation
        fight_card = self._event_data.get("FightCard")
    
        card_segments = {}
        for fight in fight_card:
            segment_name = fight.get("CardSegment")
            start_time = fight.get("CardSegmentStartTime")
            broadcaster = fight.get("CardSegmentBroadcaster")
            parsed_fight = self._parse_fight(fight)
            if segment_name in card_segments.keys():
                card_segments[segment_name].fights.append(parsed_fight)
            else:
                card_segments[segment_name] = CardSegment(
                    segment_name, self._convert_date(start_time), broadcaster, fights=[parsed_fight]
                )

        return card_segments.values()
    
    def _scrape_event(self) -> Event:
        # TODO - Documentation

        event_date = self._event_data.get("StartTime")

        event_info = {
            "fmid": self._event_fmid,
            "name": self._event_data.get("Name"),
            "date": self._convert_date(event_date),
            "status": self._event_data.get("Status"),
            "location": self._get_location_obj(),
            "card_segments": self._get_card_segments()
        }

        return Event(**event_info)
