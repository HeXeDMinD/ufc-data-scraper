import requests
import re

from bs4 import BeautifulSoup, element, ResultSet
from unidecode import unidecode

from ufc_data_scraper.custom_objects.fighter import *


class _FighterScraper:
    def __init__(self, fighter_url: str) -> None:
        """Scrapes a fighter page from ufc.com"""
        self._soup = None
        
        self._incorrect_urls = self._get_incorrect_urls()
        
        self._fighter_url = self._set_fighter_url(fighter_url)
        
    def _get_incorrect_urls(self):
        google_web_app = f"https://script.google.com/macros/s/AKfycbzYJ7dC6Xg4MSKVg7XWI5yz32Gc97ePNQnRkPs9vDz21KRD7IjFnF938aUlsouKrRy5/exec"
        
        site_response = requests.get(google_web_app)
        
        if site_response.status_code != 200:
            return None
        
        return {incorrect.lower(): correct.lower() for incorrect, correct in site_response.json().items()}
    
    def _set_fighter_url(self, fighter_url: str) -> str:
        fighter_url = fighter_url.lower()
        incorrect_urls = self._get_incorrect_urls()

        fighter_url = fighter_url.replace("https", "http")
        
        banned_url_chars = ["--", "'"]
        for banned_char in banned_url_chars:
            if banned_char in fighter_url:
                fighter_url = fighter_url.replace(banned_char, "")

        try:
            fighter_url = incorrect_urls[fighter_url]
        except (KeyError, TypeError):
            fighter_url = fighter_url

        return fighter_url
    
    def _get_name(self) -> str:
        """Returns fighter name."""

        name = ""

        target = self._soup.find("h1", class_="hero-profile__name")
        if target:
            name = target.get_text()

        name = name.replace("-", " ")
        return unidecode(name.strip())

    def _get_nickname(self) -> str:
        """Returns nickname.

        Returns:
            str: nickname
        """

        nickname = ""

        target = self._soup.find("p", class_="hero-profile__nickname")
        if target:
            nickname = target.get_text().strip()
            nickname = nickname.replace('"', "")

        return nickname

    def _get_status(self) -> str:
        """Returns fighting status.

        Returns:
            str: status
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
        """Returns fighters division and pound for pound ranking.

        Returns:
            tuple: (ranking, pfp_ranking)
        """

        ranking, pfp_ranking = "Unranked", "Unranked"

        targets = self._soup.find_all("p", class_="hero-profile__tag")
        for target in targets:
            text = target.get_text().strip()
            if "Interim" in text or "Champion" in text:
                ranking = text

            match = re.match(r"^(#[0-9]+)", text)
            if match:
                if "PFP" in text:
                    pfp_ranking = f"{match.group()} PFP"
                else:
                    ranking = match.group()

        return (ranking, pfp_ranking)

    def _get_weightclass(self) -> str:
        """Returns fighters weightclass.

        Returns:
            str: weightclass
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
        """Returns home city and country

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
        """Returns fighters gym.

        Returns:
            str: gym
        """

        gym = "Unlisted"

        targets = self._soup.find_all("div", class_="c-bio__field")
        for target in targets:
            label = target.find("div", class_="c-bio__label").get_text()
            if label == "Trains at":
                gym = target.find("div", class_="c-bio__text").get_text().strip()
                break

        return gym

    def _get_fighting_style(self) -> str:
        """Returns fighting style

        Returns:
            str: fighting_style
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
        # TODO - Documentation

        win, loss, draw = 0, 0, 0

        target = self._soup.find("p", class_="hero-profile__division-body")
        if target:
            text = target.get_text().strip().split()[0]
            win, loss, draw = text.split("-")

        record = {"win": int(win), "loss": int(loss), "draw": int(draw)}

        return Record(**record)

    def _get_average_fight_time(self) -> str:
        """Returns average fight time.

        Returns:
            str: average_fight_time
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

    def _get_win_method_obj(self, stats_section: ResultSet) -> WinMethod:
        # TODO - Documentation
        average_fight_time = self._get_average_fight_time()

        try:
            win_method_stats = self._parse_stats_section(stats_section)
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
        # TODO - Documentation

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
                    field_value = target.find("div", class_="c-bio__text").get_text().strip()
                    if field_value:
                        if name != "Age":
                            physical_stats[keys[i]] = float(field_value)
                        else:
                            physical_stats[keys[i]] = int(field_value)
        
        return PhysicalStats(**physical_stats)

    def _get_strike_position_obj(self, stats_section: ResultSet) -> StrikePosition:
        try:
            position_stats = self._parse_stats_section(stats_section)
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
        # TODO - Documentation

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

    def _get_striking_stats(self, stats_targets: ResultSet) -> dict:
        # TODO - Documentation
        try:
            (
                striking_accuracy,
                strikes_landed,
                strikes_attempted,
            ) = self._parse_stat_block(stats_targets[0])
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
        striking_results = self._parse_result_set(stats_targets, dict_keys)

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
        # TODO - Documentation
        stats = striking_stats | {
            "strike_position": strike_position,
            "strike_target": strike_target,
        }
        return Striking(**stats)

    def _get_grappling_obj(self, stats_targets: ResultSet) -> Grappling:
        # TODO - Documentation
        try:
            (
                takedown_accuracy,
                takedowns_landed,
                takedowns_attempted,
            ) = self._parse_stat_block(stats_targets[1])
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
        grappling_results = self._parse_result_set(stats_targets, dict_keys)
        grappling_stats_block2 = {
            "takedowns_average": float(grappling_results["Takedown avg"]),
            "takedown_defence": int(grappling_results["Takedown Defense"]),
            "submission_average": float(grappling_results["Submission avg"]),
        }

        grappling_stats = grappling_stats_block1 | grappling_stats_block2

        return Grappling(**grappling_stats)

    def _parse_stat_block(self, target: element.Tag) -> tuple:
        """Parses stat block, used for striking and takedown stats.

        Returns:
            tuple: (accuracy, landed, attempted)
        """

        accuracy, landed, attempted = 0, 0, 0

        acc_target = target.find("title")
        if acc_target:
            try:
                accuracy = int(acc_target.get_text().split()[-1].replace("%", "").strip())
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

    def _parse_stats_section(self, target: element.Tag) -> dict:
        """Parses stats section, used for strike position and win method stats.

        Returns:
            dict: stats[key] = [value, value_per]

            keys:
                StrikePosition: standing, clinch, ground
                WinMethod: ko/tko, dec, sub
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

                stats[key] = [value, value_per]

        return stats

    def _parse_result_set(self, result_set: element.ResultSet, dict_keys: list) -> dict:
        """Parses result set."""

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

    def _scrape_fighter(self) -> Fighter:
        """Scrapes fighter page.

        Returns:
            Fighter: Returns fighter object.
        """

        url_response = requests.get(self._fighter_url)

        url_response.raise_for_status()

        self._soup = BeautifulSoup(url_response.content, "html.parser")

        # StrikePosition and Win Method stats - 0 and 1 respectively
        stats_section = self._soup.find_all(
            "div", class_="c-stat-3bar c-stat-3bar--no-chart"
        )

        # Striking and Grappling stats - 0 and 1 respectively
        stats_targets = self._soup.find_all(
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

        win_method_obj = self._get_win_method_obj(stats_section[1])

        strike_position_obj = self._get_strike_position_obj(stats_section[0])
        strike_target_obj = self._get_strike_target_obj()

        striking_stats = self._get_striking_stats(stats_targets)
        striking_obj = self._create_striking_obj(
            striking_stats, strike_position_obj, strike_target_obj
        )

        grappling_obj = self._get_grappling_obj(stats_targets)

        fighter_data = {
            "fighter_url": self._fighter_url,
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
