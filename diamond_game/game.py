from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Literal
import uuid

from .cards import Card, diamond_deck
from .players import Player, Bot
from .strategies import choose_card, LEVELS

Winner = Literal["human", "bot", "tie"]

@dataclass
class RoundResult:
    round_no: int
    diamond: Card
    human_play: Card
    bot_play: Card
    winner: Winner
    points: int

@dataclass
class Game:
    human_names: List[str] = field(default_factory=lambda: ["Player 1", "Player 2"])
    human_suits: List[str] = field(default_factory=lambda: ["♥", "♦"])
    bot_names: List[str] = field(default_factory=lambda: ["Bot 1", "Bot 2"])
    bot_suits: List[str] = field(default_factory=lambda: ["♠", "♣"])
    bot_levels: List[str] = field(default_factory=lambda: ["medium", "hard"])
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # runtime state
    deck: List[Card] = field(default_factory=list)
    round_no: int = 0
    humans: List[Player] = field(init=False)
    bots: List[Bot] = field(init=False)
    remaining_diamonds: List[int] = field(default_factory=list)  # values only
    history: List[RoundResult] = field(default_factory=list)
    active: bool = True

    def __post_init__(self):
        self.humans = []
        for name, suit in zip(self.human_names, self.human_suits):
            p = Player(name, suit)
            p.initialize_hand()
            self.humans.append(p)
        self.bots = []
        for name, suit, level in zip(self.bot_names, self.bot_suits, self.bot_levels):
            b = Bot(name, suit, difficulty=LEVELS.get(level, "matching"))
            b.initialize_hand()
            self.bots.append(b)
        self.deck = diamond_deck()
        self.remaining_diamonds = [c.value for c in self.deck]

    def is_over(self) -> bool:
        return (self.round_no >= 13) or (not self.active)

    def status(self) -> Dict:
        return {
            "game_id": self.id,
            "active": self.active and not self.is_over(),
            "round_no": self.round_no,
            "scores": {f"bot{i+1}": b.score for i, b in enumerate(self.bots)},
            "remaining_bot_cards": [b.remaining_values() for b in self.bots],
            "remaining_diamonds_count": len(self.deck) - self.round_no,
            "bot_levels": self.bot_levels,
        }

    def _resolve_points(self, bot_cards: List[Card], diamond: Card) -> RoundResult:
        # Find highest card value
        values = [c.value for c in bot_cards]
        max_value = max(values)
        winners = [f"bot{i+1}" for i, c in enumerate(bot_cards) if c.value == max_value]
        pts = diamond.value
        pts_per_winner = pts / len(winners)
        for i, b in enumerate(self.bots):
            if f"bot{i+1}" in winners:
                b.score += pts_per_winner
        winner = winners if len(winners) > 1 else winners[0]
        return RoundResult(
            round_no=self.round_no,
            diamond=diamond,
            human_play=None,
            bot_play=[str(c) for c in bot_cards],
            winner=winner,
            points=pts,
        )

    def play_round(self) -> RoundResult:
        if self.is_over():
            raise RuntimeError("Game is already over or inactive.")

        # Draw top diamond
        diamond = self.deck[self.round_no]
        self.round_no += 1
        if diamond.value in self.remaining_diamonds:
            self.remaining_diamonds.remove(diamond.value)

        # Each bot decides
        bot_cards = []
        for i, bot in enumerate(self.bots):
            known_remaining = bot.remaining_values()
            bot_choice_value = choose_card(
                bot, diamond.value, self.remaining_diamonds, known_remaining
            )
            bot_card = bot.play(bot_choice_value)
            bot_cards.append(bot_card)

        # Resolve
        result = self._resolve_points(bot_cards, diamond)
        self.history.append(result)

        if self.is_over():
            self.active = False
        return result

    def abandon(self):
        self.active = False

    def summary(self) -> Dict:
        scores = {f"bot{i+1}": b.score for i, b in enumerate(self.bots)}
        max_score = max(scores.values())
        winners = [k for k, v in scores.items() if v == max_score]
        winner = winners if len(winners) > 1 else winners[0]
        return {
            "game_id": self.id,
            "winner": winner,
            "final_scores": scores,
            "bot_levels": self.bot_levels,
            "rounds": [
                {
                    "round": r.round_no,
                    "diamond": str(r.diamond),
                    "bot_play": r.bot_play,
                    "winner": r.winner,
                    "points_awarded": r.points,
                }
                for r in self.history
            ],
        }
