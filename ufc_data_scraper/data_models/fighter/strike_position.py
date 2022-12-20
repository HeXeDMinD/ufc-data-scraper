from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class StrikePosition():
    standing: int
    standing_per: int
    clinch: int
    clinch_per: int
    ground: int
    ground_per: int