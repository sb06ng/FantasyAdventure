from __future__ import annotations

import logging
import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.config import GameConfig
from src.data.item import Item
from src.team.target_type import TargetType

if TYPE_CHECKING:
    from src.entities.character import Character
    from src.team.team import Team

logger: logging.Logger = logging.getLogger(__name__)


class Controller(ABC):
    @abstractmethod
    def act(self, actor: Character, allies: Team, enemies: Team):
        """Decide what the actor should do."""
        pass


class RandomAI(Controller):
    @classmethod
    def act(cls, actor: Character, allies: Team, enemies: Team):
        if actor.inventory.items and random.random() < GameConfig.ITEM_USE_CHANCE:
            item = actor.inventory.get_item()
            target = cls._pick_item_target(actor, item, allies, enemies)
            actor.use_item(item, target)
        else:
            target = random.choice(enemies.active_members)
            attack_result = actor.attack(target)
            logger.info(
                f"{attack_result.attacker_name} attacked {attack_result.target_name} with {attack_result.ability_used.name} for {attack_result.ability_used.damage}."
            )
            if attack_result.target_defeated:
                logger.info(f"{attack_result.target_name} died.")
            if attack_result.leveled_up:
                logger.info(f"{attack_result.attacker_name} leveled up.")

    @classmethod
    def _pick_item_target(
        cls, actor: Character, item: Item, allies: Team, enemies: Team
    ):
        """Simple target logic"""
        if item.target_type == TargetType.ENEMY:
            return random.choice(enemies.active_members)
        elif item.target_type == TargetType.ALLY:
            return random.choice(allies.active_members)
        return actor
