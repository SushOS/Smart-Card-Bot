from typing import Dict
from .game import Game

class GameManager:
    def __init__(self):
        self._games: Dict[str, Game] = {}

    def create(self, bot_names=None, bot_suits=None, bot_levels=None) -> Game:
        if bot_names is None:
            bot_names = ["Bot 1", "Bot 2"]
        if bot_suits is None:
            bot_suits = ["♠", "♣"]
        if bot_levels is None:
            bot_levels = ["medium", "hard"]
        g = Game(bot_names=bot_names, bot_suits=bot_suits, bot_levels=bot_levels)
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
