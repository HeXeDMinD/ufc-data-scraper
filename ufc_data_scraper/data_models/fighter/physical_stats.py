from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class PhysicalStats():
    age: int
    height: float
    weight: float
    reach: float
    leg_reach: float