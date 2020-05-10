from random import choice, random
from collections import Counter
from typing import Optional

from src.game import Game
from src.position import Position


class QLearningAgent:
    def __init__(
        self, alpha=1.0, epsilon=0.05, discount=0.8,
    ):
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount
        self.values = Counter()

    def get_Q_value(self, state, action) -> float:
        return self.values[(state, action)]

    def compute_value_from_Q_values(self, state: Game) -> float:
        legal_actions = state.legal_move()
        if len(legal_actions) == 0:
            return 0.0

        possible_values = [self.get_Q_value(state, action) for action in legal_actions]

        return max(possible_values)

    def compute_action_from_Q_values(self, state: Game) -> Optional[Position]:
        legal_actions = state.legal_move()
        if len(legal_actions) == 0:
            return None

        possible_values = [
            (self.get_Q_value(state, action), action) for action in legal_actions
        ]

        max_value = max(possible_values)[0]
        return choice([value for value in possible_values if value[0] == max_value])[1]

    def get_action(self, state: Game) -> Optional[Position]:
        legal_actions = state.legal_move()
        if len(legal_actions) == 0:
            return None

        if flip_coin(self.epsilon):
            return choice(legal_actions)
        else:
            return self.get_policy(state)

    def update(self, state, action, nextState, reward) -> None:
        self.values[(state, action)] = (1 - self.alpha) * self.get_Q_value(
            state, action
        ) + self.alpha * (reward + self.discount * self.get_value(nextState))

    def get_policy(self, state) -> Optional[Position]:
        return self.compute_action_from_Q_values(state)

    def get_value(self, state) -> float:
        return self.compute_value_from_Q_values(state)


class ApproximateQAgent(QLearningAgent):
    def __init__(self, feature_extractor, alpha=1.0, epsilon=0.05, discount=0.8):
        super().__init__(alpha, epsilon, discount)
        self.feat_extractor = feature_extractor
        self.weights = Counter()

    def get_weights(self) -> Counter:
        return self.weights

    def get_Q_value(self, state, action) -> float:
        features = self.feat_extractor.get_features(state, action)
        return sum(
            [value * self.weights[feature] for feature, value in features.items()]
        )

    def update(self, state, action, nextState, reward) -> None:
        features = self.feat_extractor.get_features(state, action)
        difference = (
            reward + self.discount * self.get_value(nextState)
        ) - self.get_Q_value(state, action)

        for feature, value in features.items():
            self.weights[feature] += self.alpha * difference * value


def flip_coin(probability: float) -> bool:
    return random() < probability
