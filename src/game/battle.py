import random
from src.errors.errors import NoWinnerError
from src.classes.character import Character

MINIMUM_ROUNDS = 3
MAXIMUM_ROUNDS = 7


class Battle:
    def start(self, first_character: Character, second_character: Character) -> Character:
        """
        Do the battle logic and return the winner

        Args:
            first_character (Character): first character
            second_character (Character): second character

        Returns:
            The Character who won (lost fewer points)

        Raises:
            NoWinnerError: if no winner is available (when there is a tie)
            NoAbilityError: if one character have no abilities
        """
        if not isinstance(first_character, Character):
            raise TypeError(f"First character must be a Character, not {type(first_character).__name__}")
        if not isinstance(second_character, Character):
            raise TypeError(f"Second character must be a Character, not {type(second_character).__name__}")

        # Determine how many rounds the game will take
        rounds = random.randint(MINIMUM_ROUNDS, MAXIMUM_ROUNDS)

        first_damage_delt = 0
        second_damage_delt = 0

        for i in range(rounds):
            first_damage_delt += first_character.attack(second_character)
            second_damage_delt += second_character.attack(first_character)

        if first_damage_delt > second_damage_delt:
            return first_character
        if second_damage_delt > first_damage_delt:
            return second_character
        raise NoWinnerError(f"No winner found for {first_character.name} and {second_character.name}")
