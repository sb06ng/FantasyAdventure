import random
from dataclasses import dataclass, field

from src.inventory.item.item import Item


@dataclass
class Inventory:
    items: list[Item] = field(default_factory=list)

    def add_item(self, item: Item):
        if not isinstance(item, Item):
            raise TypeError("Item must be of type Item.")
        self.items.append(item)

    def remove_item(self, item: Item):
        self.items.remove(item)

    def get_item(self) -> Item:
        selected_item = random.choice(self.items)
        self.remove_item(selected_item)
        return selected_item

    def show_inventory(self):
        print("The inventory:")
        for item in self.items:
            print(item)
