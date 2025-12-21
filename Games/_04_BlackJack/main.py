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
    st.title("🃏 Blackjack (Streamlit edition)")

    # ---------- MOBILE RESPONSIVE CSS (UI ONLY) ----------
    st.markdown("""
    <style>
    .block-container {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }

    pre {
        overflow-x: auto;
        white-space: pre;
        font-size: 0.8rem;
        line-height: 1.2;
    }

    @media (max-width: 768px) {
        .stButton > button {
            width: 100%;
            margin-bottom: 0.5rem;
        }

        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }

        section[data-testid="stSidebar"] {
            width: 72vw !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

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
            step=1
        )
        st.session_state.numPlayers = num

        player_names = []
        for i in range(num):
            name = st.text_input(f"Name for Player {i+1}:", value=f"Player{i+1}")
            player_names.append(name)

        if st.button("Start Round"):
            players = []
            existing = {p['name']: p for p in st.session_state.players} if st.session_state.players else {}
            for nm in player_names:
                pmoney = existing.get(nm, {}).get('money', 5000)
                players.append({'name': nm, 'money': pmoney, 'hand': [], 'bet': 0, 'final_bet': 0})
            st.session_state.players = players
            st.session_state.deck = getDeck()
            st.session_state.dealerHand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
            st.session_state.current_player_index = 0
            st.session_state.phase = 'betting'
            st.rerun()
        return

    # ---------- BETTING ----------
    if st.session_state.phase == 'betting':
        st.subheader("Place Bets")
        for i, player in enumerate(st.session_state.players):
            st.write(f"**{player['name']}** — Money: ${player['money']}")
            if player['bet'] == 0 and player['money'] > 0:
                bet = st.number_input(
                    f"Bet for {player['name']}",
                    min_value=1,
                    max_value=player['money'],
                    value=1,
                    key=f"bet_{i}"
                )
                if st.button(f"Confirm bet for {player['name']}"):
                    player['bet'] = int(bet)
                    player['hand'] = [st.session_state.deck.pop(), st.session_state.deck.pop()]
                    st.rerun()
        if all(p['bet'] > 0 or p['money'] <= 0 for p in st.session_state.players):
            st.session_state.phase = 'play'
            st.rerun()
        return

    # ---------- PLAY ----------
    if st.session_state.phase == 'play':
        p = st.session_state.players[st.session_state.current_player_index]
        st.subheader(f"Turn: {p['name']}")

        st.markdown(
            f"<pre>{render_cards([BACKSIDE] + st.session_state.dealerHand[1:], True)}</pre>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<pre>{render_cards(p['hand'])}</pre>",
            unsafe_allow_html=True
        )
        st.write("Total:", getHandValue(p['hand']))

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Hit"):
                p['hand'].append(st.session_state.deck.pop())
                st.rerun()
        with col2:
            if st.button("Stand"):
                st.session_state.current_player_index += 1
                st.rerun()
        with col3:
            if len(p['hand']) == 2 and p['money'] >= p['bet'] * 2:
                if st.button("Double Down"):
                    p['bet'] *= 2
                    p['hand'].append(st.session_state.deck.pop())
                    st.session_state.current_player_index += 1
                    st.rerun()
        return

    # ---------- DEALER ----------
    if st.session_state.phase == 'dealer':
        st.subheader("Dealer Turn")
        st.markdown(
            f"<pre>{render_cards(st.session_state.dealerHand)}</pre>",
            unsafe_allow_html=True
        )
        st.session_state.dealerHand = dealer_ai_play(
            st.session_state.deck,
            st.session_state.dealerHand,
            difficulty
        )
        if st.button("Resolve round"):
            st.session_state.phase = 'resolve'
            st.rerun()
        return

    # ---------- RESOLVE ----------
    if st.session_state.phase == 'resolve':
        st.subheader("Round Results")
        dealerValue = getHandValue(st.session_state.dealerHand)
        for p in st.session_state.players:
            if p['bet'] > 0:
                pv = getHandValue(p['hand'])
                if pv <= 21 and (dealerValue > 21 or pv > dealerValue):
                    p['money'] += p['bet']
                else:
                    p['money'] -= p['bet']
                p['bet'] = 0

        if st.button("Play another round"):
            st.session_state.phase = 'betting'
            st.session_state.deck = getDeck()
            st.session_state.dealerHand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
            st.session_state.current_player_index = 0
            for p in st.session_state.players:
                p['hand'] = []
            st.rerun()


if __name__ == "__main__":
    run()
