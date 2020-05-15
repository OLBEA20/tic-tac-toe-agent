from abc import ABC, abstractmethod
from typing import List

from src.cell import Cell
from src.game import Game
from src.position import Position


class FeatureExtractor(ABC):
    @abstractmethod
    def get_features(self, state, action):
        pass


corner_positions = [Position(0, 0), Position(0, 2), Position(2, 0), Position(2, 2)]


class SimpleExtractor(FeatureExtractor):
    def __init__(self, cell: Cell) -> None:
        self.cell = cell
        self.opponent_cell = Cell.X if cell == Cell.O else Cell.O

    def get_features(self, state: Game, action: Position):
        features = {}

        if self.cell == Cell.X:
            new_state = state.play_cross(action)
        else:
            new_state = state.play_circle(action)

        lines_before_move = state.rows + state.columns + state.diagonals
        lines_after_move = new_state.rows + new_state.columns + new_state.diagonals

        for line in lines_after_move:
            if all([cell == self.cell for cell in line]):
                features["tic-tac-toe"] = 1

        if "tic-tac-toe" not in features:
            features["block-move"] = (
                count_block(self.cell, self.opponent_cell, lines_after_move)
                - count_block(self.cell, self.opponent_cell, lines_before_move)
            ) / 2

            features["corner-move"] = 0.2 if action in corner_positions else 0
            features["center"] = 0.2 if action.x == 1 and action.y == 1 else 0

        return features


def count_number_of_tic_tac_toe(reference_cell: Cell, lines: List[List[Cell]]) -> int:
    count = 0
    for line in lines:
        position_in_line = any([cell == reference_cell for cell in line])
        occupied_by_enemy = any(
            [cell != reference_cell and cell != Cell.EMPTY for cell in line]
        )
        if position_in_line and not occupied_by_enemy:
            count += 1

    return count


def count_block(player_cell: Cell, opponent_cell: Cell, lines: List[List[Cell]]) -> int:
    block = 0
    for line in lines:
        opponent_count = 0
        player_count = 0
        for cell in line:
            if cell == player_cell:
                player_count += 1
            if cell == opponent_cell:
                opponent_count += 1
        if player_count == 1 and opponent_count == 2:
            block += 1

    return block
