from src.abilities.ability import Ability

# --- Basic Abilities ---
PUNCH = Ability(name="Punch", damage=5)
KICK = Ability(name="Kick", damage=8)

# --- Physical Abilities --
SLASH = Ability(name="Slash", damage=10)
SMASH = Ability(name="Smash", damage=20)

# --- Magic Abilities ---
FIREBALL = Ability(name="Fireball", damage=20)
ICE_SHARD = Ability(name="Ice Shard", damage=15)

# --- Defaults Group ---
# We group them here so we can easily import the "Standard Set"
DEFAULT_SET = {PUNCH, KICK}
DEFAULT_MAGE_SET = DEFAULT_SET | {FIREBALL, ICE_SHARD}
DEFAULT_WARRIOR_SET = DEFAULT_SET | {SLASH, SMASH}
