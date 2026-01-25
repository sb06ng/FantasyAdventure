import logging

from src.config import GameConfig
from src.entities.character import Character, AttackResult

logger: logging.Logger = logging.getLogger(__name__)


class Mage(Character):
    """
    Mage: Heals for 7% of the damage dealt.
    """

    def attack(self, target: Character) -> AttackResult:
        result = super().attack(target)

        heal_amount = int(result.ability_used.damage * GameConfig.MAGE_LIFESTEAL_PCT)

        if heal_amount > 0 and self.is_alive:
            self.heal(heal_amount)
            logger.info(f"{self.name} drained {heal_amount} HP from {target.name}!")

        return result
