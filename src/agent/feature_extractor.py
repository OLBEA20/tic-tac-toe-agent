from abc import ABC, abstractmethod
from collections import Counter


class FeatureExtractor(ABC):
    @abstractmethod
    def getFeatures(self, state, action):
        pass


class SimpleExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        features = Counter()

        features["#-of-possible-tic-tac-toe"] = 0

        return features
