from src.classes import Mage, Warrior
from src.game.battle import Battle
from src.teams.team import Team


def main():
    # --- Create Characters ---
    # Team Heroes
    hero_warrior = Warrior(name="Aragorn")
    hero_mage = Mage(name="Gandalf")

    # Team Villains
    villain_warrior = Warrior(name="Orc Berserker")
    villain_mage = Mage(name="Saruman")

    # --- Create Teams ---
    fellowship = Team(name="The Fellowship", members=[hero_warrior, hero_mage])
    mordor = Team(name="Mordor", members=[villain_warrior, villain_mage])

    run_battle(fellowship, mordor)

    warrior1 = Warrior(name="Arg")
    warrior2 = Warrior(name="Orc")
    run_battle(warrior1, warrior2)

    villain_warrior.health_points = 100
    villain_mage.health_points = 100
    warrior3 = Warrior(name="hero")

    run_battle(warrior3, mordor)


def run_battle(first, second):
    print(f"Starting Battle: {first.name} vs {second.name} ")
    try:
        # We pass Teams into start() now
        winner = Battle.start(first, second)

        if isinstance(winner, Team):
            print(f"VICTORY! The winner is {winner.name}!")
            print(f"Survivors: {', '.join([m.name for m in winner.members if m.is_alive()])}")
        else:
            # Fallback if 1v1 logic returns a Character
            print(f"VICTORY! The winner is {winner.name}!")

    except Exception as e:
        print(f"\n An error occurred: {e}")
    print("=" * 30)
    print()


if __name__ == "__main__":
    main()
