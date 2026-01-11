from src.abilities.ability import Ability
from src.classes.warrior import Warrior
from src.classes.mage import Mage
from src.teams.team import Team
from src.game.battle import Battle


def main():
    # --- Create Abilities ---
    slash = Ability(name="Slash", damage=10)
    fireball = Ability(name="Fireball", damage=25)
    ice_shard = Ability(name="Ice Shard", damage=15)
    smash = Ability(name="Smash", damage=8)

    # --- Create Characters ---
    # Team Heroes
    hero_warrior = Warrior(name="Aragorn", abilities={slash, smash})
    hero_mage = Mage(name="Gandalf", abilities={fireball})

    # Team Villains
    villain_warrior = Warrior(name="Orc Berserker", abilities={slash})
    villain_mage = Mage(name="Saruman", abilities={ice_shard, fireball})

    # --- Create Teams ---
    fellowship = Team(name="The Fellowship", members=[hero_warrior, hero_mage])
    mordor = Team(name="Mordor", members=[villain_warrior, villain_mage])

    run_battle(fellowship, mordor)

    run_battle(hero_warrior, villain_warrior)

    run_battle(hero_warrior, mordor)


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
