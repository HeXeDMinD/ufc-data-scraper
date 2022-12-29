import pytz

from datetime import datetime

from ufc_data_scraper.utils import convert_date


class TestUtils:
    def test_convert_date_type(self):
        test_start_time = "2022-12-10T23:30Z"
        expected = datetime
        actual = convert_date(test_start_time)

        assert isinstance(actual, expected)

    def test_convert_date(self):
        test_start_time = "2022-12-10T23:30Z"
        expected = datetime(
            year=2022, month=12, day=10, hour=23, minute=30, tzinfo=pytz.timezone("GMT")
        )
        actual = convert_date(test_start_time)

        assert actual == expected

    def test__convert_date_missing_date(self):
        test_start_time = ""
        expected = None
        actual = convert_date(test_start_time)

        assert actual == expected
