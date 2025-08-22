# import sys
# from .storage import manager

# BANNER = """
# === Diamond Card Game (CLI) ===
# - You are ♥, Robot is ♠
# - Enter values 1..13 you still hold.
# - Higher card wins diamond points; ties split.
# """

# def prompt_int(msg: str):
#     while True:
#         val = input(msg).strip()
#         if val.isdigit():
#             v = int(val)
#             if 1 <= v <= 13:
#                 return v
#         print("Please enter an integer between 1 and 13.")

# def prompt_player_count():
#     while True:
#         val = input("How many human players? [1 or 2]: ").strip()
#         if val in ("1", "2"):
#             return int(val)
#         print("Please enter 1 or 2.")

# def main():
#     print(BANNER)
#     print("Game mode: 2 bots will play against each other.")
#     allowed_levels = ["easy", "medium", "expert"]
#     def prompt_level(bot_name, default):
#         while True:
#             level = input(f"Choose {bot_name} level [easy|medium|expert] (default={default}): ").strip() or default
#             if level in allowed_levels:
#                 return level
#             print("Please enter one of: easy, medium, expert.")
#     bot1_level = prompt_level("Bot 1", "medium")
#     bot2_level = prompt_level("Bot 2", "expert")
#     bot_names = ["Bot 1", "Bot 2"]
#     bot_suits = ["♠", "♣"]
#     bot_levels = [bot1_level, bot2_level]
#     g = manager.create(bot_names=bot_names, bot_suits=bot_suits, bot_levels=bot_levels)
#     print(f"Game created: {g.id}")

#     import csv
#     import os
#     while True:
#         s = g.status()
#         if not s["active"]:
#             print("\nGame over!")
#             summary = g.summary()
#             print(summary)
#             csv_path = "diamond_game_summary.csv"
#             file_exists = os.path.isfile(csv_path)
#             with open(csv_path, "a", newline="") as csvfile:
#                 writer = csv.writer(csvfile)
#                 # Write header only if file is new
#                 if not file_exists:
#                     writer.writerow(["Bot 1 Level", summary["bot_levels"][0], "Bot 2 Level", summary["bot_levels"][1]])
#                     writer.writerow(["Round", "Diamond", "Bot 1 Play", "Bot 2 Play", "Winner", "Points Awarded"])
#                 else:
#                     writer.writerow([])
#                     writer.writerow(["Bot 1 Level", summary["bot_levels"][0], "Bot 2 Level", summary["bot_levels"][1]])
#                     writer.writerow(["Round", "Diamond", "Bot 1 Play", "Bot 2 Play", "Winner", "Points Awarded"])
#                 for r in summary["rounds"]:
#                     writer.writerow([
#                         r["round"],
#                         r["diamond"],
#                         r["bot_play"][0],
#                         r["bot_play"][1],
#                         r["winner"],
#                         r["points_awarded"]
#                     ])
#                 # Write final scores
#                 writer.writerow([])
#                 writer.writerow(["Final Scores"])
#                 for k, v in summary["final_scores"].items():
#                     writer.writerow([k, v])
#                 writer.writerow(["Winner", summary["winner"]])
#             print("Summary appended to diamond_game_summary.csv")
#             break

#         print(f"\nRound {s['round_no'] + 1}")
#         current_diamond = g.deck[g.round_no]
#         print(f"Diamond for this round: {current_diamond}")
#         for i, cards in enumerate(s['remaining_bot_cards']):
#             print(f"Bot {i+1} ({bot_suits[i]}) remaining cards: {cards}")
#         try:
#             res = g.play_round()
#         except Exception as e:
#             print("Error:", e)
#             continue

#         print(f"Diamond: {res.diamond} | Bot 1: {res.bot_play[0]} | Bot 2: {res.bot_play[1]}")
#         print(f"Winner: {res.winner} (+{res.points})")
#         st = g.status()
#         score_str = " | ".join([f"Bot {i+1}: {st['scores'][f'bot{i+1}']}" for i in range(2)])
#         print(f"Scores -> {score_str}")

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         sys.exit(0)




import sys
from .storage import manager
import csv
import os

BANNER = """
=== Diamond Card Game (CLI) ===
- You are ♥️, Robot is ♠️
- Enter values 1..13 you still hold.
- Higher card wins diamond points; ties split.
"""

def prompt_int_any(msg: str, min_val: int, max_val: int):
    while True:
        val = input(msg).strip()
        if val.isdigit():
            v = int(val)
            if min_val <= v <= max_val:
                return v
        print(f"Please enter an integer between {min_val} and {max_val}.")

def prompt_level(bot_name, default):
    allowed_levels = ["easy", "medium", "expert"]
    while True:
        level = input(f"Choose {bot_name} level [easy|medium|expert] (default={default}): ").strip() or default
        if level in allowed_levels:
            return level
        print("Please enter one of: easy, medium, expert.")

def main():
    print(BANNER)
    print("Game mode: 2 bots will play against each other.")

    bot1_level = prompt_level("Bot 1", "medium")
    bot2_level = prompt_level("Bot 2", "expert")

    num_games = prompt_int_any("How many games do you want to play? ", 1, 10000)

    bot_names = ["Bot 1", "Bot 2"]
    bot_suits = ["♠", "♣"]
    bot_levels = [bot1_level, bot2_level]

    csv_path = "diamond_game_summary.csv"
    file_exists = os.path.isfile(csv_path)

    for game_index in range(1, num_games + 1):
        g = manager.create(bot_names=bot_names, bot_suits=bot_suits, bot_levels=bot_levels)
        print(f"\nGame {game_index} created: {g.id}")

        while True:
            s = g.status()
            if not s["active"]:
                print(f"\nGame {game_index} over!")
                summary = g.summary()

                with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    # Write header only if file is new
                    if not file_exists:
                        writer.writerow(["Game Number", "Bot 1 Level", "Bot 2 Level", "Round", "Diamond", "Bot 1 Play", "Bot 2 Play", "Winner", "Points Awarded"])
                        file_exists = True
                    for r in summary["rounds"]:
                        writer.writerow([
                            game_index,
                            summary["bot_levels"][0],
                            summary["bot_levels"][1],
                            r["round"],
                            r["diamond"],
                            r["bot_play"],
                            r["bot_play"][1],
                            r["winner"],
                            r["points_awarded"],
                        ])
                    # Write final scores for each game
                    writer.writerow([])
                    writer.writerow(["Game Number", game_index, "Final Scores"])
                    for k, v in summary["final_scores"].items():
                        writer.writerow([k, v])
                    writer.writerow(["Winner", summary["winner"]])
                    writer.writerow([])

                print("Summary appended to diamond_game_summary.csv")
                break

            current_diamond = g.deck[g.round_no]
            print(f"Diamond for this round: {current_diamond}")
            try:
                res = g.play_round()
            except Exception as e:
                print("Error:", e)
                continue

            print(f"Diamond: {res.diamond} | Bot 1: {res.bot_play[0]} | Bot 2: {res.bot_play[1]}")
            print(f"Winner: {res.winner} (+{res.points})")
            st = g.status()
            score_str = " | ".join([f"Bot {i+1}: {st['scores'][f'bot{i+1}']}" for i in range(2)])
            print(f"Scores -> {score_str}")

    print(f"\nTotal games played: {num_games}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)