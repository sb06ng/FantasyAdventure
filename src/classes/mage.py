from dataclasses import dataclass

from src import Ability
from src.abilities.catalog import DEFAULT_MAGE_SET
from src.classes.character import Character

LIFE_STEAL_AMOUNT = 0.07


@dataclass(eq=False)
class Mage(Character):
    def __post_init__(self):
        """
        We ensure the defaults are added to whatever the user provided.
        """
        self.abilities.update(DEFAULT_MAGE_SET)

    def attack(self, target: Character) -> int:
        """
		Overridden attack to handle the Mage's unique life steal mechanic.

	   Args:
            target: The target character

        Returns:
            Return the damage dealt across all strikes.
        """
        super().attack(target)

        total_damage = self._attack_logic(target)
        # Mage specific: Gain 7% of damage dealt back as HP
        heal_amount = int(total_damage * LIFE_STEAL_AMOUNT)
        if heal_amount > 0:
            self.health_points += heal_amount

        return total_damage
