from dataclasses import dataclass

from ..character import Character
from ..errors import InsufficientHPError, TargetDefeatedError


@dataclass
class Warrior(Character):
	def attack(self, target: Character, double_attack: bool = False) -> int:
		"""
		Overridden attack to handle the Warrior's unique Double Attack mechanic.

		Args:
			target: The character to attack.
			double_attack: If True, attacks twice but costs 5 HP.

		Returns:
			Return the damage dealt across all strikes.
		"""
		# Execute the first attack using the base class logic
		total_damage = super().attack(target)

		if double_attack:
			# Check if Warrior has enough HP to perform the double attack
			if self.health_points <= 5:
				raise InsufficientHPError(f"{self.name} does not have enough HP for a double attack!")

			self.health_points -= 5

			# Perform the second attack
			# We call super().attack again to ensure the target didn't die from the first hit
			try:
				total_damage += super().attack(target)
			except TargetDefeatedError:
				# If the target died in the first hit, super().attack will raise TargetDefeatedError
				pass

		return total_damage

	def _attack_logic(self, target: Character) -> int:
		"""
		The specific math for a Warrior's strike.
		"""
		ability = self.use_ability()
		damage = ability.damage

		# Apply damage and ensure HP doesn't drop below 0
		target.health_points = max(0, target.health_points - damage)

		return damage
