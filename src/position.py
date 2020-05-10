from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return tuple([self.x, self.y]).__hash__()

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y
