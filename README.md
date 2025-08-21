# Diamond Card Game

## Overview
Diamond Card Game is a strategic card game implemented in Python, featuring both human and bot players. The game can be played in the terminal, with options for human-vs-bot, human-vs-human-vs-bot, and bot-vs-bot modes. The project is modular, extensible, and records game results in a CSV file for analysis.

## Features
- Play with 1 or 2 human players against a bot
- Play with 2 bots, each with configurable difficulty (easy, medium, expert)
- Bot strategies: random, matching, smart
- CLI prompts for player/bot configuration
- Game summary and round-by-round results saved to CSV
- Extensible codebase for new strategies or game modes

## Codebase Structure
```
requirements.txt
streamlit_app.py
README.md
/diamond_game
    __init__.py
    api.py
    cards.py
    cli.py
    game.py
    players.py
    storage.py
    strategies.py
```

### Main Modules
- **cards.py**: Defines the `Card` class and deck generation logic.
- **players.py**: Implements `Player` and `Bot` classes, including hand management and scoring.
- **strategies.py**: Contains bot strategy functions and the strategy selector. Only three levels are supported: easy (random), medium (matching), expert (smart).
- **game.py**: Core game logic, round resolution, score calculation, and summary generation. Supports multiple players and bots.
- **cli.py**: Command-line interface for running the game, collecting user input, and saving results to CSV.
- **storage.py**: Manages game instances and provides a singleton manager for CLI/API use.
- **api.py**: (Optional) For web or API-based play, not required for CLI mode.

## Game Logic
- Each round, a diamond card is drawn.
- Players (human or bot) select a card to play from their hand.
- The highest card wins the diamond's points; ties split points.
- Bot strategies:
  - **easy**: Plays a random card.
  - **medium**: Tries to match the diamond value, or plays the lowest card above it.
  - **expert**: Saves high cards for high diamonds, tries to beat the opponent's likely best card.
- The game continues for 13 rounds (one for each card in hand).
- At the end, scores and winner are displayed and saved to CSV.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the CLI:
   ```bash
   python -m diamond_game.cli
   ```
3. Follow prompts to select game mode and bot levels.
4. After the game, check `diamond_game_summary.csv` for results.

## Contributors
- Sushant Ravva
- Anshu Raj
- Tarun Reddy
- Sanket Jagtap

## Extending the Project
- Add new bot strategies in `strategies.py` and update the `LEVELS` mapping.
- Add new game modes by extending `game.py` and updating CLI logic.
- Integrate with web or GUI by using `api.py` or building on top of the core modules.
