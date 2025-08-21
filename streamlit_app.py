import streamlit as st
from diamond_game import game, players, cards, strategies
from itertools import cycle
from diamond_game import players

st.title("Diamond Card Game")




# Game setup
if 'game' not in st.session_state:
    st.session_state['game'] = None
    st.session_state['players'] = []
    st.session_state['started'] = False

# Limit to 2 human players, plus 1 bot
num_players = st.number_input("Number of human players (max 2):", min_value=1, max_value=2, value=2)
player_names = []
for i in range(num_players):
    name = st.text_input(f"Player {i+1} name:", value=f"Player {i+1}")
    player_names.append(name)

bot_name = st.text_input("Bot name:", value="Bot")
if st.button("Start Game", key="start_game_1"):
    # Create a cycle of suits to assign to players
    suits = cycle(["♥", "♠", "♣", "♦"])
    # Create human players with assigned suits
    human_players = [players.Player(name, next(suits)) for name in player_names]
    # Create bot player with an assigned suit
    bot_player = players.Player(bot_name, next(suits))

if st.button("Start Game", key="start_game_2"):
    human_players = [players.Player(name) for name in player_names]
    # Add bot using a strategy (replace with your bot implementation if needed)
    bot_player = players.Player(bot_name)
    # If you have a bot strategy, assign it here
    # bot_player.strategy = strategies.BotStrategy()
    all_players = human_players + [bot_player]
    st.session_state['players'] = all_players
    st.session_state['game'] = game.Game(all_players)
    st.session_state['started'] = True
    st.success("Game started!")

if st.session_state['started']:
    st.header("Game Actions")
    current_player = st.session_state['game'].current_player()
    st.write(f"Current player: {current_player.name}")
    hand = current_player.hand
    card_choice = st.selectbox("Choose a card to play:", hand)
    if st.button("Play Card"):
        st.session_state['game'].play_card(current_player, card_choice)
        st.success(f"{current_player.name} played {card_choice}")
    st.write("Game State:")
    st.write(st.session_state['game'].get_state())

# Add more game actions and UI as needed
