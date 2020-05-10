from __future__ import annotations
from src.position import Position
from typing import List, Optional, Tuple

from time import sleep
from typing import Callable

from src.agent.feature_extractor import SimpleExtractor
from src.agent.q_learning_agent import QLearningAgent
from src.game import Game, create_game


def play_game(players: List[Tuple[QLearningAgent, Callable[[Game, Position], Game]]]):
    game = create_game()
    games = [game]
    turn = 0
    while game.winner() is None:
        agent, play = players[turn % len(players)]
        move = agent.get_action(game)
        if move:
            game = play(game, move)
        else:
            break

        turn += 1
        games.append(game)

    return games


def show_game(moments) -> None:
    for moment in moments:
        sleep(0.5)
        moment.show()

    winner = moments[-1].winner()
    if winner:
        print(f"Congrats to player with {winner}")
    else:
        print("TIE!")


if __name__ == "__main__":
    players = [
        (QLearningAgent(SimpleExtractor()), lambda game, move: game.play_cross(move)),
        (QLearningAgent(SimpleExtractor()), lambda game, move: game.play_circle(move)),
    ]
    moments = play_game(players)
    show_game(moments)
