import logging
import random

from src.config import GameConfig
from src.entities.character import Character, AttackResult

logger: logging.Logger = logging.getLogger(__name__)


class Villain(Character):
    """
    Villain: Has a 50% chance to steal an item from the target after attacking.
    """

    def attack(self, target: Character) -> AttackResult:
        result = super().attack(target)

        if self.is_alive and random.random() < GameConfig.VILLAIN_STEAL_CHANCE:
            self._attempt_steal(target)

        return result

    def _attempt_steal(self, target: Character):
        """Tries to move an item from target's inventory to self."""

        if not target.inventory.items:
            logger.info(
                f"{self.name} checked {target.name}'s pockets, but they were empty."
            )
            return

        try:
            item_stolen = target.inventory.get_item()

            self.inventory.add_item(item_stolen)
            logger.info(f"{self.name} STOLE {item_stolen.name}!")
        except ValueError as e:
            logger.debug(f"Steal failed from {target.name}: {e}")
