from ufc_data_scraper.models.base import BaseModel


class Location(BaseModel):
    def __init__(self, venue: str, city: str, country: str, tricode: str) -> None:
        self.venue = venue
        self.city = city
        self.country = country
        self.tricode = tricode

    def __str__(self) -> str:
        return f"{self.venue} - {self.city}, {self.country}"