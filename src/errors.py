class GameError(Exception):
    """Base class for all game-related errors."""
    pass


class InsufficientPointsError(GameError):
    """Raised when a character doesn't have enough points to perform a special move."""
    pass


class NoAbilitiesError(GameError):
    """ Raised when you try to access the character's abilities and its empty"""
    pass


class NoWinnerError(GameError):
    """ Raised when there is no winner for the battle"""
    pass
