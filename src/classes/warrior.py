import random
from dataclasses import dataclass

from src import Ability
from src.abilities.catalog import DEFAULT_WARRIOR_SET
from src.classes.character import Character
from src.errors.errors import TargetDefeatedError

SKILL_CHANCE = 33


@dataclass(eq=False)
class Warrior(Character):
    """ Warrior's character.
        Has 33% chance to double attack, would not happen if warrior has 5 or less hp
    """

    def __post_init__(self):
        """
        We ensure the defaults are added to whatever the user provided.
        """
        self.abilities.update(DEFAULT_WARRIOR_SET)

    def attack(self, target: Character) -> int:
        """
        Overridden attack to handle the Warrior's unique Double Attack mechanic.

        Args:
            target: The character to attack.

        Returns:
            Return the damage dealt across all strikes.
        """
        super().attack(target)

        total_damage = self._attack_logic(target)
        # Check if Warrior has enough HP to perform the double attack
        if self.health_points <= 5:
            if random.randint(0, 100) <= SKILL_CHANCE:
                self.health_points -= 5
                # We perform the second attack by calling this function again (without the flag)
                try:
                    total_damage += self._attack_logic(target)
                except TargetDefeatedError:
                    # If the target died in the first hit, attack will raise TargetDefeatedError
                    self.health_points += 5
                    pass

        return total_damage
