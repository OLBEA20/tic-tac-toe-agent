from enum import Enum


class Cell(str, Enum):
    X = "X"
    O = "O"
    EMPTY = " "
