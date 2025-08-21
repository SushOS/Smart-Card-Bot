import random
from typing import List, Optional
from .players import Bot
from .cards import Card

# --- Strategy helpers ---
def _pick_random(bot: Bot) -> int:
    return random.choice(bot.remaining_values())

def _pick_above_available(bot: Bot, diamond_value: int) -> int:
    options = bot.remaining_values()
    above = [v for v in options if v >= diamond_value]
    if above:
        return min(above)
    return min(options)

def _pick_matching(bot: Bot, diamond_value: int) -> int:
    # If matching value available use it, else conservative.
    if bot.has_card(diamond_value):
        return diamond_value
    return _pick_above_available(bot, diamond_value)

def _estimate_user_high_remaining(known_user_remaining: Optional[List[int]]) -> int:
    if not known_user_remaining:
        return 10  # neutral guess
    return max(known_user_remaining)

def _pick_smart(
    bot: Bot,
    diamond_value: int,
    remaining_diamonds: List[int],
    known_user_remaining: Optional[List[int]] = None,
) -> int:
    """
    Heuristic:
    - Save high cards for future high diamonds.
    - If current diamond is high (>=10), try to beat user's likely high with minimal necessary value.
    - If current diamond is low, dump the lowest card.
    """
    bot_vals = bot.remaining_values()
    if not bot_vals:
        raise RuntimeError("Bot has no cards to play")

    high_diamond_threshold = 10
    user_high = _estimate_user_high_remaining(known_user_remaining)  # Estimate user's high card
    # If diamond is low, dump lowest
    if diamond_value < high_diamond_threshold:
        return min(bot_vals)

    # For high diamonds, try to minimally exceed user's likely high if possible
    candidates = [v for v in bot_vals if v > user_high]
    if candidates:
        return min(candidates)

    # Else, play the smallest card >= diamond_value, else smallest available
    atleast = [v for v in bot_vals if v >= diamond_value]
    if atleast:
        return min(atleast)

    return min(bot_vals)

# --- Public strategy selector ---
def choose_card(
    bot: Bot,
    diamond_value: int,
    remaining_diamonds: List[int],
    known_user_remaining: Optional[List[int]] = None,
) -> int:
    d = bot.difficulty.lower()
    if d == "random":
        return _pick_random(bot)
    if d == "conservative":
        return _pick_above_available(bot, diamond_value)
    if d == "smart":
        return _pick_smart(bot, diamond_value, remaining_diamonds, known_user_remaining)
    # default "matching"
    return _pick_matching(bot, diamond_value)

# Map “levels” to strategies
LEVELS = {
    "easy": "random",
    "medium": "matching",
    "hard": "greedy",
    "expert": "smart",
}
