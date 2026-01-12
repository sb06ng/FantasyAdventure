import random

from src.inventory.item.item import Item, TargetType


class ItemLibrary(Item):
    _ITEMS = {
        "Health potion": Item(name="Healing Potion", description="Heals the target",
                              effect=20, target_type=TargetType.ALLY, durability=1),
        "Sword": Item(name="Sword", description="Deals damage to the target",
                      effect=20, target_type=TargetType.ENEMY, durability=30),
    }

    @classmethod
    def get(cls, item_id: str) -> Item:
        """ Returns an Item by item_id """
        return cls._ITEMS.get(item_id.lower())

    @classmethod
    def get_random_item(cls) -> Item:
        """ Returns a random Item """
        return random.choice(list(cls._ITEMS))
