from __future__ import annotations
from typing import Callable, Dict, List, Optional

from src.cell import Cell
from src.position import Position


def create_game() -> Game:
    return Game({Position(x, y): Cell.EMPTY for x in range(3) for y in range(3)})


diagonals_position = [
    [Position(0, 0), Position(1, 1), Position(2, 2)],
    [Position(2, 0), Position(1, 1), Position(0, 2),],
]


class Game:
    def __init__(self, board: Dict[Position, Cell] = None) -> None:
        if board is None:
            self.board = {}
        else:
            self.board: Dict[Position, Cell] = board

    def legal_move(self) -> List[Position]:
        return [position for position, cell in self.board.items() if cell == Cell.EMPTY]

    def play_cross(self, position: Position) -> Game:
        return self._play(position, Cell.X)

    def play_circle(self, position: Position) -> Game:
        return self._play(position, Cell.O)

    def _play(self, position: Position, cell: Cell) -> Game:
        if self.board[position] != Cell.EMPTY:
            raise SquareAlreadyTaken()

        return Game({**self.board, position: cell})

    def winner(self) -> Optional[Cell]:
        return (
            self._winner(self.rows)
            or self._winner(self.columns)
            or self._winner(self.diagonals)
        )

    def _winner(self, lines) -> Optional[Cell]:
        for line in lines:
            if line[0] != Cell.EMPTY and all([line[0] == cell for cell in line]):
                return line[0]

    @property
    def rows(self) -> List[List[Cell]]:
        return self._lines(lambda position: position.y)

    def row(self, position: Position) -> List[Cell]:
        return self._lines(lambda position: position.y)[position.y]

    @property
    def columns(self) -> List[List[Cell]]:
        return self._lines(lambda position: position.x)

    def column(self, position: Position) -> List[Cell]:
        return self._lines(lambda position: position.x)[position.x]

    @property
    def diagonals(self) -> List[List[Cell]]:
        first_diagonal = [
            cell for position, cell in self.board.items() if position.x == position.y
        ]
        second_diagonal = [
            cell
            for position, cell in self.board.items()
            if position.x + position.y == 2
        ]
        return [first_diagonal, second_diagonal]

    def diagonal(self, position) -> List[List[Cell]]:
        if position in diagonals_position[0] and position in diagonals_position[1]:
            return self.diagonals
        if position in diagonals_position[0]:
            return [[self.board[p] for p in diagonals_position[0]]]
        if position in diagonals_position[1]:
            return [[self.board[p] for p in diagonals_position[1]]]

        return [[]]

    def _lines(self, key: Callable[[Position], int]) -> List[List[Cell]]:
        lines = []
        for i in range(3):
            lines.append(
                [cell for position, cell in self.board.items() if key(position) == i]
            )

        return lines

    def show(self) -> None:
        cells = []
        for y in range(3):
            cells.append([self.board[Position(x, y)] for x in range(3)])

        print()
        for row in cells[:-1]:
            print("|".join(row))
            print(5 * "-")

        print("|".join(cells[-1]))
        print()


class SquareAlreadyTaken(Exception):
    pass
