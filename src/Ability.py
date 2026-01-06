from dataclasses import dataclass

@dataclass(frozen=True)
class Ability:
    name: str
    damage: int