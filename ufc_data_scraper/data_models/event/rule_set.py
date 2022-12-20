from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class RuleSet():
    description: str
    possible_rounds: str