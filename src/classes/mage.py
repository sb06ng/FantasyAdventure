from dataclasses import dataclass

from src.classes.character import Character

LIFE_STEAL_AMOUNT = 0.07


@dataclass(eq=False)
class Mage(Character):
    def attack(self, target: Character) -> int:
        """
		Overridden attack to handle the Mage's unique life steal mechanic.

	   Args:
            target: The target character

        Returns:
            Return the damage dealt across all strikes.
        """
        super().attack(target)

        ability = self.use_ability()
        damage = ability.damage

        # Apply damage and ensure HP doesn't drop below 0
        target.health_points = max(0, target.health_points - damage)

        # Mage specific: Gain 7% of damage dealt back as HP
        heal_amount = int(damage * LIFE_STEAL_AMOUNT)
        if heal_amount > 0:
            self.health_points += heal_amount

        return damage
