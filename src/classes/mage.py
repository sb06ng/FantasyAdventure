from dataclasses import dataclass

from ..character import Character


@dataclass
class Mage(Character):
    def _attack_logic(self, target: Character) -> int:
        """
        Mage attack logic: deals damage and has a chance to heal
        7% of the damage dealt.
        """
        ability = self.use_ability()
        damage = ability.damage

        # Prevent points from going below 0
        target.points = max(0, target.points - damage)

        # Mage specific: Gain 7% of damage dealt back as Points
        points_amount = int(damage * 0.07)
        if points_amount > 0:
            self.points += points_amount
        return damage
