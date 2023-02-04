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

        >>> fighter_scraper = FighterScraper(fighter_url)
        >>> fighter = fighter_scraper.scrape_fighter()
        """

        self.fighter_url = set_fighter_url(fighter_url, incorrect_urls)
        self._soup = None
        self._stats_section = None
        self._stats_targets = None

    def _create_soup(self, content: str) -> None:
        """Creates Beautiful soup object from provided content and assigns it to _soup.

        Args:
            content (str): Content to create soup from.
        """

        self._soup = BeautifulSoup(content, "html.parser")

        # StrikePosition and Win Method stats - 0 and 1 respectively
        self._stats_section = self._soup.find_all(
            "div", class_="c-stat-3bar c-stat-3bar--no-chart"
        )

        # Striking and Grappling stats - 0 and 1 respectively
        self._stats_targets = self._soup.find_all(
            "div", class_="stats-records stats-records--two-column"
        )

    def _parse_stat_block(self, target: Tag) -> tuple:
        """Parses stat block for striking and takedown stats, gets accuracy, landed and attempted information. Returns them as a tuple of int values.

        Args:
            target (Tag): Tag containing desired stats.

        Returns:
            tuple: (accuracy, landed, attempted)
        """

        stats = []

        try:
            acc_target = target.find("title")
            accuracy = acc_target.get_text().split()[-1].replace("%", "").strip()
            stats.append(int(accuracy))
        except (IndexError, AttributeError):
            stats.append(0)

        targets = target.find_all("dd", "c-overlap__stats-value")
        if not targets:
            return stats[0], 0, 0

        for target in targets:
            target_text = target.get_text().strip()
            if target_text:
                stats.append(int(target_text))
            else:
                stats.append(0)

        return tuple(stats)

    def _parse_stats_section(self, target: Tag) -> tuple[tuple[int, int]]:
        """Parses stats section for strike position and win method information. Returns them as a a tuple of tuples.

        Args:
            target (Tag): Tag containing desired information.

        Return
            tuple: Tuple of tuples containing value and percentage as ints.
        """

        tags = target.find_all("div", class_="c-stat-3bar__group")
        if not tags:
            return (0, 0), (0, 0), (0, 0)

        stats = []
        for tag in tags:
            text_split = (
                tag.find("div", class_="c-stat-3bar__value").get_text().split(" ")
            )
            try:
                value = int(text_split[0].strip())
                value_per = int(
                    re.search(r"([0-9]+)", text_split[1].strip())
                    .group()
                    .replace("%", "")
                )
            except (IndexError, ValueError):
                value, value_per = 0, 0

            stats.append((value, value_per))

        return tuple(stats)

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
                if label not in dict_keys:
                    continue

                value = target.find("div", class_="c-stat-compare__number")
                if not value:
                    continue

                value_text = value.get_text().replace("%", "").strip()
                if value_text:
                    if "." in value_text:
                        value_text = float(value_text)
                    else:
                        value_text = int(value_text)
                    stats[label] = value_text

        return stats

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
            if label != "Status":
                continue

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
        if not targets:
            return ranking, pfp_ranking

        for target in targets:
            text = target.get_text().strip()
            for keyword in champion_keywords:
                if keyword not in text:
                    continue
                ranking = text
                break

            if "PFP" in text:
                pfp_ranking = text
                continue

            match = re.match(r"^(#[0-9]+)", text)
            if match:
                ranking = match.group()

        return ranking, pfp_ranking

    def _get_weightclass(self) -> str:
        """Gets fighter's weightclass.

        Returns:
            str: Weight class.
        """

        target = self._soup.find("p", class_="hero-profile__division-title")
        if target:
            target_text = target.get_text().strip()
            if target_text:
                return target_text

        return "None"

    def _get_hometown(self) -> tuple:
        """Gets fighter's home city and country. Returns them as a tuple of str values.

        Returns:
            tuple: (city, country)
        """

        city, country = "Unlisted", "Unlisted"

        targets = self._soup.find_all("div", class_="c-bio__field")
        if not targets:
            return city, country

        for target in targets:
            label = target.find("div", class_="c-bio__label").get_text()
            if label != "Hometown":
                continue

            target_text = target.find("div", class_="c-bio__text").get_text()
            if not target_text:
                break

            split_text = target_text.split(", ")
            if len(split_text) > 1:
                city = split_text[0].strip()
                country = split_text[1].strip()
            else:
                country = target_text.strip()
            break

        return city, country

    def _get_gym(self) -> str:
        """Gets the name of fighter's gym.

        Returns:
            str: Gym.
        """

        gym = "Unlisted"

        targets = self._soup.find_all("div", class_="c-bio__field")
        if not targets:
            return gym

        for target in targets:
            label = target.find("div", class_="c-bio__label").get_text()
            if label != "Trains at":
                continue

            target_text = target.find("div", class_="c-bio__text").get_text().strip()
            if not target_text:
                break

            return target_text

        return gym

    def _get_fighting_style(self) -> str:
        """Gets fighter's fighting style.

        Returns:
            str: Fighting style.
        """

        fighting_style = "Unlisted"

        targets = self._soup.find_all("div", class_="c-bio__field")
        if not targets:
            return fighting_style

        for target in targets:
            label = target.find("div", class_="c-bio__label").get_text()
            if label != "Fighting style":
                continue

            target_text = target.find("div", class_="c-bio__text").get_text().strip()
            if not target_text:
                break

            return target_text

        return fighting_style

    def _get_average_fight_time(self) -> str:
        """Gets fighter's average fight time.

        Returns:
            str: Average fight time.
        """

        average_fight_time = "00:00"

        targets = self._soup.find_all(
            "div", class_="c-stat-compare__group c-stat-compare__group-2"
        )
        if not targets:
            return average_fight_time

        for target in targets:
            label = target.find("div", class_="c-stat-compare__label").get_text()
            if label != "Average fight time":
                continue

            target_text = target.find("div", class_="c-stat-compare__number")
            target_text = target_text.get_text().strip()
            if target_text:
                average_fight_time = target_text

        return average_fight_time

    def _get_strike_position_stats(self) -> tuple[tuple[int, int]]:
        """Get strike position information from fighter page and return it a tuple of tuples.

        Indexes:
            0 - Standing
            1 - Clinch
            2 - Ground
        Returns:
            tuple[tuple[int, int]]: Each tuple strike position count and percentage.
        """

        try:
            strike_position_stats_section = self._stats_section[0]

            return self._parse_stats_section(strike_position_stats_section)
        except IndexError:
            return (0, 0), (0, 0), (0, 0)

    def _get_strike_target_stats(self) -> dict:
        """Gets fighters strike target information and returns them as a dictionary.

        Returns:
            dict: Dictionary containing head, body and leg target stats.
        """

        strike_target_stats = {}

        target = self._soup.find("svg", class_="c-stat-body__svg")
        if not target:
            return {"head": (0, 0), "body": (0, 0), "leg": (0, 0)}

        targets = target.find_all("g")
        for target in targets:
            text_targets = target.find_all("text")
            if not text_targets:
                continue

            stats_key = text_targets[2].get_text().strip().lower()
            stats = []
            for i in range(1, -1, -1):
                stat = text_targets[i].get_text().replace("%", "").strip()
                try:
                    stat = int(stat)
                except ValueError:
                    stat = 0
                stats.append(stat)
            strike_target_stats[stats_key] = tuple(stats)

        return strike_target_stats

    def _get_striking_stats(self) -> dict:
        """Get fighter's striking information and return it as a dict.

        Returns:
            dict: Dictionary containing fighter's striking information.
        """

        # if _stats_targets[0] doesn't exist we catch the error
        try:
            accuracy, landed, attempted = self._parse_stat_block(self._stats_targets[0])
        except IndexError:
            accuracy, landed, attempted = 0, 0, 0

        striking_stats_block1 = {
            "striking_accuracy": accuracy,
            "strikes_landed": landed,
            "strikes_attempted": attempted,
        }

        dict_keys = [
            "Sig. Str. Landed",
            "Sig. Str. Absorbed",
            "Sig. Str. Defense",
            "Knockdown Avg",
        ]
        striking_results = self._parse_result_set(self._stats_targets, dict_keys)
        striking_stats_block2 = {
            "strikes_average": striking_results["Sig. Str. Landed"],
            "strikes_absorbed_average": striking_results["Sig. Str. Absorbed"],
            "striking_defence": striking_results["Sig. Str. Defense"],
            "knockdown_average": striking_results["Knockdown Avg"],
        }

        striking_stats = striking_stats_block1 | striking_stats_block2

        return striking_stats

    def _get_record_stats(self) -> tuple[int, int, int]:
        """Get record information from fighter page and returns it as a tuple.

        Returns:
            tuple: (win, loss, draw)
        """

        win, loss, draw = 0, 0, 0

        target = self._soup.find("p", class_="hero-profile__division-body")

        try:
            text = target.get_text().strip().split()[0]
            return tuple(int(text) for text in text.split("-"))
        except (IndexError, AttributeError):
            return win, loss, draw

    def _get_win_method_stats(self) -> tuple[tuple[int, int]]:
        """Get win method information from fighter page and return it a tuple of tuples.

        Indexes:
            0 - Knockout
            1 - Decision
            2 - Submission
        Returns:
            tuple[tuple[int, int]]: Each tuple win method count and percentage.
        """

        try:
            win_method_stats_section = self._stats_section[1]

            return self._parse_stats_section(win_method_stats_section)
        except IndexError:
            return (0, 0), (0, 0), (0, 0)

    def _get_physical_stats(self) -> dict:
        """Gets fighters physical stats and returns them as a dictionary.

        Returns:
            dict: Dictionary containing fighters age, height, weight, reach and leg_reach.
        """

        field_names = ["Age", "Height", "Weight", "Reach", "Leg reach"]
        targets = self._soup.find_all("div", class_="c-bio__field")

        physical_stats = {key.lower().replace(" ", "_"): 0 for key in field_names}
        for target in targets:
            label = target.find("div", class_="c-bio__label").get_text()
            if label not in field_names:
                continue

            key = label.lower().replace(" ", "_")
            field_value = target.find("div", class_="c-bio__text").get_text().strip()
            if field_value:
                if label == "Age":
                    physical_stats[key] = int(field_value)
                    continue
                physical_stats[key] = float(field_value)

        return physical_stats

    def _get_grappling_stats(self) -> dict:
        """Get fighter's grappling information and return it as a dict.

        Returns:
            dict: Dictionary containing fighter's grappling information.
        """

        # if _stats_targets[1] doesn't exist we catch the error
        try:
            accuracy, landed, attempted = self._parse_stat_block(self._stats_targets[1])
        except IndexError:
            accuracy, landed, attempted, = (
                0,
                0,
                0,
            )

        grappling_stats_block1 = {
            "takedown_accuracy": accuracy,
            "takedowns_landed": landed,
            "takedowns_attempted": attempted,
        }

        dict_keys = ["Takedown avg", "Takedown Defense", "Submission avg"]
        grappling_results = self._parse_result_set(self._stats_targets, dict_keys)
        grappling_stats_block2 = {
            "takedowns_average": grappling_results["Takedown avg"],
            "takedown_defence": grappling_results["Takedown Defense"],
            "submission_average": grappling_results["Submission avg"],
        }

        grappling_stats = grappling_stats_block1 | grappling_stats_block2

        return grappling_stats

    # Object related methods
    def _get_record_obj(self) -> Record:
        """Get record information from fighter page and return it as a Record object.

        Returns:
            Record: Record object containing fighter's record information.
        """

        win, loss, draw = self._get_record_stats()

        record = {"win": win, "loss": loss, "draw": draw}

        return Record(**record)

    def _get_win_method_obj(self) -> WinMethod:
        """Get win method information and return it as a WinMethod object.

        Returns:
            WinMethod: WinMethod object containing fighter's win method information.
        """

        average_fight_time = self._get_average_fight_time()
        win_method_stats = self._get_win_method_stats()

        knockout, knockout_per = win_method_stats[0]
        decision, decision_per = win_method_stats[1]
        submission, submission_per = win_method_stats[2]

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

        physical_stats = self._get_physical_stats()

        return PhysicalStats(**physical_stats)

    def _get_strike_position_obj(self) -> StrikePosition:
        """Get fighter's strike position information and return it as a StrikePosition object.

        Returns:
            StrikePosition: StrikePosition object containing fighter's strike position information.
        """

        strike_position_stats = self._get_strike_position_stats()

        standing, standing_per = strike_position_stats[0]
        clinch, clinch_per = strike_position_stats[1]
        ground, ground_per = strike_position_stats[2]

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

        strike_target_stats = self._get_strike_target_stats()

        head, head_per = strike_target_stats["head"]
        body, body_per = strike_target_stats["body"]
        leg, leg_per = strike_target_stats["leg"]
        strike_target_stats = {
            "head": head,
            "head_per": head_per,
            "body": body,
            "body_per": body_per,
            "leg": leg,
            "leg_per": leg_per,
        }

        return StrikeTarget(**strike_target_stats)

    def _get_striking_obj(self) -> Striking:
        """Gets fighter's striking, strike position and striking target information and returns them as a Striking object.

        Returns:
            Striking: Striking object containing all of the fighter's striking, strike position and striking target information.
        """

        strike_position_obj = self._get_strike_position_obj()
        strike_target_obj = self._get_strike_target_obj()
        striking_stats = self._get_striking_stats()

        stats = striking_stats | {
            "strike_position": strike_position_obj,
            "strike_target": strike_target_obj,
        }

        return Striking(**stats)

    def _get_grappling_obj(self) -> Grappling:
        """Get fighter's grappling information and return it as a Grappling object.

        Returns:
            Grappling: Grappling object containing fighter's grappling information.
        """

        grappling_stats = self._get_grappling_stats()

        return Grappling(**grappling_stats)

    def scrape_fighter(self) -> Fighter:
        """Scrapes fighter data from fighter url and returns it as a Fighter object.

        Args:
            fighter_url (str): Fighters ufc page url.

        Returns:
            Fighter: Fighter object containing fighter's data.
        """

        url_response = requests.get(self.fighter_url)

        url_response.raise_for_status()

        self._create_soup(url_response.content)

        ranking, pfp_ranking = self._get_ranking()
        home_city, home_country = self._get_hometown()

        fighter_data = {
            "fighter_url": self.fighter_url,
            "name": self._get_name(),
            "nickname": self._get_nickname(),
            "status": self._get_status(),
            "ranking": ranking,
            "pfp_ranking": pfp_ranking,
            "weight_class": self._get_weightclass(),
            "home_city": home_city,
            "home_country": home_country,
            "gym": self._get_gym(),
            "fighting_style": self._get_fighting_style(),
            "record": self._get_record_obj(),
            "win_method": self._get_win_method_obj(),
            "physical_stats": self._get_physical_stats_obj(),
            "striking": self._get_striking_obj(),
            "grappling": self._get_grappling_obj(),
        }

        fighter_obj = Fighter(**fighter_data)

        return fighter_obj
