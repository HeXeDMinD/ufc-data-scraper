from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Accolade:
    description: str
    type: str
