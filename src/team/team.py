from dataclasses import dataclass, field
from typing import Iterator

from src.entities.character import Character
from src.utils.errors import InvalidMemberError


@dataclass
class Team:
    name: str
    _members: list[Character] = field(default_factory=list)

    @property
    def members(self) -> list[Character]:
        """Returns a read-only copy of the members list."""
        return self._members[:]

    @property
    def active_members(self) -> list[Character]:
        """Returns only the members who are currently alive."""
        return [c for c in self._members if c.is_alive]

    @property
    def is_defeated(self) -> bool:
        """The team is defeated only if NO members are alive."""
        return len(self.active_members) == 0

    def add_member(self, character: Character):
        """
        Adds a new character to the team after validation.

        Args:
            character (Character): The character instance to add to the team.

        Raises:
            InvalidMemberError: If the provided object is not an  instance of the Character class.
        """

        if not isinstance(character, Character):
            raise InvalidMemberError(
                f"Expected Character, got {type(character).__name__}"
            )
        self._members.append(character)

    def __len__(self) -> int:
        return len(self._members)

    def __iter__(self) -> Iterator[Character]:
        """Allows you to loop over the team directly: 'for member in team:'"""
        return iter(self._members)

    def __str__(self) -> str:
        status = "DEFEATED" if self.is_defeated else "ACTIVE"
        member_names = ", ".join(
            [f"{c.name} ({c.health_points} HP)" for c in self._members]
        )
        return f"[{status}] Team {self.name}: {member_names}"
