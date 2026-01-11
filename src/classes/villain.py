import random
from dataclasses import dataclass

from src.classes.character import Character


@dataclass(eq=False)
class Villain(Character):
    def attack(self, target: Character, steal_ability: bool = False) -> int:
        """
        Overridden attack to handle the Villain's unique steal mechanic.

        Args:
            target: The target character
            steal_ability: If to perform steal

        Returns:
            Return the damage dealt across all strikes.
        """
        super().attack(target)

        # Villain specific: Steal an ability
        if steal_ability and target.abilities:
            stolen_ability = random.choice(list(target.abilities))
            target.abilities.remove(stolen_ability)
            # If the ability exist it will not add it
            self.abilities.add(stolen_ability)

        ability = self.use_ability()
        damage = ability.damage

        # Apply damage and ensure HP doesn't drop below 0
        target.health_points = max(0, target.health_points - damage)
        return damage
