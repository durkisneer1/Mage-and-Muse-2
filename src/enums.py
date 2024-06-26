import enum


class LevelOneAttack(enum.IntEnum):
    BULL = enum.auto()
    TACO = enum.auto()
    TAMBOURINE = enum.auto()


class LevelTwoAttack(enum.IntEnum):
    FIREBALL = enum.auto()


class States(enum.IntEnum):
    TITLE = enum.auto()
    CONTROLS = enum.auto()
    GAMEPLAY = enum.auto()
    PAUSE = enum.auto()
    LOSE = enum.auto()
    WIN = enum.auto()
    EXIT = enum.auto()
