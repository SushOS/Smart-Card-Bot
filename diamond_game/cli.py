import sys
from .storage import manager

BANNER = """
=== Diamond Card Game (CLI) ===
- You are ♥, Robot is ♠
- Enter values 1..13 you still hold.
- Higher card wins diamond points; ties split.
"""

def prompt_int(msg: str):
    while True:
        val = input(msg).strip()
        if val.isdigit():
            v = int(val)
            if 1 <= v <= 13:
                return v
        print("Please enter an integer between 1 and 13.")

def prompt_player_count():
    while True:
        val = input("How many human players? [1 or 2]: ").strip()
        if val in ("1", "2"):
            return int(val)
        print("Please enter 1 or 2.")

def main():
    print(BANNER)
    num_players = prompt_player_count()
    level = input("Choose bot level [easy|medium|hard|expert] (default=medium): ").strip() or "medium"
    if num_players == 1:
        human_names = ["Player 1"]
        human_suits = ["♥"]
    else:
        human_names = ["Player 1", "Player 2"]
        human_suits = ["♥", "♦"]
    g = manager.create(human_names=human_names, human_suits=human_suits, bot_level=level)
    print(f"Game created: {g.id}")

    while True:
        s = g.status()
        if not s["active"]:
            print("\nGame over!")
            print(g.summary())
            break

        print(f"\nRound {s['round_no'] + 1}")
        current_diamond = g.deck[g.round_no]
        print(f"Diamond for this round: {current_diamond}")
        for i, cards in enumerate(s['remaining_human_cards']):
            print(f"Player {i+1} ({human_suits[i]}) remaining cards: {cards}")
        human_values = []
        for i in range(num_players):
            hv = prompt_int(f"Player {i+1} ({human_suits[i]}) play a value: ")
            human_values.append(hv)
        try:
            res = g.play_round(human_values)
        except Exception as e:
            print("Error:", e)
            continue

        print(f"Diamond: {res.diamond} | Player 1: {res.human_play} | Robot: {res.bot_play}")
        print(f"Winner: {res.winner} (+{res.points})")
        st = g.status()
        score_str = " | ".join([f"Player {i+1}: {st['scores'][f'player{i+1}']}" for i in range(num_players)])
        print(f"Scores -> {score_str} | Robot: {st['bot']}")

        if not st["active"]:
            print("\nFinal summary:")
            print(g.summary())
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
