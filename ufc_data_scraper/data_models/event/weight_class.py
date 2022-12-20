from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class WeightClass():
    description: str
    abbreviation: str
    weight: str