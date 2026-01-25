from dataclasses import dataclass, field


@dataclass(frozen=True)
class Ability:
    """
    Represents a skill a character can perform.
    """

    name: str
    damage: int
    description: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __str__(self):
        return f"{self.name} (Dmg: {self.damage})"


# This mimics a database
class AbilityLibrary:
    _PRESETS = {
        "Mage": {Ability("Fireball", damage=25), Ability("Ice Shard", damage=15)},
        "Warrior": {Ability("Slash", damage=10), Ability("Shield Bash", damage=5)},
        "Villain": {Ability("Backstab", damage=20), Ability("Poison Dagger", damage=5)},
    }

    @classmethod
    def get_preset(cls, class_name: str) -> set[Ability]:
        """Returns a copy of the abilities for a specific class."""
        # Return a copy so one character's changes don't affect others
        # (Though since Ability is frozen, it's safe to share instances)
        return cls._PRESETS.get(class_name, set()).copy()
