from dataclasses import dataclass

from src.classes.character import Character
from src.errors.errors import InsufficientHPError, TargetDefeatedError


@dataclass(eq=False)
class Warrior(Character):
    def attack(self, target: Character, double_attack: bool = False) -> int:
        """
        Overridden attack to handle the Warrior's unique Double Attack mechanic.

        Args:
            target: The character to attack.
            double_attack: If True, attacks twice but costs 5 HP.

        Returns:
            Return the damage dealt across all strikes.

        Raises:
            InsufficientHPError: If the target does not have enough HP to perform the second attack.
        """
        super().attack(target)

        # perform first attack
        ability = self.use_ability()
        total_damage = ability.damage

        # Apply damage and ensure HP doesn't drop below 0
        target.health_points = max(0, target.health_points - total_damage)

        if double_attack:
            # Check if Warrior has enough HP to perform the double attack
            if self.health_points <= 5:
                raise InsufficientHPError(f"{self.name} does not have enough HP for a double attack!")

            self.health_points -= 5

            # We perform the second attack by calling this function again (without the flag)
            try:
                total_damage += self.attack(target, double_attack=False)
            except TargetDefeatedError:
                # If the target died in the first hit, attack will raise TargetDefeatedError
                pass

        return total_damage
