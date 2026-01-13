from src.abilities.ability import Ability


class AbilityLibrary:
    _ABILITIES = {
        "punch": Ability(name="Punch", damage=5),
        "kick": Ability(name="Kick", damage=8),
        "slash": Ability(name="Slash", damage=10),
        "smash": Ability(name="Smash", damage=20),
        "fireball": Ability(name="Fireball", damage=20),
        "ice shard": Ability(name="Ice Shard", damage=15),

    }

    PRESETS = {
        "basic": {"punch", "kick"},
        "mage": {"punch", "kick", "fireball", "ice shard"},
        "warrior": {"punch", "kick", "slash", "smash"},
    }

    @classmethod
    def get(cls, ability_id: str) -> Ability:
        """Returns the ability object. Use .copy() if you plan to modify it!"""
        return cls._ABILITIES.get(ability_id.lower())

    @classmethod
    def get_preset(cls, preset_name: str) -> list[Ability]:
        """Returns a list of Ability objects based on a preset name."""
        ids = cls.PRESETS.get(preset_name.lower(), "basic")
        return [cls.get(aid) for aid in ids]
