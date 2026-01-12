import random

from src.classes.character import Character
from src.errors.errors import InvalidObjectType, NoWinnerError
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
            InvalidObjectType: If the characters provided are not Character instances.
            NoWinnerError: If the battle ended without a winner.
        """
        team_a = cls._ensure_team(first)
        team_b = cls._ensure_team(second)

        all_fighters = team_a.members + team_b.members

        for fighter in all_fighters:
            if not isinstance(fighter, Character):
                raise InvalidObjectType(f"Fighter must be a Character, not {type(fighter).__name__}")

        action_queue = sorted(all_fighters, key=lambda x: x.speed)

        winner = None

        while winner is None:
            winner = cls._play_round(action_queue, team_a, team_b)

        if isinstance(first, Character) and isinstance(second, Character):
            return winner.members[0]
        # return the team
        return winner

    @classmethod
    def _play_round(cls, action_queue: list[Character], team_a: Team, team_b: Team) -> Team | None:
        """
        Play a round of the battle

        Args:
            action_queue: The list of characters participating.
            team_a: The first team to play in the round.
            team_b: The second team to play in the round.
            
        Returns:
            Character | None: The character who finished the battle, or None.

        Raises:
            NoWinnerError: If the battle ended without a winner.
        """
        count = 0
        for fighter in action_queue:
            if not fighter.is_alive():
                # check if all the fighters are dead
                count += 1
                continue

            fighter_team = team_a if fighter in team_a.members else team_b

            targets = [c for c in action_queue if c.is_alive() and c not in fighter_team.members]

            if not targets:
                # No enemies left? The current fighter's side wins.
                return fighter_team

            target = random.choice(targets)
            total_damage = fighter.attack(target)
            print(f"{fighter.name} attacked {target.name} for {total_damage} damage.")

        if len(action_queue) == count:
            raise NoWinnerError("All fighters are dead")
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
