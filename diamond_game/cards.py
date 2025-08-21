from dataclasses import dataclass
from typing import List
import random

SUITS = ("♦", "♥", "♠", "♣")

@dataclass(frozen=True)
class Card:
    suit: str
    value: int  # 1..13 (Ace=1, ... , King=13)

    def __str__(self):
        return f"{self.value} {self.suit}"

def diamond_deck() -> List["Card"]: # initializing the diamond deck and shuffling it
    """Return 13 diamond cards (♦1..♦13)."""
    diamond_deck = [Card("♦", v) for v in range(1, 14)]
    random.shuffle(diamond_deck)
    return diamond_deck

def suit_hand(suit: str) -> List["Card"]: # giving each suit to the players
    """Return 13 cards of a single suit (values 1..13)."""
    assert suit in SUITS
    return [Card(suit, v) for v in range(1, 14)]

hearts_hand = suit_hand("♥")
print(hearts_hand)