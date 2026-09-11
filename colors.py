from enum import Enum

class Colors(Enum):
    GRAY = 0
    BLACK = 1
    YELLOW = 2
    VIOLET = 3
    GREEN = 4
    PINK = 5
    RED = 6
    ORANGE = 7
    WHITE = 8
    BLUE = 9

colorValues = {
    "GRAY": (105, 105, 105),
    "BLACK": (20, 25, 30),
    "YELLOW": (205, 205, 0),
    "VIOLET": (148, 0, 211),
    "GREEN": (35, 165, 35),
    "PINK": (255, 182, 193),
    "RED": (195, 35, 35),
    "ORANGE": (225, 145, 0),
    "WHITE": (248, 248, 255),
    "BLUE": (72, 118, 255)
}