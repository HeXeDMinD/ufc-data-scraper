from datetime import datetime

from ufc_data_scraper.scraper.fighter_scraper import FighterScraper, set_fighter_url

from ufc_data_scraper.utils import get_incorrect_urls

from ufc_data_scraper.data_models.fighter import *

def _fighters_actual_age(birth_year: int):
    return datetime.now().year - birth_year

class TestFighterScraper:
    incorrect_fighter_urls = get_incorrect_urls()

    scraper_ali_alqaisi = FighterScraper(
        "https://www.ufc.com/athlete/ali-alqaisi", incorrect_fighter_urls
    )
    test_fighter = scraper_ali_alqaisi.scrape_fighter()
    test_fighter_age = _fighters_actual_age(1991)

    # Contains some data missing from scraper_ali_alqaisi
    scraper_joseph_benavidez = FighterScraper(
        "https://www.ufc.com/athlete/joseph-benavidez", incorrect_fighter_urls
    )
    scraper_joseph_benavidez.scrape_fighter()

    # Dummy fighter scraper to test methods with
    test_fighter_scraper = FighterScraper("", {})

    # Utility
    def _clean_soup(self, fighter_scraper: FighterScraper) -> None:
        """Clears FighterScrapers soup, for testing only."""

        fighter_scraper._soup = None
        fighter_scraper._stats_section = None
        fighter_scraper._stats_targets = None

    # _create_soup
    def test_create_soup_with_soup(self):
        test_soup = "<h1>Test soup</h1>"
        self.test_fighter_scraper._create_soup(test_soup)

        assert self.test_fighter_scraper._soup is not None
        assert self.test_fighter_scraper._stats_section is not None
        assert self.test_fighter_scraper._stats_targets is not None

        self._clean_soup(self.test_fighter_scraper)
        assert self.test_fighter_scraper._soup is None
        assert self.test_fighter_scraper._stats_section is None
        assert self.test_fighter_scraper._stats_targets is None

    # _parse_stat_block
    def test_parse_stat_block_webpage_striking(self):
        expected = (42, 73, 172)
        actual = self.scraper_ali_alqaisi._parse_stat_block(
            self.scraper_ali_alqaisi._stats_targets[0]
        )

        assert actual == expected

    def test_parse_stat_block_webpage_grappling(self):
        expected = (29, 0, 24)
        actual = self.scraper_ali_alqaisi._parse_stat_block(
            self.scraper_ali_alqaisi._stats_targets[1]
        )

        assert actual == expected

    def test_parse_stat_block_raw_empty_targets(self):
        test_data = """
            <div class="stats-records stats-records--two-column">
                <div class="overlap-athlete-content overlap-athlete-content--horizontal">
                    <div class="c-overlap__chart">
                        <div class="e-chart-circle__wrapper">
                            <svg class="e-chart-circle" viewBox="-14 -14 128 128" width="200" height="200" xmlns="http://www.w3.org/2000/svg">
                                <title>Striking accuracy 42%</title>
                                <circle class="e-chart-circle--athlete-stat__background" stroke="#fefefe" stroke-width="26" fill="none" cx="50" cy="50" r="50"></circle>
                                <circle class="e-chart-circle__circle" stroke="#d20a0a" stroke-width="26" fill="none" cx="50" cy="50" r="50" stroke-dasharray="314.2, 314.2" stroke-dashoffset="180.85352" transform="rotate(-90 50 50)"></circle>
                                <text class="e-chart-circle__percent" x="50" y="60" text-anchor="middle" font-size="30">42%</text>
                            </svg>
                        </div>
                    </div>
                    <div class="c-overlap__inner">
                        <div class="c-overlap--stats__title">
                            <h2 class="e-t3">Striking accuracy</h2>
                        </div>
                        <div class="c-overlap__stats-wrap">
                            <dl class="c-overlap__stats">
                                <dt class="c-overlap__stats-text">Sig. Strikes Landed</dt>
                                <dd class="c-overlap__stats-value">73</dd>
                            </dl>
                            <dl class="c-overlap__stats">
                                <dt class="c-overlap__stats-text">Sig. Strikes Attempted</dt>
                                <dd class="c-overlap__stats-value"></dd>
                            </dl>
                        </div>
                    </div>
                </div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = (42, 73, 0)
        actual = self.test_fighter_scraper._parse_stat_block(
            self.test_fighter_scraper._stats_targets[0]
        )

        assert actual == expected

    def test_parse_stat_block_raw_no_targets(self):
        test_data = '<div class="stats-records stats-records--two-column"></div>'
        self.test_fighter_scraper._create_soup(test_data)

        expected = (0, 0, 0)
        actual = self.test_fighter_scraper._parse_stat_block(
            self.test_fighter_scraper._stats_targets[0]
        )

        assert actual == expected

    # _parse_stats_section
    def test_parse_stats_section_webpage_win_method(self):
        expected = ((1, 13), (3, 38), (4, 50))
        actual = self.scraper_ali_alqaisi._parse_stats_section(
            self.scraper_ali_alqaisi._stats_section[1]
        )

        assert actual == expected

    def test_parse_stats_section_webpage_strike_position(self):
        expected = ((63, 86), (9, 12), (1, 1))
        actual = self.scraper_ali_alqaisi._parse_stats_section(
            self.scraper_ali_alqaisi._stats_section[0]
        )

        assert actual == expected

    def test_parse_stats_section_raw_empty_targets(self):
        test_data = """
            <div class="c-stat-3bar c-stat-3bar--no-chart">
                <h2 class="c-stat-3bar__title">Sig. Str. By Position</h2>
                <div class="c-stat-3bar__legend">
                    <div class="c-stat-3bar__group">
                        <div class="c-stat-3bar__label">Standing </div>
                        <div class="c-stat-3bar__value">63 (86%)</div>
                    </div>
                    <div class="c-stat-3bar__group">
                        <div class="c-stat-3bar__label">Clinch </div>
                        <div class="c-stat-3bar__value"></div>
                    </div>
                    <div class="c-stat-3bar__group">
                        <div class="c-stat-3bar__label">Ground </div>
                        <div class="c-stat-3bar__value">1 (1%)</div>
                    </div>
                </div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = ((63, 86), (0, 0), (1, 1))
        actual = self.test_fighter_scraper._parse_stats_section(
            self.test_fighter_scraper._stats_section[0]
        )

        assert actual == expected

    def test_parse_stats_section_raw_no_targets(self):
        test_data = '<div class="c-stat-3bar c-stat-3bar--no-chart"></div>'
        self.test_fighter_scraper._create_soup(test_data)

        expected = (0, 0), (0, 0), (0, 0)
        actual = self.test_fighter_scraper._parse_stats_section(
            self.test_fighter_scraper._stats_section[0]
        )

        assert actual == expected

    # _parse_result_set
    def test_parse_result_set_webpage_win_method(self):
        expected = {
            "Sig. Str. Landed": 2.43,
            "Sig. Str. Absorbed": 1.97,
            "Sig. Str. Defense": 56,
            "Knockdown Avg": 0.00,
        }

        actual = self.scraper_ali_alqaisi._parse_result_set(
            self.scraper_ali_alqaisi._stats_targets, expected.keys()
        )

        assert actual == expected

    def test_parse_result_set_webpage_strike_position(self):
        expected = {
            "Takedown avg": 3.50,
            "Takedown Defense": 60,
            "Submission avg": 1.00,
        }
        actual = self.scraper_ali_alqaisi._parse_result_set(
            self.scraper_ali_alqaisi._stats_targets, expected.keys()
        )

        assert actual == expected

    def test_parse_result_set_raw_empty_targets(self):
        test_data = """
            <div class="stats-records stats-records--two-column">
            <div class="stats-records--compare stats-records-inner">
                <div class="c-stat-compare c-stat-compare--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-1 ">
                    <div class="c-stat-compare__number"></div>
                    <div class="c-stat-compare__label">Sig. Str. Landed</div>
                    <div class="c-stat-compare__label-suffix">Per Min</div>
                </div>
                <div class="c-stat-compare__group c-stat-compare__group-2 ">
                    <div class="c-stat-compare__number">1.97 </div>
                    <div class="c-stat-compare__label">Sig. Str. Absorbed</div>
                    <div class="c-stat-compare__label-suffix">Per Min</div>
                </div>
                </div>
                <div class="c-stat-compare c-stat-compare--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-1 ">
                    <div class="c-stat-compare__number">3.50 </div>
                    <div class="c-stat-compare__label">Takedown avg</div>
                    <div class="c-stat-compare__label-suffix">Per 15 Min</div>
                </div>
                <div class="c-stat-compare__group c-stat-compare__group-2 ">
                    <div class="c-stat-compare__number">1.00 </div>
                    <div class="c-stat-compare__label">Submission avg</div>
                    <div class="c-stat-compare__label-suffix">Per 15 Min</div>
                </div>
                </div>
            </div>
            </div>
            <div class="stats-records stats-records--two-column">
            <div class="stats-records--compare stats-records-inner">
                <div class="tooltip">
                <button class="tooltip__button" type="button" aria-describedby="tooltip-1877601654">
                    <svg aria-hidden="true" width="20" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 7h2V5H9v2Zm1 11c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8Zm0-18a10 10 0 1 0 0 20 10 10 0 0 0 0-20ZM9 15h2V9H9v6Z" fill="#D20A0A"></path>
                    </svg>
                </button>
                <div id="tooltip-1877601654" role="tooltip" class="tooltip__content-wrap tooltip__content-wrap--top-right">
                    <div class="tooltip__content tooltip__content--top-right">
                    <ul>
                        <li>Sig. Str. Defense is the percentage of significant strikes attempted against a fighter that do not land.</li>
                        <li>Takedown defense is the percentage of takedowns attempted against a fighter that do not land.</li>
                        <li>Knockdown Avg. is the average number of knockdowns per 15 Minutes window.</li>
                    </ul>
                    </div>
                </div>
                </div>
                <div class="c-stat-compare c-stat-compare--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-1 ">
                    <div class="c-stat-compare__number"><div class="c-stat-compare__percent">%</div>
                    </div>
                    <div class="c-stat-compare__label">Sig. Str. Defense</div>
                </div>
                <div class="c-stat-compare__group c-stat-compare__group-2 ">
                    <div class="c-stat-compare__number">60 <div class="c-stat-compare__percent">%</div>
                    </div>
                    <div class="c-stat-compare__label">Takedown Defense</div>
                </div>
                </div>
                <div class="c-stat-compare c-stat-compare--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-1 ">
                    <div class="c-stat-compare__number">0.00 </div>
                    <div class="c-stat-compare__label">Knockdown Avg</div>
                </div>
                <div class="c-stat-compare__group c-stat-compare__group-2 ">
                    <div class="c-stat-compare__number">15:00 </div>
                    <div class="c-stat-compare__label">Average fight time</div>
                </div>
                </div>
            </div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = {
            "Sig. Str. Landed": 0,
            "Sig. Str. Absorbed": 1.97,
            "Sig. Str. Defense": 0,
            "Knockdown Avg": 0.00,
        }
        actual = self.test_fighter_scraper._parse_result_set(
            self.test_fighter_scraper._stats_targets, expected.keys()
        )

        assert actual == expected

    def test_parse_result_set_raw_no_targets(self):
        test_data = '<div class="stats-records stats-records--two-column"></div>'
        self.test_fighter_scraper._create_soup(test_data)

        expected = {
            "Sig. Str. Landed": 0,
            "Sig. Str. Absorbed": 0,
            "Sig. Str. Defense": 0,
            "Knockdown Avg": 0,
        }
        actual = self.test_fighter_scraper._parse_result_set(
            self.test_fighter_scraper._stats_targets, expected.keys()
        )

        assert actual == expected

    set_fighter_url

    def test_set_fighter_url_lower_case(self):
        test_url = "http://www.ufc.com/athlete/Jan-Blachowicz"
        expected = "http://www.ufc.com/athlete/jan-blachowicz"

        actual = set_fighter_url(test_url, self.incorrect_fighter_urls)

        assert actual == expected

    def test_set_fighter_url_https(self):
        test_url = "https://www.ufc.com/athlete/jan-blachowicz"
        expected = "http://www.ufc.com/athlete/jan-blachowicz"
        actual = set_fighter_url(test_url, self.incorrect_fighter_urls)

        assert actual == expected

    def test_set_fighter_url_banned_chars(self):
        test_url = "http://www.ufc.com/athlete/jan'-blachowicz--"
        expected = "http://www.ufc.com/athlete/jan-blachowicz"
        actual = set_fighter_url(test_url, self.incorrect_fighter_urls)

        assert actual == expected

    def test_set_fighter_url_incorrect_url(self):
        test_url = "http://www.ufc.com/athlete/Raul-Rosas-Jr."
        expected = "http://www.ufc.com/athlete/raul-rosas-jr"
        actual = set_fighter_url(test_url, self.incorrect_fighter_urls)

        assert actual == expected

    def test_set_fighter_url_incorrect_url_unidecode(self):
        # Tests if text is correctly decoded
        test_url = "http://www.ufc.com/athlete/Cristian-Quiñonez"
        expected = "http://www.ufc.com/athlete/trevin-dzhayls-6"
        actual = set_fighter_url(test_url, self.incorrect_fighter_urls)

        assert actual == expected

    # _get_name
    def test_get_name_webpage(self):
        expected = "Ali Al Qaisi"
        actual = self.scraper_ali_alqaisi._get_name()

        assert actual == expected

    def test_get_name_raw_remove_dashes(self):
        test_data = '<h1 class="hero-profile__name">Ali Al-Qaisi</h1>'
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Ali Al Qaisi"
        actual = self.test_fighter_scraper._get_name()

        assert actual == expected

    def test_get_name_raw_no_text(self):
        test_data = '<h1 class="hero-profile__name"></h1>'
        self.test_fighter_scraper._create_soup(test_data)

        expected = ""
        actual = self.test_fighter_scraper._get_name()

        assert actual == expected

    def test_get_name_raw_no_target(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = ""
        actual = self.test_fighter_scraper._get_name()

        assert actual == expected

    # _get_nickname
    def test_get_nickname_webpage(self):
        expected = "The Royal Fighter"
        actual = self.scraper_ali_alqaisi._get_nickname()

        assert actual == expected

    def test_get_nickname_raw_remove_quotation(self):
        test_data = '<p class="hero-profile__nickname">"The Royal Fighter"</p>'
        self.test_fighter_scraper._create_soup(test_data)

        expected = "The Royal Fighter"
        actual = self.test_fighter_scraper._get_nickname()

        assert actual == expected

    def test_get_nickname_raw_no_text(self):
        test_data = '<h1 class="hero-profile__nickname"></h1>'
        self.test_fighter_scraper._create_soup(test_data)

        expected = ""
        actual = self.test_fighter_scraper._get_nickname()

        assert actual == expected

    def test_get_nickname_raw_no_target(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = ""
        actual = self.test_fighter_scraper._get_nickname()

        assert actual == expected

    # _get_status
    def test_get_status_webpage(self):
        expected = "Not Fighting"
        actual = self.scraper_ali_alqaisi._get_status()

        assert actual == expected

    def test_get_status_raw_target_not_first(self):
        test_data = """
            <div class="c-bio__field">
                <div class="c-bio__label">Age</div>
                <div class="c-bio__text">
                <div class="field field--name-age field--type-integer field--label-hidden field__item">31</div>
            </div>
            <div class="c-bio__field">
                <div class="c-bio__label">Status</div>
                <div class="c-bio__text">Not Fighting</div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Not Fighting"
        actual = self.test_fighter_scraper._get_status()

        assert actual == expected

    def test_get_status_raw_no_status_target(self):
        test_data = """
            <div class="c-bio__field">
                <div class="c-bio__label">Age</div>
                <div class="c-bio__text">
                <div class="field field--name-age field--type-integer field--label-hidden field__item">31</div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Unknown"
        actual = self.test_fighter_scraper._get_status()

        assert actual == expected

    def test_get_status_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Unknown"
        actual = self.test_fighter_scraper._get_status()

        assert actual == expected

    # _get_ranking
    def test_get_ranking_webpage(self):
        expected = ("Unranked", "PFP Unranked")  # Could miss
        actual = self.scraper_ali_alqaisi._get_ranking()

        assert actual == expected

    def test_get_ranking_raw_title_with_pfp(self):
        test_data = """
            <div class="hero-profile__tags">
                <p class="hero-profile__tag">Flyweight Division</p>
                <p class="hero-profile__tag">#9 PFP</p>
                <p class="hero-profile__tag">Active</p>
                <p class="hero-profile__tag">Title Holder</p>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = ("Title Holder", "#9 PFP")
        actual = self.test_fighter_scraper._get_ranking()

        assert actual == expected

    def test_get_ranking_raw_unranked_with_pfp(self):
        test_data = """
            <div class="hero-profile__tags">
                <p class="hero-profile__tag">Bantamweight Division</p>
                <p class="hero-profile__tag">#5 PFP</p>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = ("Unranked", "#5 PFP")
        actual = self.test_fighter_scraper._get_ranking()

        assert actual == expected

    def test_get_ranking_raw_ranked_with_pfp(self):
        test_data = """
            <div class="hero-profile__tags">
                <p class="hero-profile__tag">#1 Bantamweight Division</p>
                <p class="hero-profile__tag">#5 PFP</p>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = ("#1", "#5 PFP")
        actual = self.test_fighter_scraper._get_ranking()

        assert actual == expected

    def test_get_ranking_raw_empty_targets(self):
        test_data = """
            <div class="hero-profile__tags">
                <p class="hero-profile__tag"></p>
                <p class="hero-profile__tag"></p>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = ("Unranked", "PFP Unranked")
        actual = self.test_fighter_scraper._get_ranking()

        assert actual == expected

    def test_get_ranking_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = ("Unranked", "PFP Unranked")
        actual = self.test_fighter_scraper._get_ranking()

        assert actual == expected

    # _get_weightclass
    def test_get_weightclass_webpage(self):
        expected = "Bantamweight Division"
        actual = self.scraper_ali_alqaisi._get_weightclass()

        assert actual == expected

    def test_get_weightclass_raw_empty_main_target(self):
        test_data = """
            <p class="hero-profile__tag">Featherweight Division</p>
            <p class="hero-profile__division-title"></p>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Featherweight Division"
        actual = self.test_fighter_scraper._get_weightclass()

        assert actual == expected

    def test_get_weightclass_raw_empty__main_target_no_fallback(self):
        test_data = '<p class="hero-profile__division-title"></p>'
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Unlisted"
        actual = self.test_fighter_scraper._get_weightclass()

        assert actual == expected
        
    def test_get_weightclass_raw_empty_main_target_and_empty_fallback(self):
        test_data = """
            <p class="hero-profile__tag"></p>
            <p class="hero-profile__division-title"></p>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Unlisted"
        actual = self.test_fighter_scraper._get_weightclass()

        assert actual == expected
        
    def test_get_weightclass_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Unlisted"
        actual = self.test_fighter_scraper._get_weightclass()

        assert actual == expected

    # _get_hometown
    def test_get_hometown_webpage(self):
        expected = ("Amman", "Jordan")
        actual = self.scraper_ali_alqaisi._get_hometown()

        assert actual == expected

    def test_get_hometown_raw_only_country(self):
        test_data = """
            <div class="c-bio__field c-bio__field--border-bottom-small-screens">
                <div class="c-bio__label">Hometown</div>
                <div class="c-bio__text">Mexico</div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = ("Unlisted", "Mexico")
        actual = self.test_fighter_scraper._get_hometown()

        assert actual == expected

    def test_get_hometown_raw_empty_targets(self):
        test_data = """
            <div class="c-bio__field c-bio__field--border-bottom-small-screens">
                <div class="c-bio__label">Hometown</div>
                <div class="c-bio__text"></div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = ("Unlisted", "Unlisted")
        actual = self.test_fighter_scraper._get_hometown()

        assert actual == expected

    def test_get_hometown_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = ("Unlisted", "Unlisted")
        actual = self.test_fighter_scraper._get_hometown()

        assert actual == expected

    # _get_gym
    def test_get_gym_webpage_unlisted(self):
        expected = "Unlisted"
        actual = self.scraper_ali_alqaisi._get_gym()

        assert actual == expected

    def test_get_gym_webpage_listed(self):
        expected = "Team Alpha Male  (Urijah Faber's Ultimate Fitness)"
        actual = self.scraper_joseph_benavidez._get_gym()

        assert actual == expected

    def test_get_gym_raw_empty_targets(self):
        test_data = """
            <div class="c-bio__field c-bio__field--border-bottom-small-screens">
                <div class="c-bio__label">Trains at</div>
                <div class="c-bio__text"></div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Unlisted"
        actual = self.test_fighter_scraper._get_gym()

        assert actual == expected

    def test_get_gym_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Unlisted"
        actual = self.test_fighter_scraper._get_gym()

        assert actual == expected

    # _get_fighting_style
    def test_get_fighting_style_webpage_unlisted(self):
        expected = "Unlisted"
        actual = self.scraper_ali_alqaisi._get_fighting_style()

        assert actual == expected

    def test_get_fighting_style_webpage_listed(self):
        expected = "Jiu-Jitsu"
        actual = self.scraper_joseph_benavidez._get_fighting_style()

        assert actual == expected

    def test_get_fighting_style_raw_empty_targets(self):
        test_data = """
            <div class="c-bio__field c-bio__field--border-bottom-small-screens">
                <div class="c-bio__label">Fighting style</div>
                <div class="c-bio__text"></div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Unlisted"
        actual = self.test_fighter_scraper._get_fighting_style()

        assert actual == expected

    def test_get_fighting_style_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = "Unlisted"
        actual = self.test_fighter_scraper._get_fighting_style()

        assert actual == expected

    # _get_average_fight_time
    def test_get_average_fight_time_webpage(self):
        expected = "15:00"
        actual = self.scraper_ali_alqaisi._get_average_fight_time()

        assert actual == expected

    def test_get_average_fight_time_raw_target_not_first(self):
        test_data = """
            <div class="c-stat-compare__group c-stat-compare__group-2 ">
                <div class="c-stat-compare__number">1.00</div>
                <div class="c-stat-compare__label">Submission avg</div>
                <div class="c-stat-compare__label-suffix">Per 15 Min</div>
            </div>
            <div class="c-stat-compare__group c-stat-compare__group-2 ">
                <div class="c-stat-compare__number">15:00</div>
                <div class="c-stat-compare__label">Average fight time</div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = "15:00"
        actual = self.test_fighter_scraper._get_average_fight_time()

        assert actual == expected

    def test_get_average_fight_time_raw_empty_targets(self):
        test_data = """
            <div class="c-stat-compare__group c-stat-compare__group-2 ">
                <div class="c-stat-compare__number"></div>
                <div class="c-stat-compare__label">Average fight time</div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = "00:00"
        actual = self.test_fighter_scraper._get_average_fight_time()

        assert actual == expected

    def test_get_average_fight_time_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = "00:00"
        actual = self.test_fighter_scraper._get_average_fight_time()

        assert actual == expected

    # _get_strike_position_stats
    def test_get_strike_position_stats_webpage(self):
        expected = (63, 86), (9, 12), (1, 1)
        actual = self.scraper_ali_alqaisi._get_strike_position_stats()

        assert actual == expected

    def test_get_strike_position_stats_raw_empty_targets(self):
        test_data = """
            <div class="c-stat-3bar c-stat-3bar--no-chart">
                <h2 class="c-stat-3bar__title">Sig. Str. By Position</h2>
                <div class="c-stat-3bar__legend">
                        <div class="c-stat-3bar__group">
                        <div class="c-stat-3bar__label">Standing </div>
                        <div class="c-stat-3bar__value">63 (86%)</div>
                    </div>
                        <div class="c-stat-3bar__group">
                        <div class="c-stat-3bar__label">Clinch </div>
                        <div class="c-stat-3bar__value"></div>
                    </div>
                        <div class="c-stat-3bar__group">
                        <div class="c-stat-3bar__label">Ground </div>
                        <div class="c-stat-3bar__value">1 (1%)</div>
                    </div>
                </div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = (63, 86), (0, 0), (1, 1)
        actual = self.test_fighter_scraper._get_strike_position_stats()

        assert actual == expected

    def test_get_strike_position_stats_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = (0, 0), (0, 0), (0, 0)
        actual = self.test_fighter_scraper._get_strike_position_stats()

        assert actual == expected

    # _get_strike_target_stats
    def test_get_strike_target_stats_webpage(self):
        expected = {"head": (40, 55), "body": (10, 14), "leg": (23, 32)}
        actual = self.scraper_ali_alqaisi._get_strike_target_stats()

        assert actual == expected

    def test_get_strike_target_stats_raw_empty_targets(self):
        test_data = """
            <svg class="c-stat-body__svg" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="268px" height="208px" viewBox="0 0 268 208">
                <g id="e-stat-body_x5F__x5F_bg">
                    <line id="line_2_" fill="none" stroke="#EAEAEA" stroke-linecap="square" stroke-miterlimit="10" x1="0.5" y1="39.5" x2="266.14" y2="39.5"></line>
                    <line id="line_1_" fill="none" stroke="#EAEAEA" stroke-linecap="square" stroke-miterlimit="10" x1="0.5" y1="98.5" x2="266.14" y2="98.5"></line>
                    <line id="line" fill="none" stroke="#EAEAEA" stroke-linecap="square" stroke-miterlimit="10" x1="0.5" y1="152.5" x2="266.14" y2="152.5"></line>
                </g>
                <g id="e-stat-body_x5F__x5F_head-txt">
                    <text id="e-stat-body_x5F__x5F_head_percent" transform="matrix(1 0 0 1 230.8119 32)" fill="#D20A0A" font-size="14px"></text>
                    <text id="e-stat-body_x5F__x5F_head_value" transform="matrix(1 0 0 1 197.8119 32)" fill="#D20A0A" font-size="14px"></text>
                    <text transform="matrix(1 0 0 1 3.8119 33)" fill="#1C1C1C" font-weight="600" font-size="16px">Head</text>
                </g>
                <g id="e-stat-body_x5F__x5F_body-txt">
                    <text id="e-stat-body_x5F__x5F_body_percent" transform="matrix(1 0 0 1 226.8119 90)" fill="#D20A0A" font-size="14px">14%</text>
                    <text id="e-stat-body_x5F__x5F_body_value" transform="matrix(1 0 0 1 197.8119 90)" fill="#D20A0A" font-size="14px">10 </text>
                    <text transform="matrix(1 0 0 1 4.8119 91)" fill="#1C1C1C" font-weight="600" font-size="16px">Body</text>
                </g>
                <g id="e-stat-body_x5F__x5F_leg-txt">
                    <text id="e-stat-body_x5F__x5F_leg_percent" transform="matrix(1 0 0 1 226.8119 145)" fill="#D20A0A" font-size="14px"></text>
                    <text id="e-stat-body_x5F__x5F_leg_value" transform="matrix(1 0 0 1 197.8119 145)" fill="#D20A0A" font-size="14px">23</text>
                    <text transform="matrix(1 0 0 1 8.8119 146)" fill="#1C1C1C" font-weight="600" font-size="16px">Leg</text>
                </g>
            </svg>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = {"head": (0, 0), "body": (10, 14), "leg": (23, 0)}
        actual = self.test_fighter_scraper._get_strike_target_stats()

        assert actual == expected

    def test_get_strike_target_stats_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = {"head": (0, 0), "body": (0, 0), "leg": (0, 0)}
        actual = self.test_fighter_scraper._get_strike_target_stats()

        assert actual == expected

    # _get_striking_stats
    def test_get_striking_stats_webpage(self):
        expected = {
            "striking_accuracy": 42,
            "strikes_landed": 73,
            "strikes_attempted": 172,
            "strikes_average": 2.43,
            "strikes_absorbed_average": 1.97,
            "striking_defence": 56,
            "knockdown_average": 0.00,
        }
        actual = self.scraper_ali_alqaisi._get_striking_stats()

        for key, value in expected.items():
            assert actual[key] == value

    def test_get_striking_stats_raw_empty_targets(self):
        test_data = """
            <div class="stats-records stats-records--two-column">
            <div class="stats-records-inner">
                <div class="tooltip">
                <button class="tooltip__button" type="button" aria-describedby="tooltip-810836017">
                    <svg aria-hidden="true" width="20" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 7h2V5H9v2Zm1 11c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8Zm0-18a10 10 0 1 0 0 20 10 10 0 0 0 0-20ZM9 15h2V9H9v6Z" fill="#D20A0A"></path>
                    </svg>
                </button>
                <div id="tooltip-810836017" role="tooltip" class="tooltip__content-wrap tooltip__content-wrap--top-right">
                    <div class="tooltip__content tooltip__content--top-right">Significant Strikes include all strikes at distance, plus power strikes in the clinch and on the ground.</div>
                </div>
                </div>
                <div class="overlap-athlete-content overlap-athlete-content--horizontal">
                <div class="c-overlap__chart">
                    <div class="e-chart-circle__wrapper">
                    <svg class="e-chart-circle" viewBox="-14 -14 128 128" width="200" height="200" xmlns="http://www.w3.org/2000/svg">
                        <title>Striking accuracy 42%</title>
                        <circle class="e-chart-circle--athlete-stat__background" stroke="#fefefe" stroke-width="26" fill="none" cx="50" cy="50" r="50"></circle>
                        <circle class="e-chart-circle__circle" stroke="#d20a0a" stroke-width="26" fill="none" cx="50" cy="50" r="50" stroke-dasharray="314.2, 314.2" stroke-dashoffset="180.85352" transform="rotate(-90 50 50)"></circle>
                        <text class="e-chart-circle__percent" x="50" y="60" text-anchor="middle" font-size="30">42%</text>
                    </svg>
                    </div>
                </div>
                <div class="c-overlap__inner">
                    <div class="c-overlap--stats__title">
                    <h2 class="e-t3">Striking accuracy</h2>
                    </div>
                    <div class="c-overlap__stats-wrap">
                    <dl class="c-overlap__stats">
                        <dt class="c-overlap__stats-text">Sig. Strikes Landed</dt>
                        <dd class="c-overlap__stats-value">73</dd>
                    </dl>
                    <dl class="c-overlap__stats">
                        <dt class="c-overlap__stats-text">Sig. Strikes Attempted</dt>
                        <dd class="c-overlap__stats-value"></dd>
                    </dl>
                    </div>
                </div>
                </div>
            </div>
            </div>
            <div class="stats-records stats-records--two-column">
            <div class="stats-records--compare stats-records-inner">
                <div class="c-stat-compare c-stat-a--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-1 ">
                    <div class="c-stat-compare__number">2.43 </div>
                    <div class="c-stat-compare__label">Sig. Str. Landed</div>
                    <div class="c-stat-compare__label-suffix">Per Min</div>
                </div>
                <div class="c-stat-compare__group c-stat-compare__group-2 ">
                    <div class="c-stat-compare__number">1.97 </div>
                    <div class="c-stat-compare__label">Sig. Str. Absorbed</div>
                    <div class="c-stat-compare__label-suffix">Per Min</div>
                </div>
                </div>
                <div class="c-stat-compare c-stat-compare--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-1 ">
                    <div class="c-stat-compare__number">3.50 </div>
                    <div class="c-stat-compare__label">Takedown avg</div>
                    <div class="c-stat-compare__label-suffix">Per 15 Min</div>
                </div>
                <div class="c-stat-compare__group c-stat-compare__group-2 ">
                    <div class="c-stat-compare__number">1.00 </div>
                    <div class="c-stat-compare__label">Submission avg</div>
                    <div class="c-stat-compare__label-suffix">Per 15 Min</div>
                </div>
                </div>
            </div>
            </div>
            <div class="stats-records stats-records--two-column">
            <div class="stats-records--compare stats-records-inner">
                <div class="tooltip">
                <button class="tooltip__button" type="button" aria-describedby="tooltip-1877601654">
                    <svg aria-hidden="true" width="20" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 7h2V5H9v2Zm1 11c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8Zm0-18a10 10 0 1 0 0 20 10 10 0 0 0 0-20ZM9 15h2V9H9v6Z" fill="#D20A0A"></path>
                    </svg>
                </button>
                <div id="tooltip-1877601654" role="tooltip" class="tooltip__content-wrap tooltip__content-wrap--top-right">
                    <div class="tooltip__content tooltip__content--top-right">
                    <ul>
                        <li>Sig. Str. Defense is the percentage of significant strikes attempted against a fighter that do not land.</li>
                        <li>Takedown defense is the percentage of takedowns attempted against a fighter that do not land.</li>
                        <li>Knockdown Avg. is the average number of knockdowns per 15 Minutes window.</li>
                    </ul>
                    </div>
                </div>
                </div>
                <div class="c-stat-compare c-stat-compare--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-2 ">
                    <div class="c-stat-compare__number">60 <div class="c-stat-compare__percent">%</div>
                    </div>
                    <div class="c-stat-compare__label">Takedown Defense</div>
                </div>
                </div>
                <div class="c-stat-compare c-stat-compare--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-1 ">
                    <div class="c-stat-compare__number">0.00 </div>
                    <div class="c-stat-compare__label">Knockdown Avg</div>
                </div>
                <div class="c-stat-compare__group c-stat-compare__group-2 ">
                    <div class="c-stat-compare__number">15:00 </div>
                    <div class="c-stat-compare__label">Average fight time</div>
                </div>
                </div>
            </div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)
        expected = {
            "striking_accuracy": 42,
            "strikes_landed": 73,
            "strikes_attempted": 0,
            "strikes_average": 2.43,
            "strikes_absorbed_average": 1.97,
            "striking_defence": 0,
            "knockdown_average": 0.00,
        }
        actual = self.test_fighter_scraper._get_striking_stats()

        for key, value in expected.items():
            assert actual[key] == value

    def test_get_striking_stats_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)
        expected = {
            "striking_accuracy": 0,
            "strikes_landed": 0,
            "strikes_attempted": 0,
            "strikes_average": 0,
            "strikes_absorbed_average": 0,
            "striking_defence": 0,
            "knockdown_average": 0,
        }
        actual = self.test_fighter_scraper._get_striking_stats()

        for key, value in expected.items():
            assert actual[key] == value

    # _get_record_obj
    def test_get_record_stats_webpage(self):
        expected = (8, 5, 0)
        actual = self.scraper_ali_alqaisi._get_record_stats()

        assert actual == expected

    def test_get_record_stats_raw_target_no_text(self):
        test_data = '<p class="hero-profile__division-body"></p>'
        self.test_fighter_scraper._create_soup(test_data)

        expected = (0, 0, 0)
        actual = self.test_fighter_scraper._get_record_stats()

        assert actual == expected

    def test_get_record_stats_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = (0, 0, 0)
        actual = self.test_fighter_scraper._get_record_stats()

        assert actual == expected

    # _get_win_method_stats
    def test_get_win_method_stats_webpage(self):
        expected = (1, 13), (3, 38), (4, 50)
        actual = self.scraper_ali_alqaisi._get_win_method_stats()

        assert actual == expected

    def test_get_win_method_stats_raw_empty_targets(self):
        test_data = """
            <div class="c-stat-3bar c-stat-3bar--no-chart"></div>
            
            <div class="c-stat-3bar c-stat-3bar--no-chart">
                <h2 class="c-stat-3bar__title">Win by Method</h2>
                <div class="c-stat-3bar__legend">
                        <div class="c-stat-3bar__group">
                        <div class="c-stat-3bar__label">KO/TKO </div>
                        <div class="c-stat-3bar__value">1 (13%)</div>
                    </div>
                        <div class="c-stat-3bar__group">
                        <div class="c-stat-3bar__label">DEC </div>
                        <div class="c-stat-3bar__value"></div>
                    </div>
                        <div class="c-stat-3bar__group">
                        <div class="c-stat-3bar__label">SUB </div>
                        <div class="c-stat-3bar__value">4 (50%)</div>
                    </div>
                </div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = (1, 13), (0, 0), (4, 50)
        actual = self.test_fighter_scraper._get_win_method_stats()

        assert actual == expected

    def test_get_win_method_stats_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = (0, 0), (0, 0), (0, 0)
        actual = self.test_fighter_scraper._get_win_method_stats()

        assert actual == expected

    # _get_physical_stats
    def test_get_physical_stats_webpage(self):
        expected = {
            "age": self.test_fighter_age,
            "height": 68.0,
            "weight": 136.0,
            "reach": 68.0,
            "leg_reach": 38.0,
        }
        actual = self.scraper_ali_alqaisi._get_physical_stats()

        assert actual == expected

    def test_get_physical_stats_raw_empty_targets(self):
        test_data = """
            <div class="c-bio__info-details">
                <div class="c-bio__row--3col">
                    <div class="c-bio__field">
                        <div class="c-bio__label">Age</div>
                        <div class="c-bio__text">
                            <div class="field field--name-age field--type-integer field--label-hidden field__item"></div>
                        </div>
                    </div>
                    <div class="c-bio__field">
                        <div class="c-bio__label">Height</div>
                        <div class="c-bio__text">68.00</div>
                    </div>
                    <div class="c-bio__field">
                        <div class="c-bio__label">Weight</div>
                        <div class="c-bio__text"></div>
                    </div>
                </div>
                <div class="c-bio__row--3col">
                    <div class="c-bio__field">
                        <div class="c-bio__label">Octagon Debut</div>
                        <div class="c-bio__text">Aug. 08, 2020</div>
                    </div>
                    <div class="c-bio__field">
                        <div class="c-bio__label">Reach</div>
                        <div class="c-bio__text">68.00</div>
                    </div>
                    <div class="c-bio__field">
                        <div class="c-bio__label">Leg reach</div>
                        <div class="c-bio__text"></div>
                    </div>
                </div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = {
            "age": 0,
            "height": 68.0,
            "weight": 0,
            "reach": 68.0,
            "leg_reach": 0,
        }
        actual = self.test_fighter_scraper._get_physical_stats()

        assert actual == expected

    def test_get_physical_stats_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = {"age": 0, "height": 0, "weight": 0, "reach": 0, "leg_reach": 0}
        actual = self.test_fighter_scraper._get_physical_stats()

        assert actual == expected

    # _get_grappling_stats
    def test_get_grappling_stats_webpage(self):
        expected = {
            "takedown_accuracy": 29,
            "takedowns_landed": 0,
            "takedowns_attempted": 24,
            "takedowns_average": 3.50,
            "takedown_defence": 60,
            "submission_average": 1.00,
        }
        actual = self.scraper_ali_alqaisi._get_grappling_stats()

        for key, value in expected.items():
            assert actual[key] == value

    def test_get_grappling_stats_raw_empty_targets(self):
        test_data = """
            <div class="stats-records stats-records--two-column"></div>
            <div class="stats-records stats-records--two-column">
            <div class="stats-records-inner">
                <div class="tooltip">
                <button class="tooltip__button" type="button" aria-describedby="tooltip-1914946899">
                    <svg aria-hidden="true" width="20" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 7h2V5H9v2Zm1 11c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8Zm0-18a10 10 0 1 0 0 20 10 10 0 0 0 0-20ZM9 15h2V9H9v6Z" fill="#D20A0A"></path>
                    </svg>
                </button>
                <div id="tooltip-1914946899" role="tooltip" class="tooltip__content-wrap tooltip__content-wrap--top-right">
                    <div class="tooltip__content tooltip__content--top-right">A takedown is awarded when a fighter deliberately grapples an opponent to the ground and establishes an advantageous position for an appreciable amount of time.</div>
                </div>
                </div>
                <div class="overlap-athlete-content overlap-athlete-content--horizontal">
                <div class="c-overlap__chart">
                    <div class="e-chart-circle__wrapper">
                    <svg class="e-chart-circle" viewBox="-14 -14 128 128" width="200" height="200" xmlns="http://www.w3.org/2000/svg">
                        <title>Takedown Accuracy 29%</title>
                        <circle class="e-chart-circle--athlete-stat__background" stroke="#fefefe" stroke-width="26" fill="none" cx="50" cy="50" r="50"></circle>
                        <circle class="e-chart-circle__circle" stroke="#d20a0a" stroke-width="26" fill="none" cx="50" cy="50" r="50" stroke-dasharray="314.2, 314.2" stroke-dashoffset="222.54786" transform="rotate(-90 50 50)"></circle>
                        <text class="e-chart-circle__percent" x="50" y="60" text-anchor="middle" font-size="30">29%</text>
                    </svg>
                    </div>
                </div>
                <div class="c-overlap__inner">
                    <div class="c-overlap--stats__title">
                    <h2 class="e-t3">Takedown Accuracy</h2>
                    </div>
                    <div class="c-overlap__stats-wrap">
                    <dl class="c-overlap__stats">
                        <dt class="c-overlap__stats-text">Takedowns Landed</dt>
                        <dd class="c-overlap__stats-value"></dd>
                    </dl>
                    <dl class="c-overlap__stats">
                        <dt class="c-overlap__stats-text">Takedowns Attempted</dt>
                        <dd class="c-overlap__stats-value">24</dd>
                    </dl>
                    </div>
                </div>
                </div>
            </div>
            </div>
            <div class="stats-records stats-records--two-column">
            <div class="stats-records--compare stats-records-inner">
                <div class="c-stat-compare c-stat-compare--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-1 ">
                    <div class="c-stat-compare__number">2.43 </div>
                    <div class="c-stat-compare__label">Sig. Str. Landed</div>
                    <div class="c-stat-compare__label-suffix">Per Min</div>
                </div>
                <div class="c-stat-compare__group c-stat-compare__group-2 ">
                    <div class="c-stat-compare__number">1.97 </div>
                    <div class="c-stat-compare__label">Sig. Str. Absorbed</div>
                    <div class="c-stat-compare__label-suffix">Per Min</div>
                </div>
                </div>
                <div class="c-stat-compare c-stat-compare--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-1 ">
                    <div class="c-stat-compare__number">3.50 </div>
                    <div class="c-stat-compare__label">Takedown avg</div>
                    <div class="c-stat-compare__label-suffix">Per 15 Min</div>
                </div>
                </div>
            </div>
            </div>
            <div class="stats-records stats-records--two-column">
            <div class="stats-records--compare stats-records-inner">
                <div class="tooltip">
                <button class="tooltip__button" type="button" aria-describedby="tooltip-1877601654">
                    <svg aria-hidden="true" width="20" height="20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 7h2V5H9v2Zm1 11c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8Zm0-18a10 10 0 1 0 0 20 10 10 0 0 0 0-20ZM9 15h2V9H9v6Z" fill="#D20A0A"></path>
                    </svg>
                </button>
                <div id="tooltip-1877601654" role="tooltip" class="tooltip__content-wrap tooltip__content-wrap--top-right">
                    <div class="tooltip__content tooltip__content--top-right">
                    <ul>
                        <li>Sig. Str. Defense is the percentage of significant strikes attempted against a fighter that do not land.</li>
                        <li>Takedown defense is the percentage of takedowns attempted against a fighter that do not land.</li>
                        <li>Knockdown Avg. is the average number of knockdowns per 15 Minutes window.</li>
                    </ul>
                    </div>
                </div>
                </div>
                <div class="c-stat-compare c-stat-compare--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-1 ">
                    <div class="c-stat-compare__number">56 <div class="c-stat-compare__percent">%</div>
                    </div>
                    <div class="c-stat-compare__label">Sig. Str. Defense</div>
                </div>
                <div class="c-stat-compare__group c-stat-compare__group-2 ">
                    <div class="c-stat-compare__number"><div class="c-stat-compare__percent">%</div>
                    </div>
                    <div class="c-stat-compare__label">Takedown Defense</div>
                </div>
                </div>
                <div class="c-stat-compare c-stat-compare--no-bar">
                <div class="c-stat-compare__group c-stat-compare__group-1 ">
                    <div class="c-stat-compare__number">0.00 </div>
                    <div class="c-stat-compare__label">Knockdown Avg</div>
                </div>
                <div class="c-stat-compare__group c-stat-compare__group-2 ">
                    <div class="c-stat-compare__number">15:00 </div>
                    <div class="c-stat-compare__label">Average fight time</div>
                </div>
                </div>
            </div>
            </div>
        """
        self.test_fighter_scraper._create_soup(test_data)

        expected = {
            "takedown_accuracy": 29,
            "takedowns_landed": 0,
            "takedowns_attempted": 24,
            "takedowns_average": 3.50,
            "takedown_defence": 0,
            "submission_average": 0,
        }
        actual = self.test_fighter_scraper._get_grappling_stats()

        for key, value in expected.items():
            assert actual[key] == value

    def test_get_grappling_stats_raw_no_targets(self):
        test_data = ""
        self.test_fighter_scraper._create_soup(test_data)

        expected = {
            "takedown_accuracy": 0,
            "takedowns_landed": 0,
            "takedowns_attempted": 0,
            "takedowns_average": 0,
            "takedown_defence": 0,
            "submission_average": 0,
        }
        actual = self.test_fighter_scraper._get_grappling_stats()

        for key, value in expected.items():
            assert actual[key] == value

    # Object related methods
    def test_get_record_obj(self):
        expected = {"win": 8, "loss": 5, "draw": 0}
        actual = self.scraper_ali_alqaisi._get_record_obj()

        assert isinstance(actual, Record)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    def test_get_win_method_obj(self):
        expected = {
            "knockout": 1,
            "knockout_per": 13,
            "decision": 3,
            "decision_per": 38,
            "submission": 4,
            "submission_per": 50,
            "average_fight_time": "15:00",
        }
        actual = self.test_fighter.win_method

        assert isinstance(actual, WinMethod)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    def test_get_physical_stats_obj(self):
        expected = {
            "age": self.test_fighter_age,
            "height": 68.00,
            "weight": 136.00,
            "reach": 68.00,
            "leg_reach": 38.00,
        }
        actual = self.test_fighter.physical_stats

        assert isinstance(actual, PhysicalStats)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    def test_get_strike_position_obj(self):
        expected = {
            "standing": 63,
            "standing_per": 86,
            "clinch": 9,
            "clinch_per": 12,
            "ground": 1,
            "ground_per": 1,
        }
        actual = self.test_fighter.striking.strike_position

        assert isinstance(actual, StrikePosition)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    def test_get_strike_target_obj(self):
        expected = {
            "head": 40,
            "head_per": 55,
            "body": 10,
            "body_per": 14,
            "leg": 23,
            "leg_per": 32,
        }
        actual = self.test_fighter.striking.strike_target

        assert isinstance(actual, StrikeTarget)

        for key, value in expected.items():
            assert actual.__dict__[key] == value

    def test_get_striking_obj(self):
        expected = {
            "striking_accuracy": 42,
            "strikes_landed": 73,
            "strikes_attempted": 172,
            "strikes_average": 2.43,
            "strikes_absorbed_average": 1.97,
            "striking_defence": 56,
            "knockdown_average": 0.00,
            "strike_position": {
                "standing": 63,
                "standing_per": 86,
                "clinch": 9,
                "clinch_per": 12,
                "ground": 1,
                "ground_per": 1,
            },
            "strike_target": {
                "head": 40,
                "head_per": 55,
                "body": 10,
                "body_per": 14,
                "leg": 23,
                "leg_per": 32,
            },
        }
        actual = self.scraper_ali_alqaisi._get_striking_obj()

        assert isinstance(actual, Striking)

        for key, value in expected.items():
            if key in ["strike_position", "strike_target"]:
                if key == "strike_position":
                    assert isinstance(actual.__dict__[key], StrikePosition)
                elif key == "strike_target":
                    assert isinstance(actual.__dict__[key], StrikeTarget)
                for sub_key, sub_value in value.items():
                    assert actual.__dict__[key].__dict__[sub_key] == sub_value
                continue
            assert actual.__dict__[key] == value

    def test_get_grappling_obj(self):
        expected = {
            "takedown_accuracy": 29,
            "takedowns_landed": 0,
            "takedowns_attempted": 24,
            "takedowns_average": 3.50,
            "takedown_defence": 60,
            "submission_average": 1.00,
        }
        actual = self.scraper_ali_alqaisi._get_grappling_obj()

        assert isinstance(actual, Grappling)

        for key, value in expected.items():
            assert actual.__dict__[key] == value
