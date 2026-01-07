import random

from src.classes.character import Character
from src.errors.errors import NoWinnerError

MINIMUM_ROUNDS = 3
MAXIMUM_ROUNDS = 7


class Battle:
    _action_queue = set[Character]
    _number_of_rounds = 0

    def start(self, first_team: set[Character], second_team: set[Character]) -> Character:
        """
        Do the battle logic and return the winner


        Args:
            first_team: a set represent the first team of fighters
            second_team:  a set represent the second team of fighters

        Returns:
            A Character from the team that won

        Raises:
            TypeError: if the characters provided is not a Character instance
            NoWinnerError: if no winner is available (when there is a tie)
            NoAbilityError: if one character have no abilities
        """
        for fighter in first_team.union(second_team):
            if not isinstance(fighter, Character):
                raise TypeError(f"Fighter must be a Character, not {type(fighter).__name__}")

        self._action_queue = [c for c in first_team.union(second_team) if c.is_alive()]

        self._number_of_rounds = random.randint(MINIMUM_ROUNDS, MAXIMUM_ROUNDS)

        for round_number in range(self._number_of_rounds):
            fighter = self._play_round()
            if fighter is not None:
                return fighter

        raise NoWinnerError(f"No winner found for battle")

    def _play_round(self) -> Character | None:
        """
        Play a round of the battle

        Returns:
            Return a Character from the party that won, and it is his turn. Otherwise None
        """
        for fighter in self._action_queue:
            if not fighter.is_alive():
                continue

            targets = [c for c in self._action_queue if c.is_alive() and c.team != fighter.team]

            if not targets:
                # if targets empty, fight party won
                return fighter

            target = random.choice(targets)
            fighter.attack(target)

        return None
