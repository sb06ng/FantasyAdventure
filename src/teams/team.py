from dataclasses import dataclass, field

from src.classes import Character
from src.errors.errors import InvalidMemberError


@dataclass
class Team:
    name: str
    members: list[Character] = field(default_factory=set)

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
                f"Expected a Character instance, but got {type(character).__name__}."
            )
        self.members.append(character)

    def __str__(self) -> str:
        """Returns a string representation of the team."""
        member_names = ", ".join([c.name for c in self.members]) or "No members"
        return f"Team '{self.name}' | Members: [{member_names}]"

    def __eq__(self, other: Team) -> bool:
        return self.name == other.name

    def is_alive(self) -> bool:
        """Returns whether the team is alive."""
        for member in self.members:
            if not member.is_alive():
                return False
        return True
