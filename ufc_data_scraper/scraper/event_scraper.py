import requests
import concurrent.futures

from ufc_data_scraper.scraper.fighter_scraper import FighterScraper

from ufc_data_scraper.data_models.event import *
from ufc_data_scraper.data_models.fighter import Fighter

from ufc_data_scraper.utils import convert_date


class EventScraper:
    def __init__(self, event_fmid: int) -> None:
        """Queries private UFC api and returns query as an Event object.

        Args:
            event_fmid (int): Event FMID, to query.

        >>> event_scraper = _EventScraper(event_fmid)
        >>> event = event_scraper._scrape_event()
        """

        self._event_fmid = event_fmid
        self._event_data = self._get_event_data()
        self._fighter_urls = self._get_fighter_urls()
        self._scraped_fighters = self._scrape_fighters()

    def _get_event_data(self) -> dict:
        """Returns event api response as dict.

        Returns:
            dict: API response in dictionary format.
        """

        events_endpoint = f"http://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{self._event_fmid}.json"
        event_response = requests.get(events_endpoint)

        event_response.raise_for_status()

        return event_response.json().get("LiveEventDetail")

    def _get_fighter_urls(self) -> list:
        fighter_urls = []

        for fight in self._event_data.get("FightCard"):
            for fighter in fight.get("Fighters"):
                url = self._get_fighter_url(fighter)
                fighter_urls.append(url.lower())

        return fighter_urls

    def _scrape_fighters(self) -> dict:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [
                executor.submit(
                    self._get_fighter_obj,
                    fighter_url,
                )
                for fighter_url in self._fighter_urls
            ]
            fighters = [future.result() for future in futures]
        return dict(zip(self._fighter_urls, fighters))

    def _get_location_obj(self) -> Location:
        """Get location data from event data and return it as a Location object.

        Returns:
            Location: Location object containing location data.
        """

        location_data = self._event_data.get("Location")

        keys = ["Venue", "City", "Country", "TriCode"]
        location_data = {
            key.lower(): location_data[key] or "TBD" for key in keys}

        return Location(**location_data)

    def _get_fighter_name(self, fighter: dict) -> str:
        """Get fighter name from fighter dictionary and return it as a string.

        Args:
            fighter (dict): Fighter dictionary from event data.

        Returns:
            str: Fighter's full name as a string.
        """

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
        """Get fight score information from fight dictionary convert each into a FightScore object and return them as a list.

        Args:
            fight (dict): Fight dictionary from event data.

        Returns:
            list: List of FightScore objects.
        """

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
        """Get referee name from fight dictionary and return it as a string.

        Args:
            fight (dict): Fight dictionary from event data.

        Returns:
            str: Referee's full name as a string.
        """

        referee_name = ""

        referee = fight.get("Referee")
        if referee.get("FirstName"):
            referee_name = f"{referee.get('FirstName')} {referee.get('LastName')}"

        return referee_name

    def _get_fighter_url(self, fighter: dict) -> str:
        """Get fighter url from event data or approximate it using their name if none is listed.

        Args:
            fighter (dict): Fighter dictionary from event data.

        Returns:
            str: Fighters ufc page url.
        """

        fighter_url = fighter.get("UFCLink")

        if not fighter_url:
            fighter_name = self._get_fighter_name(fighter)
            fighter_url = (
                f"https://www.ufc.com/athlete/{fighter_name.replace(' ', '-')}"
            )

        return fighter_url.lower()

    def _get_fighter_obj(self, fighter_url: str) -> Fighter:
        """Scrapes fighter data from fighter url and returns it as a Fighter object.

        Args:
            fighter_url (str): Fighters ufc page url.

        Returns:
            Fighter: Fighter object containing fighter's data.
        """

        try:
            figher_scraper = FighterScraper(fighter_url)
            fighter = figher_scraper.scrape_fighter()
        except requests.exceptions.HTTPError:
            fighter = None

        return fighter

    def _get_fighters_stats(self, fighter: dict) -> FighterStats:
        """Get fighter stats from fighter dictionary and return it as a FighterStats object.

        Args:
            fighter (dict): Fighter dictionary from event data.

        Returns:
            FighterStats: FighterStats object containing fighter stats from perticular fight.
        """

        fighter_url = self._get_fighter_url(fighter)

        try:
            fighter_obj = self._scraped_fighters[fighter_url]
        except KeyError:
            fighter_obj = fighter_url

        fighter_stats_data = {
            "fighter": fighter_obj,
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
        """Parse each fighter in fight dictionary, convert each into a FighterStats object and return them as a list.

        Args:
            fight (dict): Fight dictionary from event data.

        Returns:
            list: List of FighterStats objects.
        """

        fighters = fight.get("Fighters")

        return [self._get_fighters_stats(fighter) for fighter in fighters]

    def _get_result_obj(self, fight: dict) -> Result:
        """Get result information from fight dictionary and return it as a Result object.

        Args:
            fight (dict): Fight dictionary from event data.

        Returns:
            Result: Result object containing fight's result information.
        """

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
        """Get weight class information from fight dictionary and return it as a WeightClass object.

        Args:
            fight (dict): Fight dictionary from event data.

        Returns:
            WeightClass: WeightClass object containing fight weight class information.
        """

        weight_class = fight.get("WeightClass")

        description = weight_class.get("Description")
        abbreviation = weight_class.get("Abbreviation")

        weight = weight_class.get("Weight")
        if not weight:
            weight = weight_class.get("CatchWeight")

        return WeightClass(description, abbreviation, weight)

    def _get_accolades_obj(self, fight: dict) -> Accolade:
        """Get accolades information from fight dictionary and return it as an Accolade object.

        Args:
            fight (dict): Fight dictionary from event data.

        Returns:
            Accolade: Accolade object containing fight accolade information or None if no accolades are available.
        """

        accolade_obj = None

        accolades = fight.get("Accolades")
        if len(accolades) > 0:
            accolade = accolades[0]
            type = accolade.get("Type")
            description = accolade.get("Name")
            accolade_obj = Accolade(description, type)

        return accolade_obj

    def _get_rule_set_obj(self, fight: dict) -> RuleSet:
        """Get rule set information from fight dictionary and return it as a RuleSet object.

        Args:
            fight (dict): Fight dictionary from event data.

        Returns:
            RuleSet: RuleSet object containing fight's rule set information.
        """

        rule_set = fight.get("RuleSet")

        description = rule_set.get("Description")
        possible_rounds = rule_set.get("PossibleRounds")

        return RuleSet(description, possible_rounds)

    def _parse_fight(self, fight: dict) -> Fight:
        """Parse information from fight dictionary and return it as a Fight object.

        Args:
            fight (dict): Fight dictionary from event data.

        Returns:
            Fight: Fight object containing fight information.
        """

        fight_order = fight.get("FightOrder")
        referee_name = self._get_referee_name(fight)

        fighters_stats = self._parse_fighters(fight)
        result_obj = self._get_result_obj(fight)

        weight_class_obj = self._get_weight_class_obj(fight)
        accolades_obj = self._get_accolades_obj(fight)
        rule_set_obj = self._get_rule_set_obj(fight)

        fight_scores = self._get_fight_scores(fight)

        fight = Fight(
            fight_order,
            referee_name,
            fighters_stats,
            result_obj,
            weight_class_obj,
            accolades_obj,
            rule_set_obj,
            fight_scores,
        )

        return fight

    def _get_card_segments(self) -> dict:
        """Parse each card segment in event data, convert each into a CardSegment objects and return them as a dict.

        Returns:
            dict: Dictionary of card segements. name: CardSegment
        """

        fight_card = self._event_data.get("FightCard")

        card_segments = {}
        for fight in fight_card:
            name = fight.get("CardSegment") or "Main"
            start_time = fight.get("CardSegmentStartTime") or self._event_data.get(
                "StartTime"
            )
            broadcaster = fight.get("CardSegmentBroadcaster")
            parsed_fight = self._parse_fight(fight)
            if name in card_segments.keys():
                card_segments[name].fights.append(parsed_fight)
            else:
                card_segments[name] = CardSegment(
                    name=name,
                    start_time=convert_date(start_time),
                    broadcaster=broadcaster or "Unlisted",
                    fights=[parsed_fight],
                )

        return card_segments

    def scrape_event(self) -> Event:
        """Queries private UFC api and returns query as an Event object.

        Returns:
            Event: Event object containing all data about queried event.
        """

        event_date = self._event_data.get("StartTime")

        event_info = {
            "fmid": self._event_fmid,
            "name": self._event_data.get("Name"),
            "date": convert_date(event_date),
            "status": self._event_data.get("Status"),
            "location": self._get_location_obj(),
            "card_segments": self._get_card_segments(),
        }

        return Event(**event_info)
