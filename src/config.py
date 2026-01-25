from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    # Character stats
    DEFAULT_HP: int = 100
    DEFAULT_SPEED: int = 1
    DEFAULT_LEVEL: int = 1

    # Progression
    XP_BASE: int = 10
    XP_REQ_BASE: int = 100
    HP_GAIN_MIN: int = 15
    HP_GAIN_MAX: int = 30

    # Items & drops
    ITEM_DROP_RATE: float = 0.5
    INVENTORY_CAPACITY: int = 10

    # Class-specific
    MAGE_LIFESTEAL_PCT: float = 0.07
    WARRIOR_DOUBLE_ATTACK_CHANCE: float = 0.4
    WARRIOR_RECOIL_DAMAGE: int = 5
    WARRIOR_RECOIL_TAG = "recoil"
    VILLAIN_STEAL_CHANCE: float = 0.5

    # Engine
    ITEM_USE_CHANCE: float = 0.2


# Singleton instance
config = GameConfig()
