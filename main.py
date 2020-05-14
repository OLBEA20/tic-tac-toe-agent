from __future__ import annotations

from collections import Counter
from time import sleep
from typing import Callable, Dict, List, Optional, Tuple

from src.agent.feature_extractor import SimpleExtractor
from src.agent.q_learning_agent import ApproximateQAgent, QLearningAgent
from src.cell import Cell
from src.game import Game, create_game
from src.position import Position


def play_game(players: List[Tuple[QLearningAgent, Callable[[Game, Position], Game]]]):
    game = create_game()
    games = [game]
    turn = 0
    players_action = {player: [] for player, _ in players}
    while game.winner() is None:
        agent, play = players[turn % len(players)]
        move = agent.get_action(game)
        if move:
            game = play(game, move)
            players_action[agent].append(tuple([games[-1], move, game]))
        else:
            break

        turn += 1
        games.append(game)

    return games, players_action


def update_agents(
    players: List[Tuple[QLearningAgent, Callable[[Game, Position], Game]]],
    moves: Dict[QLearningAgent, List[Tuple[Game, Position, Game]]],
    winner: Optional[Cell],
) -> None:
    for player, _ in players:
        reward = 1 if winner == player.name or winner is None else -1
        for move in moves[player]:
            player.update(*move, reward)


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
        (QLearningAgent(Cell.O), lambda game, move: game.play_circle(move)),
        (
            ApproximateQAgent(SimpleExtractor(Cell.X), Cell.X),
            lambda game, move: game.play_cross(move),
        ),
    ]
    for _ in range(3000):
        moments, players_move = play_game(players)
        update_agents(players, players_move, moments[-1].winner())

    for player, _ in players:
        player.stop_learning()

    leaderboard = Counter()
    for _ in range(1000):
        moments, players_move = play_game(players)
        leaderboard[moments[-1].winner()] += 1
        # show_game(moments)
        # input("Waiting")

    print(leaderboard)
    # show_game(moments)
