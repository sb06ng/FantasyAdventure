import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from src.abilities.ability import Ability
from src.errors.errors import DefeatedError, TargetDefeatedError

DEFAULT_HEALTH_POINTS = 15
DEFAULT_LEVEL = 1
DEFAULT_ABILITIES = [Ability("Punch", 5)]


@dataclass
class Character(ABC):
    name: str
    health_points: int = DEFAULT_HEALTH_POINTS
    level: int = DEFAULT_LEVEL
    abilities: set[Ability] = field(default_factory=set)

    def use_ability(self) -> Ability:
        """
        Select Random ability and return it

        Returns:
            the ability
        """
        if not self.abilities:
            # We use .update() because DEFAULT_ABILITIES is a list and abilities is a set
            self.abilities.update(DEFAULT_ABILITIES)

        return random.choice(list(self.abilities))

    @abstractmethod
    def attack(self, target: Character) -> int:
        """
        Decreases target health points
        Returns the damage dealt

        Args:
            target: the target character

        Returns:
            the damage dealt

        Raises:
            TypeError: if target is not a Character
            DefeatedError: if the character is defeated
            TargetDefeatedError: if the target is defeated
        """
        if not isinstance(target, Character):
            raise TypeError(f"Target must be a Character, not {type(target).__name__}")

        if self.health_points <= 0:
            raise DefeatedError(f"{self.name} is defeated and cannot attack!")

        if target.health_points <= 0:
            raise TargetDefeatedError(f"{target.name} is already down; stop hitting them!")
        ...

    def __str__(self) -> str:
        return (
            f"--- Character Profile ---\n"
            f"Name:   {self.name}\n"
            f"Level:  {self.level}\n"
            f"Health: {self.health_points}\n"
            f"Skills: {', '.join([a.name for a in self.abilities]) or 'None'}\n"
            f"-------------------------"
        )

    def __eq__(self, other) -> bool:
        return self is other

    def __hash__(self):
        """
        Allows the object to be used as a dictionary key.
        Hashes based on the object's memory address (identity).
        """
        return id(self)

    def is_alive(self) -> bool:
        return self.health_points > 0
