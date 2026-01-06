import logging
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .ability import Ability

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("GameLogic")


@dataclass
class Character(ABC):
    name: str
    health_points: int
    level: int
    abilities: set[Ability] = field(default_factory=set)

    def use_ability(self) -> int:
        """Selects a random ability and returns its point value."""
        if not self.abilities:
            logger.warning(f"{self.name} has no abilities to use!")
            return 0

        ability = random.choice(list(self.abilities))
        logger.info(f"{self.name} prepares to use '{ability.name}' (Damage: {ability.damage})")
        return ability.damage

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
        """
        
        if not isinstance(target, Character):
            raise TypeError(f"Target must be an instance of Character, not {type(target).__name__}")

        # Attacker is already defeated
        if self.health_points <= 0:
            logger.error(f"{self.name} cannot attack because they are defeated!")
            return 0

        # Target is already defeated
        if target.health_points <= 0:
            logger.info(f"{self.name} tried to attack {target.name}, but they are already down.")
            return 0

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