import requests
import re

from bs4 import BeautifulSoup, Tag, ResultSet
from unidecode import unidecode

from ufc_data_scraper.utils import *

from ufc_data_scraper.data_models.fighter import *


def set_fighter_url(fighter_url: str, incorrect_urls: dict) -> str:
    """Replaces incorrect urls and removes inconsistancies from url.

    Args:
        fighter_url (str): UFC fighter page url.
        incorrect_urls (dict): Dictionary of incorrect urls with their corrected counterpart.

    Returns:
        str: Corrected fighter url.
    """

    # Remove any strange chars from fighter name
    url_name = fighter_url.split("/")[-1].lower()

    banned_url_chars = ["--", "'", "."]
    for banned_char in banned_url_chars:
        if banned_char in url_name:
            url_name = url_name.replace(banned_char, "")
    fighter_url = f"http://www.ufc.com/athlete/{url_name}"
    fighter_url = unidecode(fighter_url)

    try:
        fighter_url = incorrect_urls[fighter_url]
    except (KeyError, TypeError):
        fighter_url = fighter_url

    return fighter_url


class FighterScraper:
    def __init__(
        self, fighter_url: str, incorrect_urls=utils.get_incorrect_urls()
    ) -> None:
        """Scrapes ufc fighter page and returns data as a Fighter object.

        Args:
            fighter_url (url): UFC fighter page url.
            incorrect_urls (dict, optional): Dictionary of incorrect fighter urls and their correct counterpart. If supplied the scraper won't request it from web app.

        >>> fighter_scraper = _FighterScraper(fighter_url)
        >>> fighter = fighter_scraper._scrape_fighter()
        """

        self._soup = None
        self._stats_section = None
        self._stats_targets = None
        self.fighter_url = set_fighter_url(fighter_url, incorrect_urls)

    def _get_name(self) -> str:
        """Gets fighter name.

        Returns:
            str: Fighter's full name.
        """

        name = ""

        target = self._soup.find("h1", class_="hero-profile__name")
        if target:
            name = target.get_text()

        name = name.replace("-", " ")
        return unidecode(name.strip())

    def _get_nickname(self) -> str:
        """Gets fighter nickname.

        Returns:
            str: Nickname.
        """

        nickname = ""

        target = self._soup.find("p", class_="hero-profile__nickname")
        if target:
            nickname = target.get_text().strip()
            nickname = nickname.replace('"', "")

        return nickname

    def _get_status(self) -> str:
        """Gets fighter's fighting status.

        Returns:
            str: Status.
        """

        status = "Unknown"

        targets = self._soup.find_all("div", class_="c-bio__field")
        for target in targets:
            label = target.find("div", class_="c-bio__label").get_text()
            if label == "Status":
                status = target.find("div", class_="c-bio__text").get_text().strip()
                break

        return status

    def _get_ranking(self) -> tuple:
        """Gets fighter's division and pound for pound ranking. Returns them as a tuple of str values.

        Returns:
            tuple: (ranking, pfp_ranking)
        """

        ranking, pfp_ranking = "Unranked", "PFP Unranked"

        champion_keywords = ("Interim", "Champion", "Title")

        targets = self._soup.find_all("p", class_="hero-profile__tag")
        for target in targets:
            text = target.get_text().strip()
            for keyword in champion_keywords:
                if keyword in text:
                    ranking = text

            match = re.match(r"^(#[0-9]+)", text)
            if match:
                if "PFP" in text:
                    pfp_ranking = f"{match.group()} PFP"
                else:
                    ranking = match.group()

        return (ranking, pfp_ranking)

    def _get_weightclass(self) -> str:
        """Gets fighter's weightclass.

        Returns:
            str: Weight class.
        """

        weightclass = "None"

        target = self._soup.find("p", class_="hero-profile__division-title")
        if target:
            target_text = target.get_text().strip()
            if target_text != "":
                weightclass = target_text
            else:
                match = re.search(r"\s([a-z]+weight)\s", str())
                if match:
                    weightclass = f"{match.group().strip().capitalize()} Division"

        return weightclass

    def _get_hometown(self) -> tuple:
        """Gets fighter's home city and country. Returns them as a tuple of str values.

        Returns:
            tuple: (city, country)
        """

        city, country = "Unlisted", "Unlisted"

        targets = self._soup.find_all("div", class_="c-bio__field")
        for target in targets:
            label = target.find("div", class_="c-bio__label").get_text()
            if label == "Hometown":
                text = target.find("div", class_="c-bio__text").get_text()
                split_text = text.split(", ")
                if len(split_text) > 1:
                    city = split_text[0].strip()
                    country = split_text[1].strip()
                else:
                    country = text.strip()
                break

        return (city, country)

    def _get_gym(self) -> str:
        """Gets the name of fighter's gym.

        Returns:
            str: Gym.
        """

        targets = self._soup.find_all("div", class_="c-bio__field")
        if not targets:
            return "Unlisted"
        
        for target in targets:
            label = target.find("div", class_="c-bio__label").get_text()
            if label == "Trains at":
                return target.find("div", class_="c-bio__text").get_text().strip()

        return "Unlisted"
    
    def _get_fighting_style(self) -> str:
        """Gets fighter's fighting style.

        Returns:
            str: Fighting style.
        """

        fighting_style = "Unlisted"

        targets = self._soup.find_all("div", class_="c-bio__field")
        for target in targets:
            label = target.find("div", class_="c-bio__label").get_text()
            if label == "Fighting style":
                fighting_style = (
                    target.find("div", class_="c-bio__text").get_text().strip()
                )
                break

        return fighting_style

    def _get_record_obj(self) -> Record:
        """Get record information from fighter page and return it as a Record object.

        Returns:
            Record: Record object containing fighter's record information.
        """

        win, loss, draw = 0, 0, 0

        target = self._soup.find("p", class_="hero-profile__division-body")
        if target:
            text = target.get_text().strip().split()[0]
            win, loss, draw = text.split("-")

        record = {"win": int(win), "loss": int(loss), "draw": int(draw)}

        return Record(**record)

    def _get_average_fight_time(self) -> str:
        """Gets fighter's average fight time.

        Returns:
            str: Average fight time.
        """

        average_fight_time = "00:00"

        targets = self._soup.find_all(
            "div", class_="c-stat-compare__group c-stat-compare__group-2"
        )
        for target in targets:
            label = target.find("div", class_="c-stat-compare__label").get_text()
            if label == "Average fight time":
                time = target.find("div", class_="c-stat-compare__number")
                if time:
                    time = time.get_text().strip()
                    if time != "":
                        average_fight_time = time

        return average_fight_time

    def _get_win_method_obj(self) -> WinMethod:
        """Get win method information and return it as a WinMethod object.

        Returns:
            WinMethod: WinMethod object containing fighter's win method information.
        """

        average_fight_time = self._get_average_fight_time()

        try:
            win_method_stats = self._parse_stats_section(self._stats_section[1])
            knockout, knockout_per = win_method_stats["ko/tko"]
            decision, decision_per = win_method_stats["dec"]
            submission, submission_per = win_method_stats["sub"]
        except IndexError:
            knockout, knockout_per = 0, 0
            decision, decision_per = 0, 0
            submission, submission_per = 0, 0

        win_method_stats = {
            "knockout": knockout,
            "knockout_per": knockout_per,
            "decision": decision,
            "decision_per": decision_per,
            "submission": submission,
            "submission_per": submission_per,
            "average_fight_time": average_fight_time,
        }

        return WinMethod(**win_method_stats)

    def _get_physical_stats_obj(self) -> PhysicalStats:
        """Get fighter's physical stats and return it as a PhysicalStats object.

        Returns:
            PhysicalStats: PhysicalStats object containing fighter's physical stats information.
        """

        field_names = ["Age", "Height", "Weight", "Reach", "Leg reach"]
        physical_stats = {
            "age": 0,
            "height": 0,
            "weight": 0,
            "reach": 0,
            "leg_reach": 0,
        }
        keys = list(physical_stats.keys())

        targets = self._soup.find_all("div", class_="c-bio__field")
        for target in targets:
            label = target.find("div", class_="c-bio__label").get_text()
            for i, name in enumerate(field_names):
                if label == name:
                    field_value = (
                        target.find("div", class_="c-bio__text").get_text().strip()
                    )
                    if field_value:
                        if name != "Age":
                            physical_stats[keys[i]] = float(field_value)
                        else:
                            physical_stats[keys[i]] = int(field_value)

        return PhysicalStats(**physical_stats)

    def _get_strike_position_obj(self) -> StrikePosition:
        """Get fighter's strike position information and return it as a StrikePosition object.

        Returns:
            StrikePosition: StrikePosition object containing fighter's strike position information.
        """

        try:
            position_stats = self._parse_stats_section(self._stats_section[0])
            standing, standing_per = position_stats["standing"]
            clinch, clinch_per = position_stats["clinch"]
            ground, ground_per = position_stats["ground"]
        except IndexError:
            standing, standing_per = 0, 0
            clinch, clinch_per = 0, 0
            ground, ground_per = 0, 0

        strike_position_stats = {
            "standing": standing,
            "standing_per": standing_per,
            "clinch": clinch,
            "clinch_per": clinch_per,
            "ground": ground,
            "ground_per": ground_per,
        }
        return StrikePosition(**strike_position_stats)

    def _get_strike_target_obj(self) -> StrikeTarget:
        """Get fighter's strike target information and return it as a StrikeTarget object.

        Returns:
            StrikeTarget: StrikeTarget object containing fighter's strike target information.
        """

        field_names = ["head", "body", "leg"]
        strike_target_stats = {
            "head": 0,
            "head_per": 0,
            "body": 0,
            "body_per": 0,
            "leg": 0,
            "leg_per": 0,
        }

        target = self._soup.find("svg", class_="c-stat-body__svg")
        if target:
            fields = target.find_all("text")
            for name in field_names:
                value, value_per = 0, 0
                for field in fields:
                    try:
                        field_id = field["id"]
                    except KeyError:
                        continue
                    if f"{name}_percent" in field_id:
                        value_per = field.get_text().replace("%", "").strip()
                    elif f"{name}_value" in field_id:
                        value = field.get_text().strip()
                strike_target_stats[name] = int(value)
                strike_target_stats[f"{name}_per"] = int(value_per)

        return StrikeTarget(**strike_target_stats)

    def _get_striking_stats(self) -> dict:
        """Get fighter's striking information and return it as a dict.

        Returns:
            dict: Dictionary containing fighter's striking information.
        """

        try:
            (
                striking_accuracy,
                strikes_landed,
                strikes_attempted,
            ) = self._parse_stat_block(self._stats_targets[0])
        except IndexError:
            striking_accuracy, strikes_landed, strikes_attempted = 0, 0, 0

        striking_stats_block1 = {
            "striking_accuracy": striking_accuracy,
            "strikes_landed": strikes_landed,
            "strikes_attempted": strikes_attempted,
        }

        dict_keys = [
            "Sig. Str. Landed",
            "Sig. Str. Absorbed",
            "Sig. Str. Defense",
            "Knockdown Avg",
        ]
        striking_results = self._parse_result_set(self._stats_targets, dict_keys)

        striking_stats_block2 = {
            "strikes_average": float(striking_results["Sig. Str. Landed"]),
            "strikes_absorbed_average": float(striking_results["Sig. Str. Absorbed"]),
            "striking_defence": int(striking_results["Sig. Str. Defense"]),
            "knockdown_average": float(striking_results["Knockdown Avg"]),
        }

        striking_stats = striking_stats_block1 | striking_stats_block2
        return striking_stats

    def _create_striking_obj(
        self,
        striking_stats: dict,
        strike_position: StrikePosition,
        strike_target: StrikeTarget,
    ) -> Striking:
        """Takes fighter's striking, strike position and striking target information and returns them as a Striking object.

        Args:
            striking_stats (dict): Dictionary containing fighter's striking information.
            strike_position (StrikePosition): StrikePosition object containing fighter's strike position information.
            strike_target (StrikeTarget): StrikeTarget object containing fighter's strike target information.

        Returns:
            Striking: Striking object containing all of the fighter's striking, strike position and striking target information.
        """

        stats = striking_stats | {
            "strike_position": strike_position,
            "strike_target": strike_target,
        }
        return Striking(**stats)

    def _get_grappling_obj(self) -> Grappling:
        """Get fighter's grappling information and return it as a Grappling object.

        Returns:
            Grappling: Grappling object containing fighter's grappling information.
        """

        try:
            (
                takedown_accuracy,
                takedowns_landed,
                takedowns_attempted,
            ) = self._parse_stat_block(self._stats_targets[1])
        except IndexError:
            takedown_accuracy, takedowns_landed, takedowns_attempted, = (
                0,
                0,
                0,
            )

        grappling_stats_block1 = {
            "takedown_accuracy": takedown_accuracy,
            "takedowns_landed": takedowns_landed,
            "takedowns_attempted": takedowns_attempted,
        }

        dict_keys = ["Takedown avg", "Takedown Defense", "Submission avg"]
        grappling_results = self._parse_result_set(self._stats_targets, dict_keys)
        grappling_stats_block2 = {
            "takedowns_average": float(grappling_results["Takedown avg"]),
            "takedown_defence": int(grappling_results["Takedown Defense"]),
            "submission_average": float(grappling_results["Submission avg"]),
        }

        grappling_stats = grappling_stats_block1 | grappling_stats_block2

        return Grappling(**grappling_stats)

    def _parse_stat_block(self, target: Tag) -> tuple:
        """Parses stat block for striking and takedown stats, gets accuracy, landed and attempted information. Returns them as a tuple of int values.

        Args:
            target (Tag): Tag containing desired stats.

        Returns:
            tuple: (accuracy, landed, attempted)
        """

        accuracy, landed, attempted = 0, 0, 0

        acc_target = target.find("title")
        if acc_target:
            try:
                accuracy = int(
                    acc_target.get_text().split()[-1].replace("%", "").strip()
                )
            except IndexError:
                pass

        targets = target.find_all("dd", "c-overlap__stats-value")
        if targets:
            try:
                landed_target = targets[0].get_text().strip()
                if landed_target != "":
                    landed = int(landed_target)
            except IndexError:
                pass

            try:
                attempted_target = targets[1].get_text().strip()
                if attempted_target != "":
                    attempted = int(attempted_target)
            except IndexError:
                pass

        return (accuracy, landed, attempted)

    def _parse_stats_section(self, target: Tag) -> dict:
        """Parses stats section for strike position and win method information. Returns them as a dictionary.

        Args:
            target (Tag): Tag containing desired information.

        keys:
            StrikePosition: standing, clinch, ground
            WinMethod: ko/tko, dec, sub

        Return
            dict: stats[key] = (value, value_per)
        """
        # TODO - Not super happy with this

        stats = {}

        tags = target.find_all("div", class_="c-stat-3bar__group")
        if tags:
            for tag in tags:
                key = (
                    tag.find("div", class_="c-stat-3bar__label")
                    .get_text()
                    .lower()
                    .strip()
                )

                text_split = (
                    tag.find("div", class_="c-stat-3bar__value").get_text().split("(")
                )
                try:
                    value = int(text_split[0].strip())
                    value_per = int(
                        re.search(r"([0-9]+)", text_split[1].strip())
                        .group()
                        .replace("%", "")
                    )
                except IndexError:
                    value, value_per = 0, 0

                stats[key] = (value, value_per)

        return stats

    def _parse_result_set(self, result_set: ResultSet, dict_keys: list[str]) -> dict:
        """Parses result set for supplied dictionary keys and returns them as a dictionary.

        Args:
            result_set (ResultSet): ResultSet object containing fighters striking and grappling information.
            dict_keys (list[str]): List of dicionary keys to find within result_set.

        Returns:
            dict: Dictionary of requested information from ResultSet.
        """

        stats = {key: 0 for key in dict_keys}

        for result in result_set:
            for target in result.find_all("div", class_="c-stat-compare__group"):
                label = target.find("div", class_="c-stat-compare__label")

                if not label:
                    break

                label = label.get_text().strip()
                for key in dict_keys:
                    if label == key:
                        value = target.find("div", class_="c-stat-compare__number")
                        if value and value.get_text() != "":
                            value = value.get_text().replace("%", "")
                            stats[key] = value.strip()
                            break

        return stats

    def scrape_fighter(self) -> Fighter:
        """Scrapes fighter data from fighter url and returns it as a Fighter object.

        Args:
            fighter_url (str): Fighters ufc page url.

        Returns:
            Fighter: Fighter object containing fighter's data.
        """

        url_response = requests.get(self.fighter_url)

        url_response.raise_for_status()

        self._soup = BeautifulSoup(url_response.content, "html.parser")

        # StrikePosition and Win Method stats - 0 and 1 respectively
        self._stats_section = self._soup.find_all(
            "div", class_="c-stat-3bar c-stat-3bar--no-chart"
        )

        # Striking and Grappling stats - 0 and 1 respectively
        self._stats_targets = self._soup.find_all(
            "div", class_="stats-records stats-records--two-column"
        )

        name = self._get_name()
        nickname = self._get_nickname()

        status = self._get_status()
        ranking, pfp_ranking = self._get_ranking()
        weight_class = self._get_weightclass()

        home_city, home_country = self._get_hometown()

        gym = self._get_gym()
        fighting_style = self._get_fighting_style()

        record_obj = self._get_record_obj()

        physical_stats_obj = self._get_physical_stats_obj()

        win_method_obj = self._get_win_method_obj()

        strike_position_obj = self._get_strike_position_obj()

        strike_target_obj = self._get_strike_target_obj()

        striking_stats = self._get_striking_stats()
        striking_obj = self._create_striking_obj(
            striking_stats, strike_position_obj, strike_target_obj
        )

        grappling_obj = self._get_grappling_obj()

        fighter_data = {
            "fighter_url": self.fighter_url,
            "name": name,
            "nickname": nickname,
            "status": status,
            "ranking": ranking,
            "pfp_ranking": pfp_ranking,
            "weight_class": weight_class,
            "home_city": home_city,
            "home_country": home_country,
            "gym": gym,
            "fighting_style": fighting_style,
            "record": record_obj,
            "win_method": win_method_obj,
            "physical_stats": physical_stats_obj,
            "striking": striking_obj,
            "grappling": grappling_obj,
        }

        fighter_obj = Fighter(**fighter_data)

        return fighter_obj
