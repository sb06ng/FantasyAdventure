import random
from dataclasses import dataclass

from ..character import Character


@dataclass
class Villain(Character):
    def attack(self, target: Character, steal_ability: bool = False) -> int:
        """
        Overridden attack to handle the Villain's ability theft.
        """
        # Execute the base attack first
        damage = super().attack(target)

        # Villain specific: Steal an ability if requested and target has them
        if steal_ability and target.abilities:
            stolen_ability = random.choice(list(target.abilities))
            target.abilities.remove(stolen_ability)
            # If the ability exist it will not add it
            self.abilities.add(stolen_ability)

        return damage

    def _attack_logic(self, target: Character) -> int:
        ability = self.use_ability()
        damage = ability.damage

        # Prevent points from going below 0
        target.points = max(0, target.points - damage)

        return damage
