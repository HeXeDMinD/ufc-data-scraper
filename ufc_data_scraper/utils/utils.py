import os
import json
import pytz
import requests

from datetime import datetime


def convert_date(date: str) -> datetime:
    """Converts API response date into usable format.

    Args:
        date (str): Date in simple string format.

    Returns:
        datetime: Datetime object of supplied string, localized to GMT.
    """

    date_obj = None

    if date:
        date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%MZ")
        date_obj = pytz.timezone("GMT").localize(date_obj)

    return date_obj


def fetch_latest_urls(full_path: str) -> dict:
    data_url = "https://raw.githubusercontent.com/HeXeDMinD/ufc-data-scraper/main/ufc_data_scraper/data/incorrect_urls.json"

    site_response = requests.get(data_url)

    if site_response.status_code != 200:
        return None

    json_data = site_response.json()
    json_data["last_fetched"] = datetime.strftime(
        datetime.now(), "%Y-%m-%d %H:%M")

    json_dump = json.dumps(json_data, indent=4)
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(json_dump)

    return json_data.get("incorrect_urls")


def should_fetch_latest(last_fetched: str):
    time_delta = datetime.now() - datetime.strptime(last_fetched,
                                                    "%Y-%m-%d %H:%M")
    time_delta_in_hours = time_delta.total_seconds() / 3600
    return time_delta_in_hours > 1


def get_incorrect_urls():
    filename = "incorrect_urls.json"
    working_dir = os.getcwd()
    file_path = os.path.join(working_dir, "ufc_data_scraper/data")
    full_path = f"{file_path}/{filename}"

    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as file:
            file_data = json.load(file)

        if should_fetch_latest(file_data.get("last_fetched")):
            incorrect_urls = fetch_latest_urls(full_path)
        else:
            incorrect_urls = file_data.get("incorrect_urls")
    else:
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        incorrect_urls = fetch_latest_urls(full_path)

    return incorrect_urls
