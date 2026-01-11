import random

from src.classes.character import Character
from src.errors.errors import NoWinnerError, InvalidObjectType
from src.teams.team import Team

MINIMUM_ROUNDS = 3
MAXIMUM_ROUNDS = 7


class Battle:
    """
    Handles combat logic between individual Characters or Teams.
    """

    @classmethod
    def start(cls, first: Team | Character, second: Team | Character) -> Team | Character:
        """
        Starts the battle logic and returns the winner (Character or Team).

        Args:
            first: The first participant (Character or Team).
            second: The second participant (Character or Team).

        Returns:
            Character | Team: The winning Character (if 1v1) or the winning Team.

        Raises:
            TypeError: If the characters provided are not Character instances.
            NoWinnerError: If the maximum rounds are reached with no clear winner.
        """
        team_a = cls._ensure_team(first)
        team_b = cls._ensure_team(second)

        team_lookup: dict[Character, Team] = {}
        all_fighters = team_a.members + team_b.members

        for fighter in all_fighters:
            if not isinstance(fighter, Character):
                raise TypeError(f"Fighter must be a Character, not {type(fighter).__name__}")
            team_lookup[fighter] = team_a if fighter in team_a.members else team_b

        action_queue = [c for c in all_fighters if c.is_alive()]
        num_rounds = random.randint(MINIMUM_ROUNDS, MAXIMUM_ROUNDS)

        for _ in range(num_rounds):
            winner_char = cls._play_round(action_queue, team_lookup)

            if winner_char is not None:
                if isinstance(first, Character) and isinstance(second, Character):
                    return winner_char
                return team_lookup[winner_char]

        raise NoWinnerError("The battle timed out without a clear winner.")

    @classmethod
    def _play_round(cls, action_queue: list[Character], team_lookup: dict[Character, Team]) -> Character | None:
        """
        Play a round of the battle

        Args:
            action_queue: The list of characters participating.
            team_lookup: Mapping of characters to their teams.
            
        Returns:
            Character | None: The character who finished the battle, or None.
        """
        random.shuffle(action_queue)

        for fighter in action_queue:
            if not fighter.is_alive():
                continue

            my_team = team_lookup[fighter]
            targets = [c for c in action_queue if c.is_alive() and team_lookup[c] != my_team]

            if not targets:
                # No enemies left? The current fighter's side wins.
                return fighter

            target = random.choice(targets)
            fighter.attack(target)

        return None

    @staticmethod
    def _ensure_team(participant: Character | Team) -> Team:
        """
        Wraps a Character in a Team object if it isn't one already.

        Args:
            participant: A Character or Team instance.

        Returns:
            Team: A team containing the participant(s).
        """
        if isinstance(participant, Team):
            return participant
        if isinstance(participant, Character):
            return Team(participant.name, [participant])

        raise InvalidObjectType(f"Expected Character or Team, got {type(participant).__name__}")
