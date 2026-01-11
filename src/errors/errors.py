class GameError(Exception):
    """Base class for all game-related errors."""
    pass


class DefeatedError(GameError):
    """Raised when a defeated character tries to perform an action."""
    pass


class TargetDefeatedError(GameError):
    """Raised when an action is attempted on an already defeated target."""
    pass


class NoAbilitiesError(GameError):
    """ Raised when you try to access the character's abilities and its empty"""
    pass


class InvalidMemberError(GameError):
    """Exception raised when a non-Character object is added to a Team."""
    pass


class InvalidObjectType(GameError):
    """ Exception raised when a non-Character object is provided"""
