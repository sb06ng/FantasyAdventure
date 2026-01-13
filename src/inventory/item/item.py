from dataclasses import dataclass
from enum import Enum, auto

DEFAULT_DURABILITY = 3


class TargetType(Enum):
    ALLY = auto()
    ENEMY = auto()


@dataclass
class Item:
    name: str
    description: str
    effect: int
    target_type: TargetType
    durability: int = DEFAULT_DURABILITY

    def __str__(self):
        return f'{self.name}, it have {self.durability} durability. and {self.description} for {self.effect}'

    def get_effect(self) -> int:
        """
        Returns the effect amount
        if the items deal damage it returns a negative effect
        """
        if self.target_type == TargetType.ENEMY:
            return self.effect * -1
        return self.effect
