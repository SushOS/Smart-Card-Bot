from dataclasses import dataclass, field
from typing import List, Optional, Dict
from .cards import Card, suit_hand

@dataclass
class Player:
    name: str
    suit: str
    hand: List[Card] = field(default_factory=list)
    score: int = 0

    def initialize_hand(self):
        self.hand = suit_hand(self.suit)

    def has_card(self, value: int) -> bool:
        return any(c.value == value for c in self.hand)

    def play(self, value: int) -> Card:
        """Remove and return the card of 'value' from hand; raises if not present."""
        for i, c in enumerate(self.hand):
            if c.value == value:
                return self.hand.pop(i)
        raise ValueError(f"{self.name} does not have card value {value} {self.suit}")

    def remaining_values(self) -> List[int]:
        return sorted(c.value for c in self.hand)

@dataclass
class Bot(Player):
    difficulty: str = "random"
    memory: Dict[str, object] = field(default_factory=dict)  # space for strategy state
