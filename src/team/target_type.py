from enum import Enum, auto


class TargetType(Enum):
    SELF = auto()
    ALLY = auto()
    ENEMY = auto()
    ANY = auto()
