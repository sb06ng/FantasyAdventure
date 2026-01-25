import logging
from typing import Union

from src.entities.character import Character
from src.team.team import Team
from src.utils.errors import NoWinnerError, InvalidObjectType

# Type alias for cleaner signatures
Participant = Union[Character, Team]

logger: logging.Logger = logging.getLogger("BattleEngine")


class Battle:
    """
    An instance-based Battle Engine.
    Normalizes 1v1 and Team interactions into a single consistent loop.
    """

    def __init__(self, side_a: Participant, side_b: Participant) -> None:
        # We flag if the original input was a single character so we can unwrap the result later.
        self._a_is_single = isinstance(side_a, Character)
        self._b_is_single = isinstance(side_b, Character)

        # "Everything is a Team" - Normalize inputs
        self.team_a: Team = self._ensure_team(side_a)
        self.team_b: Team = self._ensure_team(side_b)

        self.round_number = 0
        self.is_finished = False

    def start(self) -> Participant:
        """
        Executes the battle loop until a winner is determined.
        Returns the specific Character (if 1v1) or Team (if TvT) that won.
        """
        self._validate_start()
        logger.info(f"BATTLE START: {self.team_a.name} VS {self.team_b.name}")

        while True:
            self.round_number += 1
            winner_team = self._play_round()

            if winner_team:
                return self._format_result(winner_team)

    def _play_round(self) -> Team | None:
        """
        Runs one round.
        Returns the Winning Team if the battle ends this round, else None.
        """
        logger.info(f"--- Round {self.round_number} ---")

        fighters = self.team_a.active_members + self.team_b.active_members

        # We re-sort every round to handle buffs/debuffs or new summons
        fighters.sort(key=lambda x: x.speed, reverse=True)

        for fighter in fighters:
            # Check death mid-round (someone might have died before their turn)
            if not fighter.is_alive:
                continue

            # Check win condition immediately before every turn
            # (If the last enemy died from a DoT or previous hit, stop now)
            if self.team_a.is_defeated:
                return self.team_b
            if self.team_b.is_defeated:
                return self.team_a

            self._execute_turn(fighter)

        return None

    def _execute_turn(self, current_fighter: Character):
        """Helper to determine allies/enemies and delegate logic."""
        allies, enemies = self._get_teams_for_fighter(current_fighter)
        current_fighter.take_turn(allies, enemies)

    def _get_teams_for_fighter(self, fighter: Character) -> tuple[Team, Team]:
        """Returns (allies, enemies) for the given fighter."""
        if fighter in self.team_a.members:
            return self.team_a, self.team_b
        return self.team_b, self.team_a

    def _format_result(self, winning_team: Team) -> Participant:
        """
        Unwraps the result.
        If the winner was originally a single Character, return that Character.
        Otherwise, return the Team.
        """
        logger.info(f"VICTORY for {winning_team.name}!")

        # If Side A won and Side A was originally a single character
        if winning_team == self.team_a and self._a_is_single:
            return winning_team.members[0]

        # If Side B won and Side B was originally a single character
        if winning_team == self.team_b and self._b_is_single:
            return winning_team.members[0]

        return winning_team

    def _validate_start(self):
        """Sanity checks before starting."""
        if self.team_a.is_defeated or self.team_b.is_defeated:
            raise NoWinnerError("One or both teams started the battle dead.")

    @staticmethod
    def _ensure_team(participant: Participant) -> Team:
        """Adapts a Character into a temporary Team if necessary."""
        if isinstance(participant, Team):
            return participant
        if isinstance(participant, Character):
            # Create a wrapper team
            temp_team = Team(name=participant.name)
            temp_team.add_member(participant)
            return temp_team

        raise InvalidObjectType(f"Invalid participant type: {type(participant)}")
