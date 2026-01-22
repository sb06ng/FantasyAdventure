import logging
import random
from typing import Final

from src.config import GameConfig
from src.data.item import Item

logger: logging.Logger = logging.getLogger(__name__)


class Inventory:
    def __init__(self, capacity: int = GameConfig.INVENTORY_CAPACITY) -> None:
        self._items: list[Item] = []
        self._capacity: Final[int] = capacity

    @property
    def items(self) -> list[Item]:
        """Return a read-only view of items to prevent external messing."""
        return self._items[:]

    @property
    def is_full(self) -> bool:
        return len(self._items) >= self._capacity

    def add_item(self, item: Item) -> bool:
        """
        Adds an item if space permits.
        Returns True if successful, False if inventory is full.
        """
        if self.is_full:
            logger.info(f"Inventory full! Cannot pick up {item.name}.")
            return False
        self._items.append(item)
        return True

    def remove_item(self, item: Item) -> None:
        """Removes a specific item instance."""
        if item in self._items:
            self._items.remove(item)
        else:
            raise ValueError(f"Item {item.name} not found in inventory.")

    def get_item(self) -> Item:
        """Retrieves and removes a random item"""
        if not self._items:
            raise ValueError("Inventory is empty")

        item = random.choice(self._items)
        self.remove_item(item)
        return item

    def __str__(self):
        if not self._items:
            return "Inventory: <Empty>"
        item_list = ", ".join([str(i) for i in self._items])
        return f"Inventory ({len(self._items)}/{self._capacity}): {item_list}"
