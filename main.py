import logging
import sys

from src.data.item import ItemLibrary
from src.engine.battle import Battle
from src.entities.jobs.mage import Mage
from src.entities.jobs.villain import Villain
from src.entities.jobs.warrior import Warrior
from src.team.team import Team

# This ensures we see the battle logs in the console
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def main():
    conan = Warrior(name="Conan", speed=12)
    conan.inventory.add_item(ItemLibrary.get_random_item())

    merlin = Mage(name="Merlin", speed=10)

    joker = Villain(name="Joker", speed=14)

    minion = Warrior(name="Henchman", speed=8)
    minion.inventory.add_item(ItemLibrary.get_random_item())

    heroes_team = Team(name="The Guardians")
    heroes_team.add_member(conan)
    heroes_team.add_member(merlin)

    villains_team = Team(name="The Syndicate")
    villains_team.add_member(joker)
    villains_team.add_member(minion)

    engine = Battle(heroes_team, villains_team)

    winner = engine.start()

    print("\n" + "=" * 30)
    print(f"GAME OVER! The winner is: {winner.name}")
    print("=" * 30)

    for survivor in winner.members:
        if survivor.is_alive:
            print(f"{survivor.name}: {survivor.health_points} HP remaining.")


if __name__ == "__main__":
    main()
