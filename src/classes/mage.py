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

		# Apply damage to target
		target.health_points = max(0, target.health_points - damage)

		# Mage specific: Gain 7% of damage dealt back as HP
		heal_amount = int(damage * 0.07)
		if heal_amount > 0:
			self.health_points += heal_amount

		return damage
