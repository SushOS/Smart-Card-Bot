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
    bot_name: str = "Robot"
    bot_suit: str = "♠"
    bot_level: str = "medium"  # easy, medium, hard, expert
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # runtime state
    deck: List[Card] = field(default_factory=list)
    round_no: int = 0
    humans: List[Player] = field(init=False)
    bot: Bot = field(init=False)
    remaining_diamonds: List[int] = field(default_factory=list)  # values only
    history: List[RoundResult] = field(default_factory=list)
    active: bool = True

    def __post_init__(self):
        self.humans = []
        for name, suit in zip(self.human_names, self.human_suits):
            p = Player(name, suit)
            p.initialize_hand()
            self.humans.append(p)
        self.bot = Bot(self.bot_name, self.bot_suit, difficulty=LEVELS.get(self.bot_level, "matching"))
        self.bot.initialize_hand()
        self.deck = diamond_deck()
        self.remaining_diamonds = [c.value for c in self.deck]

    def is_over(self) -> bool:
        return (self.round_no >= 13) or (not self.active)

    def status(self) -> Dict:
        return {
            "game_id": self.id,
            "active": self.active and not self.is_over(),
            "round_no": self.round_no,
            "scores": {f"player{i+1}": p.score for i, p in enumerate(self.humans)},
            "bot": self.bot.score,
            "remaining_human_cards": [p.remaining_values() for p in self.humans],
            "remaining_bot_cards_count": len(self.bot.remaining_values()),
            "remaining_diamonds_count": len(self.deck) - self.round_no,
            "bot_level": self.bot_level,
        }

    def _resolve_points(self, human_cards: List[Card], bot_card: Card, diamond: Card) -> RoundResult:
        # Find highest card value
        all_cards = human_cards + [bot_card]
        values = [c.value for c in all_cards]
        max_value = max(values)
        winners = []
        for i, c in enumerate(human_cards):
            if c.value == max_value:
                winners.append(f"player{i+1}")
        if bot_card.value == max_value:
            winners.append("bot")
        pts = diamond.value
        # Split points among winners
        pts_per_winner = pts // len(winners)
        remainder = pts % len(winners)
        for i, p in enumerate(self.humans):
            if f"player{i+1}" in winners:
                p.score += pts_per_winner
        if "bot" in winners:
            self.bot.score += pts_per_winner
        # Give remainder to first winner
        if winners:
            if winners[0].startswith("player"):
                idx = int(winners[0][-1]) - 1
                self.humans[idx].score += remainder
            else:
                self.bot.score += remainder
        winner = winners if len(winners) > 1 else winners[0]
        return RoundResult(
            round_no=self.round_no,
            diamond=diamond,
            human_play=human_cards[0],  # for compatibility, first player
            bot_play=bot_card,
            winner=winner,
            points=pts,
        )

    def play_round(self, human_values: List[int]) -> RoundResult:
        if self.is_over():
            raise RuntimeError("Game is already over or inactive.")
        if len(human_values) != len(self.humans):
            raise ValueError("Must provide a value for each player.")
        for i, v in enumerate(human_values):
            if not self.humans[i].has_card(v):
                raise ValueError(f"{self.humans[i].name} does not have {self.humans[i].suit}{v} available.")

        # Draw top diamond
        diamond = self.deck[self.round_no]
        self.round_no += 1
        if diamond.value in self.remaining_diamonds:
            self.remaining_diamonds.remove(diamond.value)

        # Human plays
        human_cards = [p.play(v) for p, v in zip(self.humans, human_values)]

        # Bot decides
        known_user_remaining = [p.remaining_values() for p in self.humans]
        # For bot strategy, flatten known_user_remaining
        flat_known = [v for sub in known_user_remaining for v in sub]
        bot_choice_value = choose_card(
            self.bot, diamond.value, self.remaining_diamonds, flat_known
        )
        bot_card = self.bot.play(bot_choice_value)

        # Resolve
        result = self._resolve_points(human_cards, bot_card, diamond)
        self.history.append(result)

        if self.is_over():
            self.active = False
        return result

    def abandon(self):
        self.active = False

    def summary(self) -> Dict:
        scores = {f"player{i+1}": p.score for i, p in enumerate(self.humans)}
        scores["bot"] = self.bot.score
        max_score = max(scores.values())
        winners = [k for k, v in scores.items() if v == max_score]
        winner = winners if len(winners) > 1 else winners[0]
        return {
            "game_id": self.id,
            "winner": winner,
            "final_scores": scores,
            "rounds": [
                {
                    "round": r.round_no,
                    "diamond": str(r.diamond),
                    "human_play": str(r.human_play),
                    "bot_play": str(r.bot_play),
                    "winner": r.winner,
                    "points_awarded": r.points,
                }
                for r in self.history
            ],
        }
