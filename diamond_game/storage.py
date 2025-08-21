from typing import Dict
from .game import Game

class GameManager:
    def __init__(self):
        self._games: Dict[str, Game] = {}

    def create(self, human_names=None, human_suits=None, bot_level: str = "medium") -> Game:
        if human_names is None:
            human_names = ["Player 1"]
        if human_suits is None:
            human_suits = ["♥"]
        g = Game(human_names=human_names, human_suits=human_suits, bot_level=bot_level)
        self._games[g.id] = g
        return g

    def get(self, game_id: str) -> Game:
        if game_id not in self._games:
            raise KeyError("Game not found")
        return self._games[game_id]

    def abandon(self, game_id: str):
        g = self.get(game_id)
        g.abandon()
        return g

# Singleton for simple deployments
manager = GameManager()
