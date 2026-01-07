import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .ability import Ability
from .errors import NoAbilitiesError, DefeatedError, TargetDefeatedError


@dataclass
class Character(ABC):
    name: str
    health_points: int
    level: int
    abilities: set[Ability] = field(default_factory=set)

    def use_ability(self) -> Ability:
        """
        Select Random ability and return it

        Returns:
            the ability

        Raises:
            NoAbilities: if no ability for this character
        """
        try:
            ability = random.choice(list(self.abilities))
            return ability
        except IndexError as e:
            raise NoAbilitiesError(f"Action failed: {self.name} has no abilities available.") from e

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

        return self._attack_logic(target)

    @abstractmethod
    def _attack_logic(self, target: Character) -> int:
        """
        Preform the logic of the attack on the character

        Args:
            target: the target character

        Returns:
            the damage dealt
        """
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
        """
        Compare two characters by level

        Args:
            other: the other character

        Returns:
            True if they are equal.
        """
        return self.level == other.level
