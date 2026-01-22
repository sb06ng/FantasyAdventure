import random
from dataclasses import dataclass, replace

from src.team.target_type import TargetType
from src.utils.errors import ItemIsBrokenError


@dataclass
class Item:
    name: str
    description: str
    value: int  # The magnitude of the effect (e.g., Heal amount or Damage boost)
    target_type: TargetType
    durability: int = 1
    max_durability: int = 1

    def get_effect(self) -> int:
        """Calculates effect and degrades durability."""
        if self.is_broken:
            raise ItemIsBrokenError(f"The {self.name} is broken and cannot be used.")

        return self.value

    @property
    def is_broken(self) -> bool:
        return self.durability <= 0

    def use(self) -> None:
        """Explicitly degrade durability."""
        if not self.is_broken:
            self.durability -= 1

    def repair(self) -> None:
        self.durability = self.max_durability

    def __str__(self):
        status = (
            "Broken" if self.is_broken else f"{self.durability}/{self.max_durability}"
        )
        return f"[{self.name} | {status}]"


class ItemLibrary:
    """Factory to generate fresh items."""

    @staticmethod
    def get_random_item() -> Item:
        common_items = [
            Item(
                "Health Potion",
                "Restores HP",
                value=20,
                target_type=TargetType.ALLY,
                durability=1,
                max_durability=1,
            ),
            Item(
                "Iron Shield",
                "Blocks Damage",
                value=10,
                target_type=TargetType.SELF,
                durability=3,
                max_durability=3,
            ),
            Item(
                "Throwing Knife",
                "Deals Damage",
                value=15,
                target_type=TargetType.ENEMY,
                durability=1,
                max_durability=1,
            ),
            Item(
                name="Goblin Bomb",
                description="Explodes on enemies",
                value=25,
                target_type=TargetType.ENEMY,
                durability=1,
                max_durability=1,
            ),
        ]
        # Return a new instance, not a reference to the list above
        template = random.choice(common_items)
        return replace(template)
