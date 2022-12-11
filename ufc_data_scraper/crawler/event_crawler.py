import json
import requests
import re
import pytz

from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime, timedelta

class _EventCrawler():
    def __init__(self, event_url: str) -> None:
        """Finds UFC event fmids and urls and adds them to a list."""

        self._event_url = event_url

    def _page_is_valid(self, soup: BeautifulSoup) -> bool:
        """Checks if page is empty"""
        
        return soup.find("h3") and True or False
    
    def _get_event_urls(self, page_num: int) -> None:
        """Queries events with page_num and adds event urls to list.

        Args:
            page_num (int): Page number for query.
        """
        
        page_query = {"page": page_num}

        site_response = requests.get("http://www.ufc.com/events", params=page_query)

        if site_response.status_code != 200:
            return

        only_headlines = SoupStrainer(
            "h3", attrs={"class": "c-card-event--result__headline"}
        )
        soup = BeautifulSoup(
            site_response.text, "html.parser", parse_only=only_headlines
        )

        if not self._page_is_valid(soup):
            return

        headlines = list(soup)

        event_urls = []

        for item in headlines:
            url = item.find("a")["href"]
            url = f"http://www.ufc.com{url}"
            if url not in event_urls:
                event_urls.append(url)
                
        return event_urls
    
    def _get_last_fmid(self) -> int:
        """Returns last available fmid from UFC events page."""
        
        last_fmid = None

        recent_events = self._get_event_urls(page_num=0)
        
        for event_url in recent_events:
            current_fmid = self._scrape_event_fmid(event_url)
            if not current_fmid:
                break
            
            if last_fmid == None or current_fmid > last_fmid:
                last_fmid = current_fmid
        
        return last_fmid
    
    def _get_event_data(self, event_fmid: int) -> dict:
        """Queries private API and returns json data in dict format.

        Args:
            event_fmid (int): fmid to query

        Returns:
            dict: Event data json in dict format
        """

        events_endpoint = (
            f"http://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{event_fmid}.json"
        )
        response_date = requests.get(events_endpoint)

        return response_date.json().get("LiveEventDetail")
 
    def _get_event_date(self, soup: BeautifulSoup) -> str:
        """Returns event date.

        Returns:
            str: date_time_obj.strftime("%Y %b %d")
        """

        event_start = None

        target = soup.select(
            "#block-mainpagecontent > div > div.c-hero > div.c-hero__container > div > div.c-hero__bottom-text > div.c-hero__headline-suffix.tz-change-inner"
        )

        if len(target) > 0:
            event_start = target[0].get_text().strip()

        return event_start
   
    def _convert_date(self, date: str) -> str:
        """Converts scraped event date into usable format.

        Returns:
            str: date_time_obj.strftime("%Y %b %d")
        """
        
        date_now = datetime.now()
        year = date_now.year

        date = date.split(",")[1].strip()
        date = " ".join(date.split()[:-1])
        date = f"{year} {date}"

        tz = pytz.timezone("EST")

        date_time_obj = datetime.strptime(date, "%Y %b %d / %I:%M %p")

        # Check for wrap around and match years.
        if date_time_obj.month < date_now.month:
            date_time_obj += timedelta(days=365)

        date_time_obj = date_time_obj.replace(tzinfo=tz)

        date_time_obj = date_time_obj.astimezone(pytz.timezone("GMT"))

        return date_time_obj

    def _start_time_to_date(self, start_time: str):
        """Converts API response date into usable format.

        Returns:
            str: date_time_obj.strftime("%Y %b %d")
        """

        date_obj = None

        if start_time:
            date_obj = datetime.strptime(start_time, "%Y-%m-%dT%H:%MZ")
            date_obj = pytz.timezone("GMT").localize(date_obj)

        return date_obj

    def _scrape_event_fmid(self, event_url: str) -> int:
        """Gets event fmids from url, fmid can be used as API query."""
        
        site_response = requests.get(event_url)

        site_response.raise_for_status()

        only_script = SoupStrainer("script", attrs={"type": "application/json"})
        soup = BeautifulSoup(site_response.text, "html.parser", parse_only=only_script)

        site_scripts = json.loads(list(soup)[-1].text)
        try:
            fmid = int(site_scripts["eventLiveStats"]["event_fmid"])
        except KeyError:
            fmid = None

        return fmid
    
    def _brute_force_event_fmid(self) -> int:
        # TODO - Documentation
        current_fmid = self._get_last_fmid() - 20

        while True:
            data = self._get_event_data(current_fmid)

            if not data or (data and len(data) < 1):
                break

            site_response = requests.get(self._event_url)
            
            site_response.raise_for_status()

            soup = BeautifulSoup(site_response.content, "html.parser")
            
            scraped_date = self._get_event_date(soup)
            scraped_date = self._convert_date(scraped_date)
            if scraped_date:
                api_date = self._start_time_to_date(start_time=data["StartTime"])
                if scraped_date - api_date <= timedelta(days=2):
                    return current_fmid

            current_fmid += 1
        return None
    
    def get_event_fmid(self) -> int:
        """Gets event fmids from url, fmid can be used as API query."""
        
        fmid = self._scrape_event_fmid(self._event_url) or self._brute_force_event_fmid()
        if not fmid:
            raise Exception(f"FMID could not be found for event url. {self._event_url}")
            
        return fmid