from ufc_data_scraper.scraper.fighter_scraper import _FighterScraper
from ufc_data_scraper.custom_objects.fighter import *

class TestFighterScraper():
    test_url = "https://www.ufc.com/athlete/ali-alqaisi" # Retired fighter
    
    test_fighter_scraper = _FighterScraper(test_url)
    test_fighter = test_fighter_scraper._scrape_fighter()
    
    def test_set_fighter_url_lower_case(self):
        test_url = "http://www.ufc.com/athlete/Jan-Blachowicz"
        expected = "http://www.ufc.com/athlete/jan-blachowicz"
        
        actual = self.test_fighter_scraper._set_fighter_url(test_url)
        
        assert actual == expected
        
    def test_set_fighter_url_https(self):
        test_url = "https://www.ufc.com/athlete/jan-blachowicz"
        expected = "http://www.ufc.com/athlete/jan-blachowicz"
        actual = self.test_fighter_scraper._set_fighter_url(test_url)
        
        assert actual == expected
    
    def test_set_fighter_url_banned_chars(self):
        test_url = "http://www.ufc.com/athlete/jan-blachowicz--"
        expected = "http://www.ufc.com/athlete/jan-blachowicz"
        actual = self.test_fighter_scraper._set_fighter_url(test_url)
        
        assert actual == expected
        
    def test_set_fighter_url_banned_chars_2(self):
        test_url = "http://www.ufc.com/athlete/'jan-blachowicz"
        expected = "http://www.ufc.com/athlete/jan-blachowicz"
        actual = self.test_fighter_scraper._set_fighter_url(test_url)
        
        assert actual == expected
        
    def test_set_fighter_url_incorrect_url(self):
        test_url = "http://www.ufc.com/athlete/Raul-Rosas-Jr."
        expected = "http://www.ufc.com/athlete/raul-rosas-jr"
        actual = self.test_fighter_scraper._set_fighter_url(test_url)
        
        assert actual == expected
    
    def test_get_name(self):
        expected = "Ali Al Qaisi"
        actual = self.test_fighter_scraper._get_name()
        
        assert actual == expected
        
    def test_get_nickname(self):
        expected = "The Royal Fighter"
        actual = self.test_fighter_scraper._get_nickname()
        
        assert actual == expected
        
    def test_get_status(self):
        expected = "Not Fighting" # Could miss
        actual = self.test_fighter_scraper._get_status()
        
        assert actual == expected
    
    def test_get_ranking(self):
        expected = ("Unranked", "Unranked") # Could miss
        actual = self.test_fighter_scraper._get_ranking()
        
        assert actual == expected
    
    def test_get_weightclass(self):
        expected = "Bantamweight Division"
        actual = self.test_fighter_scraper._get_weightclass()
        
        assert actual == expected
    
    def test_get_hometown(self):
        expected = ("Amman", "Jordan")
        actual = self.test_fighter_scraper._get_hometown()
        
        assert actual == expected
        
    def _get_gym(self):
        expected = "Unlisted" # Could miss
        actual = self.test_fighter_scraper._get_gym()
        
        assert actual == expected
        
    def test_get_fighting_style(self):
        expected = "Unlisted" # Could miss
        actual = self.test_fighter_scraper._get_fighting_style()
        
        assert actual == expected
    
    def test_get_record_obj(self):
        expected = Record(win=8, loss=5, draw=0)
        actual = self.test_fighter_scraper._get_record_obj().__dict__
        
        for key, value in expected.__dict__.items():
            assert actual[key] == value
        
    def test_get_average_fight_time(self):
        expected = "15:00"
        actual = self.test_fighter_scraper._get_average_fight_time()
        
        assert actual == expected

    def test_get_win_method_obj(self):
        expected = WinMethod(
            knockout=1,
            knockout_per=13,
            decision=3,
            decision_per=38,
            submission=4,
            submission_per=50,
            average_fight_time="15:00",
        )
        actual = self.test_fighter.win_method.__dict__
        
        for key, value in expected.__dict__.items():
            assert actual[key] == value
            
    def test_get_physical_stats_obj(self):
        expected = PhysicalStats(
            age=31,
            height=68.00,
            weight=136.00,
            reach=68.00,
            leg_reach=38.00,
        )
        actual = self.test_fighter.physical_stats.__dict__
        
        for key, value in expected.__dict__.items():
            assert actual[key] == value
        
    def test_get_strike_position_obj(self):
        expected = StrikePosition(
            standing=63,
            standing_per=86,
            clinch=9,
            clinch_per=12,
            ground=1,
            ground_per=1,
        )
        actual = self.test_fighter.striking.strike_position.__dict__
        
        for key, value in expected.__dict__.items():
            assert actual[key] == value
            
    def test_get_strike_target_obj(self):
        expected = StrikeTarget(
            head=40,
            head_per=55,
            body=10,
            body_per=14,
            leg=23,
            leg_per=32,
        )
        actual = self.test_fighter.striking.strike_target.__dict__
        
        for key, value in expected.__dict__.items():
            assert actual[key] == value

    def test_get_striking_stats(self):
        expected = Striking(
            striking_accuracy=42,
            strikes_landed=73,
            strikes_attempted=172,
            strikes_average=2.43,
            strikes_absorbed_average=1.97,
            striking_defence=56,
            knockdown_average=0.00,
            strike_position=None,
            strike_target=None
        )
        actual = self.test_fighter.striking.__dict__
        
        for key, value in expected.__dict__.items():
            if key == "strike_position" or key == "strike_target":
                continue
            assert actual[key] == value