from __future__ import annotations

import logging
import random
from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.config import GameConfig
from src.data.ability import Ability, AbilityLibrary
from src.data.item import Item, ItemLibrary
from src.engine.controller import RandomAI, Controller
from src.entities.inventory import Inventory
from src.team.target_type import TargetType
from src.utils.errors import (
    TargetDefeatedError,
    DefeatedError,
    InvalidObjectType,
    ItemIsBrokenError,
)

if TYPE_CHECKING:
    from src.team.team import Team

logger: logging.Logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AttackResult:
    """Structure to return detailed outcome of an attack."""

    attacker_name: str
    target_name: str
    ability_used: Ability
    target_defeated: bool
    xp_gained: int = 0
    leveled_up: bool = False


@dataclass
class Character(ABC):
    """
    Abstract Base Class for all game entities.
    Implements core RPG logic: Health, Inventory, Leveling, and Turn-taking.
    """

    name: str
    _health_points: int = int(GameConfig.DEFAULT_HP)
    _max_health: int = int(GameConfig.DEFAULT_HP)
    speed: int = int(GameConfig.DEFAULT_SPEED)
    _level: int = int(GameConfig.DEFAULT_LEVEL)
    _xp: int = 0

    abilities: set[Ability] = field(default_factory=set)
    inventory: Inventory = field(default_factory=Inventory)

    controller: Controller = field(default_factory=RandomAI, repr=False)

    def __post_init__(self):
        """Initialize abilities once to avoid overhead."""
        self._load_initial_abilities()

    def _load_initial_abilities(self) -> None:
        """Hydrates abilities from the library based on class name."""
        preset = AbilityLibrary.get_preset(self.__class__.__name__)
        if preset:
            self.abilities.update(preset)

    @property
    def health_points(self) -> int:
        return self._health_points

    @property
    def level(self) -> int:
        return self._level

    @property
    def is_alive(self) -> bool:
        return self._health_points > 0

    def receive_damage(self, amount: int) -> bool:
        """
        Safely reduces HP.
        Returns True if the character was defeated by this specific damage.
        """
        self._health_points = max(0, self._health_points - amount)
        if self._health_points == 0:
            logger.info(f"{self.name} has been defeated.")
            return True
        return False

    def heal(self, amount: int) -> None:
        """Safely increases HP up to max."""
        if not self.is_alive:
            return  # Cannot heal the dead

        previous_hp = self._health_points
        self._health_points = min(self._max_health, self._health_points + amount)
        logger.debug(f"{self.name} healed for {self._health_points - previous_hp} HP.")

    def attack(self, target: Character) -> AttackResult:
        """
        Template Method: Handles validation, execution, and progression.
        Concrete subclasses must implement `_calculate_damage`.
        """
        self._validate_attack_conditions(target)

        ability = self._get_ability()

        killed = target.receive_damage(ability.damage)

        xp_gained = int(GameConfig.XP_BASE)
        self._xp += xp_gained
        leveled_up = self._check_level_up()

        return AttackResult(
            attacker_name=self.name,
            target_name=target.name,
            ability_used=ability,
            target_defeated=killed,
            xp_gained=xp_gained,
            leveled_up=leveled_up,
        )

    def _get_ability(self) -> Ability:
        return random.choice(list(self.abilities))

    def _validate_attack_conditions(self, target: Character) -> None:
        if not isinstance(target, Character):
            raise InvalidObjectType(f"Target must be Character, got {type(target)}")
        if not self.is_alive:
            raise DefeatedError(f"{self.name} is defeated and cannot act.")
        if not target.is_alive:
            raise TargetDefeatedError(f"{target.name} is already defeated.")

    def take_turn(self, allies: Team, enemies: Team) -> None:
        if not self.is_alive:
            return
        self.controller.act(self, allies, enemies)

    def use_item(self, item: Item, target: Character):
        try:
            effect_value = item.get_effect()
            item.use()

            if item.target_type == TargetType.ENEMY:
                target.receive_damage(effect_value)
                logger.info(
                    f"{self.name} damaged {target.name} for {effect_value} with {item.name}!"
                )
            else:
                target.heal(effect_value)
                logger.info(
                    f"{self.name} healed {target.name} for {effect_value} with {item.name}."
                )

            if not item.is_broken:
                self.inventory.add_item(item)
            else:
                logger.info(f"{self.name}'s {item.name} shattered!")

        except ItemIsBrokenError as e:
            logger.error(f"Cannot use broken item: {e}")
        except ValueError as e:
            logger.error(f"Invalid item usage: {e}")

    def _check_level_up(self) -> bool:
        """Checks if XP threshold is met and performs level up."""
        required_xp = int(GameConfig.XP_REQ_BASE) + int(
            GameConfig.XP_BASE * self._level
        )

        if self._xp >= required_xp:
            self._xp -= required_xp
            self._perform_level_up()
            return True
        return False

    def _perform_level_up(self):
        self._level += 1

        # Reward: Item or Stats
        if random.random() < GameConfig.ITEM_DROP_RATE:
            new_item = ItemLibrary.get_random_item()
            self.inventory.add_item(new_item)
            logger.info(
                f"LEVEL UP: {self.name} reached lvl {self.level} and found {new_item.name}!"
            )
        else:
            hp_gain = random.randint(GameConfig.HP_GAIN_MIN, GameConfig.HP_GAIN_MAX)
            self._max_health += hp_gain
            self._health_points = self._max_health
            logger.info(
                f"LEVEL UP: {self.name} reached lvl {self.level} and gained {hp_gain} Max HP."
            )

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other

    def __str__(self) -> str:
        ability_names = ", ".join([a.name for a in self.abilities]) or "None"
        return (
            f"--- {self.name} (Lvl {self.level}) ---\n"
            f"HP: {self.health_points}/{self._max_health} | XP: {self._xp}\n"
            f"Abilities: {ability_names}\n"
        )
