import logging
import random

from src.config import GameConfig
from src.data.ability import Ability
from src.entities.character import Character, AttackResult

logger: logging.Logger = logging.getLogger(__name__)


class Warrior(Character):
    """
    Warrior: Has a chance to Double Attack.
    If Double Attack triggers, they take 5 Recoil Damage.
    """

    def attack(self, target: Character) -> AttackResult:
        """
        Executes the attack.
        Checks if the ability used was a "Double" ability to trigger recoil.
        """
        result = super().attack(target)

        if "recoil" in result.ability_used.tags:
            logger.info(
                f"{self.name} exerts too much force and takes {GameConfig.WARRIOR_RECOIL_DAMAGE} recoil damage!"
            )
            self.receive_damage(GameConfig.WARRIOR_RECOIL_DAMAGE)

        return result

    def _get_ability(self) -> Ability:
        """
        Overrides the standard ability selection to potentially double the attack.
        """
        # Get a standard ability from the parent logic
        base_ability = super()._get_ability()

        # Roll for Double Attack
        if random.random() < GameConfig.WARRIOR_DOUBLE_ATTACK_CHANCE:
            # Create a temporary, stronger version of the ability on the fly
            return Ability(
                name=f"Double {base_ability.name}",
                damage=base_ability.damage * 2,
                description=f"A powerful double strike of {base_ability.name}",
                tags=(GameConfig.WARRIOR_RECOIL_TAG,),
            )

        return base_ability
