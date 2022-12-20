from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class StrikeTarget:
    head: int
    head_per: int
    body: int
    body_per: int
    leg: int
    leg_per: int
