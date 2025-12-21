# blackjack_streamlit.py
# Streamlit wrapper for the "Big Book" Blackjack game logic.
# Preserves original rules and options (multiplayer, betting, double down, difficulty).

import streamlit as st
import random
import sys

# --- Constants / Globals (visual) ---
HEARTS   = chr(9829)
DIAMONDS = chr(9830)
SPADES   = chr(9824)
CLUBS    = chr(9827)
BACKSIDE = 'backside'

MAX_PLAYERS = 4

# --- Core game helper functions (kept logic identical) ---

def getDeck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

def getHandValue(cards):
    value = 0
    numberOfAces = 0
    for card in cards:
        rank = card[0]
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)
    value += numberOfAces
    for _ in range(numberOfAces):
        if value + 10 <= 21:
            value += 10
    return value

def render_cards(cards, hide_first=False):
    """Return ascii text for a list of cards (string)."""
    rows = ['', '', '', '', '']
    for i, card in enumerate(cards):
        rows[0] += ' ___  '
        if card == BACKSIDE and hide_first:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            rank, suit = card
            rows[1] += f'|{rank.ljust(2)} | '
            rows[2] += f'| {suit} | '
            rows[3] += f'|_{rank.rjust(2, "_")}| '
    return "\n".join(rows)

# Dealer AI same logic as original
def dealer_ai_play(deck, dealerHand, difficulty):
    if difficulty == 'easy':
        stop_threshold = 15
    elif difficulty == 'hard':
        stop_threshold = random.randint(18, 19)
    else:
        stop_threshold = 17

    while getHandValue(dealerHand) < stop_threshold:
        dealerHand.append(deck.pop())
    return dealerHand

# --- Streamlit run() entrypoint ---

def run():
    st.set_page_config(
    page_title="Responsive App",
    layout="centered",
    initial_sidebar_state="collapsed"
    )
    st.title("🃏 Blackjack (Streamlit edition)")
    
    st.markdown("""
    A simplified version of the casino classic 🎲  

    **How to play:**  
    - The goal is to get as close to **21** as possible without going over.  
    - You start with two cards; face values are added together.  
    - Click **Hit** to draw another card, or **Stand** to stop.  
    - If your hand exceeds 21, you **bust** and lose the round!  
    - Dealer plays after you and must hit until reaching 17 or higher.  

    💡 Tip: Aces count as **1 or 11**, whichever helps your score the most.
    """)
    st.divider()


    # Sidebar difficulty selection (with unique key)
    difficulty = st.sidebar.selectbox(
        "Choose difficulty",
        ["normal", "easy", "hard"],
        index=0,
        key="difficulty_select"
    )
    st.sidebar.write("Dealer behavior:")
    st.sidebar.write("- easy: stops at 15+")
    st.sidebar.write("- normal: stops at 17")
    st.sidebar.write("- hard: may risk 18-19")

    # Initialize session state
    if 'bj_initialized' not in st.session_state:
        st.session_state.bj_initialized = True
        st.session_state.wins = 0
        st.session_state.losses = 0
        st.session_state.ties = 0
        st.session_state.players = []
        st.session_state.deck = []
        st.session_state.dealerHand = []
        st.session_state.phase = 'setup'
        st.session_state.current_player_index = 0
        st.session_state.message = ""
        st.session_state.numPlayers = 1

    st.write("Rules: Get close to 21. Face cards = 10. Aces = 1 or 11.")
    st.write("---")

    # ---------- SETUP ----------
    if st.session_state.phase == 'setup':
        st.subheader("Game Setup")

        num = st.number_input(
            "Number of players (1-4):",
            min_value=1,
            max_value=MAX_PLAYERS,
            value=1,
            step=1,
            key="num_players_input"
        )
        st.session_state.numPlayers = num

        player_names = []
        for i in range(num):
            default = f"Player{i+1}"
            name = st.text_input(
                f"Name for Player {i+1}:",
                value=default,
                key=f"name_input_{i}"
            )
            player_names.append(name or default)

        # Start Round button
        if st.button("Start Round", key="start_round_btn"):
            players = []
            existing = {p['name']: p for p in st.session_state.players} if st.session_state.players else {}
            for i, nm in enumerate(player_names):
                pmoney = existing.get(nm, {}).get('money', 5000)
                players.append({'name': nm, 'money': pmoney, 'hand': [], 'bet': 0, 'final_bet': 0})
            st.session_state.players = players

            st.session_state.deck = getDeck()
            st.session_state.dealerHand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
            st.session_state.current_player_index = 0
            st.session_state.message = ""
            st.session_state.phase = 'betting'
            st.rerun()

        return

    # ---------- BETTING ----------
    if st.session_state.phase == 'betting':
        st.subheader("Place Bets")
        active_players = [p for p in st.session_state.players if p['money'] > 0]
        if not active_players:
            st.info("All players are broke! Game over.")
            st.session_state.phase = 'setup'
            return

        all_bet_done = True
        for i, player in enumerate(st.session_state.players):
            st.write(f"**{player['name']}** — Money: ${player['money']}")
            if player['money'] <= 0:
                st.write("Broke — skipped.")
                continue

            if player['bet'] == 0:
                bet = st.number_input(
                    f"Bet for {player['name']} (1-{player['money']}):",
                    min_value=1,
                    max_value=player['money'],
                    value=1,
                    key=f"bet_input_{i}"
                )
                if st.button(f"Confirm bet for {player['name']}", key=f"confirm_bet_btn_{i}"):
                    player['bet'] = int(bet)
                    player['hand'] = [st.session_state.deck.pop(), st.session_state.deck.pop()]
                    st.rerun()
            else:
                st.write(f"Bet placed: ${player['bet']}")

            if player['bet'] == 0 and player['money'] > 0:
                all_bet_done = False

        if all_bet_done:
            st.success("All bets placed! Starting turns...")
            st.session_state.phase = "play"
            st.rerun()

        st.info("Place bets for each player and confirm. When all are done, the game will begin.")
        return

    # ---------- PLAY ----------
    if st.session_state.phase == 'play':
        players = st.session_state.players
        idx = st.session_state.current_player_index

        while idx < len(players) and (players[idx]['money'] <= 0 or players[idx]['bet'] == 0):
            idx += 1

        if idx >= len(players):
            st.session_state.phase = 'dealer'
            st.rerun()

        player = players[idx]
        st.subheader(f"Turn: {player['name']}")
        st.write(f"Money: ${player['money']} | Current Bet: ${player['bet']}")
        st.text("Dealer shows (one hidden):")
        st.text(render_cards([BACKSIDE] + st.session_state.dealerHand[1:], hide_first=True))
        st.text("Your hand:")
        st.text(render_cards(player['hand']))
        st.write("Your total:", getHandValue(player['hand']))

        if getHandValue(player['hand']) > 21:
            st.write("You already busted.")
            player['final_bet'] = player['bet']
            st.session_state.current_player_index += 1
            st.rerun()

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Hit", key=f"hit_btn_{idx}"):
                player['hand'].append(st.session_state.deck.pop())
                st.rerun()
        with col2:
            if st.button("Stand", key=f"stand_btn_{idx}"):
                player['final_bet'] = player['bet']
                st.session_state.current_player_index += 1
                st.rerun()
        with col3:
            can_double = len(player['hand']) == 2 and (player['money'] - player['bet']) >= player['bet']
            if can_double and st.button("Double down", key=f"double_btn_{idx}"):
                player['bet'] *= 2
                player['final_bet'] = player['bet']
                player['hand'].append(st.session_state.deck.pop())
                st.session_state.current_player_index += 1
                st.rerun()

        st.write("Tip: Hit until you stand or bust. Double down allowed only on your first move.")
        if st.button("End turn (force)", key=f"end_turn_btn_{idx}"):
            player['final_bet'] = player['bet']
            st.session_state.current_player_index += 1
            st.rerun()
        return

    # ---------- DEALER ----------
    if st.session_state.phase == 'dealer':
        st.subheader("Dealer's Turn")
        st.text("Dealer's hand:")
        st.text(render_cards(st.session_state.dealerHand))
        st.write("Dealer total:", getHandValue(st.session_state.dealerHand))

        if any(getHandValue(p['hand']) <= 21 for p in st.session_state.players if p['bet'] > 0):
            st.write("Dealer is playing...")
            st.session_state.dealerHand = dealer_ai_play(st.session_state.deck, st.session_state.dealerHand, difficulty)
            st.write("Dealer finished.")
            st.text(render_cards(st.session_state.dealerHand))
            st.write("Dealer total:", getHandValue(st.session_state.dealerHand))
        else:
            st.write("No active players left (all busted).")

        if st.button("Resolve round", key="resolve_btn"):
            st.session_state.phase = 'resolve'
            st.rerun()
        return

    # ---------- RESOLVE ----------
    if st.session_state.phase == 'resolve':
        st.subheader("Round Results")
        dealerValue = getHandValue(st.session_state.dealerHand)
        for player in st.session_state.players:
            if player['bet'] == 0 or player['money'] <= 0:
                continue
            playerValue = getHandValue(player['hand'])
            bet = player.get('final_bet', player['bet'])
            if dealerValue > 21:
                st.write(f"{player['name']}: Dealer busts! You win ${bet}!")
                st.session_state.wins += 1
                player['money'] += bet
            elif playerValue > 21 or playerValue < dealerValue:
                st.write(f"{player['name']}: You lost ${bet}.")
                st.session_state.losses += 1
                player['money'] -= bet
            elif playerValue > dealerValue:
                st.write(f"{player['name']}: You won ${bet}!")
                st.session_state.wins += 1
                player['money'] += bet
            else:
                st.write(f"{player['name']}: It's a tie — bet returned.")
                st.session_state.ties += 1
            player['bet'] = 0
            player['final_bet'] = 0

        st.write("---")
        st.write(f"🏆 Stats: {st.session_state.wins} Wins | {st.session_state.losses} Losses | {st.session_state.ties} Ties")

        st.write("Player balances:")
        for player in st.session_state.players:
            st.write(f"{player['name']}: ${player['money']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Play another round", key="new_round_btn"):
                st.session_state.deck = getDeck()
                st.session_state.dealerHand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
                for p in st.session_state.players:
                    p['hand'] = []
                    p['bet'] = 0
                    p['final_bet'] = 0
                st.session_state.phase = 'betting'
                st.session_state.current_player_index = 0
                st.rerun()
        with col2:
            if st.button("Back to Home (end session)", key="end_session_btn"):
                st.session_state.phase = 'setup'
                st.rerun()