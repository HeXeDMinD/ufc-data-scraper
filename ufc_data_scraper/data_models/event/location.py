from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Location():
    venue: str
    city: str
    country: str
    tricode: str