import pytest

from ufc_data_scraper.scraper import EventScraper

from ufc_data_scraper.exceptions import MissingEventData

from ufc_data_scraper.data_models.event import *
from ufc_data_scraper.data_models.fighter import Fighter

from ufc_data_scraper.utils import convert_date


class TestEventScraper:
    test_fmid = 1124  # Completed Event
    test_url = "https://www.ufc.com/event/ufc-282"
    test_event_scraper = EventScraper(test_fmid, test_url)
    test_event = test_event_scraper.scrape_event()

    test_fight_1 = {
        "FightId": 10227,
        "FightOrder": 5,
        "Status": "Final",
        "CardSegment": "Main",
        "CardSegmentStartTime": "2022-12-11T03:00Z",
        "CardSegmentBroadcaster": "PPV",
        "Fighters": [
            {
                "FighterId": 3130,
                "MMAId": 129655,
                "Name": {
                    "FirstName": "Bryce",
                    "LastName": "Mitchell",
                    "NickName": "Thug Nasty",
                },
                "Born": {
                    "City": "Texarkana",
                    "State": "Texas",
                    "Country": "USA",
                    "TriCode": "USA",
                },
                "FightingOutOf": {
                    "City": "Searcy",
                    "State": "Arkansas",
                    "Country": "USA",
                    "TriCode": "USA",
                },
                "Record": {"Wins": 15, "Losses": 2, "Draws": 0, "NoContests": 0},
                "DOB": "1994-10-04",
                "Age": 28,
                "Stance": "Southpaw",
                "Weight": 145.0,
                "Height": 70.0,
                "Reach": 70.0,
                "UFCLink": "http://www.ufc.com/athlete/Bryce-Mitchell",
                "WeightClasses": [
                    {
                        "WeightClassId": 6,
                        "WeightClassOrder": 1,
                        "Description": "Featherweight",
                        "Abbreviation": "FTW",
                    }
                ],
                "Corner": "Red",
                "WeighIn": 146.0,
                "Outcome": {"OutcomeId": 2, "Outcome": "Loss"},
                "KOOfTheNight": False,
                "SubmissionOfTheNight": False,
                "PerformanceOfTheNight": False,
            },
            {
                "FighterId": 3605,
                "MMAId": 163860,
                "Name": {
                    "FirstName": "Ilia",
                    "LastName": "Topuria",
                    "NickName": "El Matador",
                },
                "Born": {
                    "City": "Halle Westfalen",
                    "State": "North Rhine-Westphalia",
                    "Country": "Germany",
                    "TriCode": "GER",
                },
                "FightingOutOf": {
                    "City": "Alicante",
                    "State": "Alacant",
                    "Country": "Spain",
                    "TriCode": "ESP",
                },
                "Record": {"Wins": 13, "Losses": 0, "Draws": 0, "NoContests": 0},
                "DOB": "1997-01-21",
                "Age": 25,
                "Stance": "Orthodox",
                "Weight": 145.0,
                "Height": 67.0,
                "Reach": 69.0,
                "UFCLink": "http://www.ufc.com/athlete/Ilia-Topuria",
                "WeightClasses": [
                    {
                        "WeightClassId": 6,
                        "WeightClassOrder": 1,
                        "Description": "Featherweight",
                        "Abbreviation": "FTW",
                    }
                ],
                "Corner": "Blue",
                "WeighIn": 146.0,
                "Outcome": {"OutcomeId": 1, "Outcome": "Win"},
                "KOOfTheNight": False,
                "SubmissionOfTheNight": False,
                "PerformanceOfTheNight": True,
            },
        ],
        "Result": {
            "Method": "Submission",
            "EndingRound": 2,
            "EndingTime": "3:10",
            "EndingStrike": None,
            "EndingTarget": None,
            "EndingPosition": "From Side Control",
            "EndingSubmission": "Arm Triangle",
            "EndingNotes": None,
            "FightOfTheNight": False,
            "FightScores": [],
        },
        "WeightClass": {
            "WeightClassId": 6,
            "CatchWeight": None,
            "Weight": "136-145",
            "Description": "Featherweight",
            "Abbreviation": "FTW",
        },
        "Accolades": [],
        "Referee": {"RefereeId": 31, "FirstName": "Marc", "LastName": "Goddard"},
        "RuleSet": {"PossibleRounds": 3, "Description": "3 Rnd (5-5-5)"},
        "FightNightTracking": [],
    }

    test_fight_2 = {
        "FightId": 10211,
        "FightOrder": 1,
        "Status": "Final",
        "CardSegment": "Main",
        "CardSegmentStartTime": "2022-12-11T03:00Z",
        "CardSegmentBroadcaster": "PPV",
        "Fighters": [
            {
                "FighterId": 2300,
                "MMAId": 140580,
                "Name": {
                    "FirstName": "Jan",
                    "LastName": "Blachowicz",
                    "NickName": None,
                },
                "Born": {
                    "City": "Cieszyn",
                    "State": None,
                    "Country": "Poland",
                    "TriCode": "POL",
                },
                "FightingOutOf": {
                    "City": "Warsaw",
                    "State": None,
                    "Country": "Poland",
                    "TriCode": "POL",
                },
                "Record": {"Wins": 29, "Losses": 9, "Draws": 1, "NoContests": 0},
                "DOB": "1983-02-24",
                "Age": 39,
                "Stance": "Orthodox",
                "Weight": 205.0,
                "Height": 74.0,
                "Reach": 78.0,
                "UFCLink": "http://www.ufc.com/athlete/Jan-Blachowicz",
                "WeightClasses": [
                    {
                        "WeightClassId": 2,
                        "WeightClassOrder": 1,
                        "Description": "Light Heavyweight",
                        "Abbreviation": "LHW",
                    }
                ],
                "Corner": "Red",
                "WeighIn": 204.5,
                "Outcome": {"OutcomeId": 3, "Outcome": "Draw"},
                "KOOfTheNight": False,
                "SubmissionOfTheNight": False,
                "PerformanceOfTheNight": False,
            },
            {
                "FighterId": 3046,
                "MMAId": 155703,
                "Name": {
                    "FirstName": "Magomed",
                    "LastName": "Ankalaev",
                    "NickName": None,
                },
                "Born": {
                    "City": None,
                    "State": "Dagestan",
                    "Country": "Russia",
                    "TriCode": "RUS",
                },
                "FightingOutOf": {
                    "City": "Makhachkala",
                    "State": "Dagestan",
                    "Country": "Russia",
                    "TriCode": "RUS",
                },
                "Record": {"Wins": 18, "Losses": 1, "Draws": 1, "NoContests": 0},
                "DOB": "1992-06-02",
                "Age": 30,
                "Stance": "Orthodox",
                "Weight": 205.0,
                "Height": 75.0,
                "Reach": 75.0,
                "UFCLink": "http://www.ufc.com/athlete/Magomed-Ankalaev",
                "WeightClasses": [
                    {
                        "WeightClassId": 2,
                        "WeightClassOrder": 1,
                        "Description": "Light Heavyweight",
                        "Abbreviation": "LHW",
                    }
                ],
                "Corner": "Blue",
                "WeighIn": 205.0,
                "Outcome": {"OutcomeId": 3, "Outcome": "Draw"},
                "KOOfTheNight": False,
                "SubmissionOfTheNight": False,
                "PerformanceOfTheNight": False,
            },
        ],
        "Result": {
            "Method": "Decision - Split",
            "EndingRound": 5,
            "EndingTime": "5:00",
            "EndingStrike": None,
            "EndingTarget": None,
            "EndingPosition": None,
            "EndingSubmission": None,
            "EndingNotes": None,
            "FightOfTheNight": False,
            "FightScores": [
                {
                    "JudgeId": 228,
                    "JudgeFirstName": "Mike",
                    "JudgeLastName": "Bell",
                    "Fighters": [
                        {"FighterId": 2300, "Score": 48},
                        {"FighterId": 3046, "Score": 47},
                    ],
                },
                {
                    "JudgeId": 200,
                    "JudgeFirstName": "Derek",
                    "JudgeLastName": "Cleary",
                    "Fighters": [
                        {"FighterId": 2300, "Score": 46},
                        {"FighterId": 3046, "Score": 48},
                    ],
                },
                {
                    "JudgeId": 14,
                    "JudgeFirstName": "Sal",
                    "JudgeLastName": "D'amato",
                    "Fighters": [
                        {"FighterId": 2300, "Score": 47},
                        {"FighterId": 3046, "Score": 47},
                    ],
                },
            ],
        },
        "WeightClass": {
            "WeightClassId": 2,
            "CatchWeight": None,
            "Weight": "186-205",
            "Description": "Light Heavyweight",
            "Abbreviation": "LHW",
        },
        "Accolades": [{"Type": "Belt", "Name": "UFC Light Heavyweight Title"}],
        "Referee": {"RefereeId": 31, "FirstName": "John", "LastName": "McCarthy"},
        "RuleSet": {"PossibleRounds": 5, "Description": "5 Rnd (5-5-5-5-5)"},
    }

    test_fighter = test_fight_1.get("Fighters")[0]

    # _get_event_data
    def test_get_event_data(self):
        actual = self.test_event_scraper._event_data
        expected = 1124

        assert len(actual) > 0
        assert actual["EventId"] == expected

    # _get_location_obj
    def test_get_location_obj(self):
        expected = {
            "venue": "T-Mobile Arena",
            "city": "Las Vegas",
            "country": "USA",
            "tricode": "USA",
        }

        actual = self.test_event.location

        assert isinstance(actual, Location)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    # _get_fighter_name
    def test_get_fighter_name(self):
        expected = "Bryce Mitchell"
        actual = self.test_event_scraper._get_fighter_name(self.test_fighter)

        assert actual == expected

    def test_get_fighter_name_missing_first_name(self):
        test_fighter = {"Name": {"FirstName": "", "LastName": "Mitchell"}}
        expected = "Mitchell"
        actual = self.test_event_scraper._get_fighter_name(test_fighter)

        assert actual == expected

    def test_get_fighter_name_missing_last_name(self):
        test_fighter = {"Name": {"FirstName": "Bryce", "LastName": ""}}
        expected = "Bryce"
        actual = self.test_event_scraper._get_fighter_name(test_fighter)

        assert actual == expected

    def test_get_fighter_name_no_name_data(self):
        test_fighter = {}
        actual = self.test_event_scraper._get_fighter_name(test_fighter)

        assert actual is None

    # _get_fighter_url
    def test_get_fighter_url(self):
        expected = "http://www.ufc.com/athlete/bryce-mitchell"
        actual = self.test_event_scraper._get_fighter_url(self.test_fighter)

        assert actual == expected

    def test_get_fighter_url_missing_url(self):
        test_fighter = {
            "UFCLink": None,
            "Name": {"FirstName": "Bryce", "LastName": "Mitchell"},
        }
        expected = "http://www.ufc.com/athlete/bryce-mitchell"
        actual = self.test_event_scraper._get_fighter_url(test_fighter)

        assert actual == expected

    def test_get_fighter_url_no_data(self):
        test_fighter = {}
        actual = self.test_event_scraper._get_fighter_url(test_fighter)

        assert actual is None

    def test_get_fighter_url_missing_both_names(self):
        test_fighter = {
            "UFCLink": None,
            "Name": {"FirstName": "", "LastName": ""},
        }
        actual = self.test_event_scraper._get_fighter_url(test_fighter)

        assert actual is None

    # _get_booked_fighter_urls
    def test_get_booked_fighter_urls(self):
        expected = [
            "http://www.ufc.com/athlete/jan-blachowicz",
            "http://www.ufc.com/athlete/magomed-ankalaev",
            "http://www.ufc.com/athlete/paddy-pimblett",
            "http://www.ufc.com/athlete/jared-gordon",
            "http://www.ufc.com/athlete/santiago-ponzinibbio",
            "http://www.ufc.com/athlete/alex-morono",
            "http://www.ufc.com/athlete/darren-till",
            "http://www.ufc.com/athlete/dricus-du-plessis",
            "http://www.ufc.com/athlete/bryce-mitchell",
            "http://www.ufc.com/athlete/ilia-topuria",
            "http://www.ufc.com/athlete/raul-rosas-jr",
            "http://www.ufc.com/athlete/jay-perrin",
            "http://www.ufc.com/athlete/jairzinho-rozenstruik",
            "http://www.ufc.com/athlete/chris-daukaus",
            "http://www.ufc.com/athlete/edmen-shahbazyan",
            "http://www.ufc.com/athlete/dalcha-lungiambula",
            "http://www.ufc.com/athlete/chris-curtis",
            "http://www.ufc.com/athlete/joaquin-buckley",
            "http://www.ufc.com/athlete/billy-quarantillo",
            "http://www.ufc.com/athlete/alexander-hernandez",
            "http://www.ufc.com/athlete/tj-brown",
            "http://www.ufc.com/athlete/erik-silva",
            "http://www.ufc.com/athlete/cameron-saaiman",
            "http://www.ufc.com/athlete/steven-koslow",
        ]
        actual = self.test_event_scraper._fighter_urls

        assert actual.sort() == expected.sort()

    # _get_fighter_obj
    def test_get_fighter_obj(self):
        test_url = "http://www.ufc.com/athlete/jan-blachowicz"
        actual = self.test_event_scraper._get_fighter_obj(test_url)

        assert isinstance(actual, Fighter)
        assert actual.fighter_url == test_url

    def test_get_fighter_obj_invalid_url(self):
        test_url = "http://www.google.com"
        actual = self.test_event_scraper._get_fighter_obj(test_url)

        assert actual is None

    # _scrape_fighters
    def test_scraped_fighters(self):
        actual = self.test_event_scraper._scraped_fighters

        assert len(self.test_event_scraper._fighter_urls) == len(actual)

        for fighter_url, fighter_obj in actual.items():
            assert fighter_obj.fighter_url == fighter_url

    # _get_fighters_stats
    def test_get_fighters_stats(self):
        expected = {
            "fighter": None,
            "fighter_url": "http://www.ufc.com/athlete/jan-blachowicz",
            "corner": "Red",
            "weigh_in": 204.5,
            "outcome": "Draw",
            "ko_of_the_night": False,
            "submission_of_the_night": False,
            "performance_of_the_night": False,
        }

        actual = self.test_event.card_segments[0].fights[0].fighters_stats[0]

        assert isinstance(actual, FighterStats)

        for key, value in expected.items():
            if key == "fighter":
                assert isinstance(actual.__dict__[key], Fighter)
                continue
            assert actual.__dict__[key] == value

    def test_get_fighters_stats_test_fighter(self):
        expected = {
            "fighter": None,
            "fighter_url": "http://www.ufc.com/athlete/bryce-mitchell",
            "corner": "Red",
            "weigh_in": 146.0,
            "outcome": "Loss",
            "ko_of_the_night": False,
            "submission_of_the_night": False,
            "performance_of_the_night": False,
        }
        actual = self.test_event_scraper._get_fighters_stats(self.test_fighter)

        assert isinstance(actual, FighterStats)

        for key, value in expected.items():
            if key == "fighter":
                assert isinstance(actual.__dict__[key], Fighter)
                continue
            assert actual.__dict__[key] == value

    def test_get_fighters_stats_no_fighter_url(self):
        expected = {
            "fighter": None,
            "fighter_url": "http://www.ufc.com/athlete/bryce-mitchell",
            "corner": "Red",
            "weigh_in": 146.0,
            "outcome": "Loss",
            "ko_of_the_night": False,
            "submission_of_the_night": False,
            "performance_of_the_night": False,
        }
        test_fighter = dict(self.test_fighter)
        test_fighter["UFCLink"] = None
        actual = self.test_event_scraper._get_fighters_stats(test_fighter)

        assert isinstance(actual, FighterStats)

        for key, value in expected.items():
            if key == "fighter":
                assert isinstance(actual.__dict__[key], Fighter)
                continue
            assert actual.__dict__[key] == value

    def test_get_fighters_stats_no_fighter_url_no_name(self):
        expected = {
            "fighter": None,
            "fighter_url": "http://www.ufc.com/athlete/dallas-mitchell",
            "corner": "Red",
            "weigh_in": 146.0,
            "outcome": "Loss",
            "ko_of_the_night": False,
            "submission_of_the_night": False,
            "performance_of_the_night": False,
        }

        test_fighter = dict(self.test_fighter)
        test_fighter["UFCLink"] = None
        test_fighter["Name"]["FirstName"] = "Dallas"
        actual = self.test_event_scraper._get_fighters_stats(test_fighter)

        assert isinstance(actual, FighterStats)

        for key, value in expected.items():
            if key == "fighter":
                assert actual.__dict__[key] is None
                continue
            assert actual.__dict__[key] == value

    # _parse_fighters
    def test_parse_fighters(self):
        expected = ("Bryce Mitchell", "Ilia Topuria")
        actual = self.test_event_scraper._parse_fighters(self.test_fight_1)

        assert len(actual) == 2

        for i, name in enumerate(expected):
            assert isinstance(actual[i].fighter, Fighter)
            assert actual[i].fighter.name == name

    # _get_fight_scores
    def test_get_fight_scores_no_scores(self):
        expected = []
        actual = self.test_event_scraper._get_fight_scores(self.test_fight_1)

        assert actual == expected

    def test_get_fight_score_has_scores(self):
        actual = self.test_event_scraper._get_fight_scores(self.test_fight_2)

        assert len(actual) > 0

        for fight_score in actual:
            assert isinstance(fight_score, FightScore)

    # _get_referee_name
    def test_get_referee_name_fight_1(self):
        expected = "Marc Goddard"
        actual = self.test_event_scraper._get_referee_name(self.test_fight_1)

        assert actual == expected

    def test_get_referee_name_fight_2(self):
        expected = "John McCarthy"
        actual = self.test_event_scraper._get_referee_name(self.test_fight_2)

        assert actual == expected

    # _get_result_obj
    def test_get_result_test_fight_1(self):
        expected = {
            "method": "Submission",
            "ending_round": 2,
            "ending_time": "3:10",
            "ending_strike": "",
            "ending_target": "",
            "ending_position": "From Side Control",
            "ending_submission": "Arm Triangle",
            "ending_notes": "",
            "fight_of_the_night": False,
        }

        actual = self.test_event_scraper._get_result_obj(self.test_fight_1)

        assert isinstance(actual, Result)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    def test_get_result_test_fight_2(self):
        expected = {
            "method": "Decision - Split",
            "ending_round": 5,
            "ending_time": "5:00",
            "ending_strike": "",
            "ending_target": "",
            "ending_position": "",
            "ending_submission": "",
            "ending_notes": "",
            "fight_of_the_night": False,
        }
        actual = self.test_event_scraper._get_result_obj(self.test_fight_2)

        assert isinstance(actual, Result)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    # _get_weight_class_obj
    def test_get_weight_class_obj_fight_1(self):
        expected = {
            "description": "Featherweight",
            "abbreviation": "FTW",
            "weight": "136-145",
        }

        actual = self.test_event_scraper._get_weight_class_obj(self.test_fight_1)

        assert isinstance(actual, WeightClass)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    def test_get_weight_class_obj_fight_2(self):
        expected = {
            "description": "Light Heavyweight",
            "abbreviation": "LHW",
            "weight": "186-205",
        }
        actual = self.test_event_scraper._get_weight_class_obj(self.test_fight_2)

        assert isinstance(actual, WeightClass)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    # _get_accolades_obj
    def test_get_accolades_obj_no_accolades(self):
        actual = self.test_event_scraper._get_accolades_obj(self.test_fight_1)

        assert actual is None

    def test_get_accolades_obj_has_accolades(self):
        expected = {"description": "UFC Light Heavyweight Title", "type": "Belt"}

        actual = self.test_event_scraper._get_accolades_obj(self.test_fight_2)

        assert isinstance(actual, Accolade)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    # _get_rule_set_obj
    def test_get_rule_set_obj_fight_1(self):
        expected = {"description": "3 Rnd (5-5-5)", "possible_rounds": 3}
        actual = self.test_event_scraper._get_rule_set_obj(self.test_fight_1)

        assert isinstance(actual, RuleSet)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    def test_get_rule_set_obj_fight_2(self):
        expected = {"description": "5 Rnd (5-5-5-5-5)", "possible_rounds": 5}
        actual = self.test_event_scraper._get_rule_set_obj(self.test_fight_2)

        assert isinstance(actual, RuleSet)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    # _parse_fight
    def test_parse_fight(self):
        actual = self.test_event_scraper._parse_fight(self.test_fight_2)

        assert isinstance(actual, Fight)

        attributes_to_check = {
            FighterStats: actual.fighters_stats,
            Result: actual.result,
            WeightClass: actual.weight_class,
            Accolade: actual.accolades,
            RuleSet: actual.rule_set,
            FightScore: actual.fight_scores,
        }

        for obj_type, attribute in attributes_to_check.items():
            if isinstance(attribute, list):
                for item in attribute:
                    assert isinstance(item, obj_type)
                continue
            assert isinstance(attribute, obj_type)

    # _get_card_segments
    def test_get_card_segments(self):
        expected = ("Main", "Prelims", "Early Prelims")
        actual = self.test_event.card_segments

        assert isinstance(actual, list)
        assert len(actual) == 3

        for i, segment in enumerate(actual):
            assert isinstance(segment, CardSegment)
            assert segment.name == expected[i]

    def test_get_card_segments_start_times(self):
        expected = ("2022-12-11T03:00Z", "2022-12-11T01:00Z", "2022-12-10T23:30Z")
        actual = self.test_event.card_segments

        for i, segment in enumerate(actual):
            assert segment.start_time == convert_date(expected[i])

    def test_get_card_segments_broadcasters(self):
        expected = ("PPV", "ESPN 2", "UFC Fight Pass")
        actual = self.test_event.card_segments

        for i, segment in enumerate(actual):
            assert segment.broadcaster == expected[i]

    # scrape_event
    def test_scrape_event(self):
        expected = {
            "fmid": self.test_fmid,
            "event_url": self.test_url,
            "name": "UFC 282: Blachowicz vs. Ankalaev",
            "date": convert_date("2022-12-10T23:30Z"),
            "status": "Final",
        }
        actual = self.test_event

        assert isinstance(actual, Event)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    def test_scrape_invalid_event(self):
        invalid_fmid = 9999
        invalid_url = "http://madeup.com/event/madeup-event"

        test_event_scraper = EventScraper(invalid_fmid, invalid_url)

        with pytest.raises(MissingEventData, match=r"Could not retrieve event data."):
            test_event_scraper.scrape_event()
