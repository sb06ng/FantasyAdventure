import random
from dataclasses import dataclass

from src.classes.character import Character

SKILL_CHANCE = 10


@dataclass(eq=False)
class Villain(Character):
    def attack(self, target: Character) -> int:
        """
        Overridden attack to handle the Villain's unique steal mechanic.

        Args:
            target: The target character

        Returns:
            Return the damage dealt across all strikes.
        """
        super().attack(target)

        # Villain specific skill: Steal an ability
        if random.randint(0, 100) <= SKILL_CHANCE:
            stolen_ability = random.choice(list(target.abilities))
            target.abilities.remove(stolen_ability)
            # If the ability exist it will not add it
            self.abilities.add(stolen_ability)

        return self._attack_logic(target)
