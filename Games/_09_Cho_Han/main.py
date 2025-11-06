import streamlit as st
import random
import time
import os

# --- Constants ---
JAPANESE_NUMBERS = {1: 'ICHI', 2: 'NI', 3: 'SAN', 4: 'SHI', 5: 'GO', 6: 'ROKU'}
DICE_UNICODE = {1: '⚀', 2: '⚁', 3: '⚂', 4: '⚃', 5: '⚄', 6: '⚅'}

SHAKE_AUDIO = "shake.wav"
SLAM_AUDIO = "slam.wav"

# --- Helpers ---
def play_audio_if_exists(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            st.audio(f.read())

def animate_dice(duration_secs=1.2, fps=12):
    placeholder = st.empty()
    for _ in range(int(duration_secs * fps)):
        a, b = random.randint(1, 6), random.randint(1, 6)
        placeholder.markdown(
            f"<div style='font-size:72px;text-align:center'>{DICE_UNICODE[a]}&nbsp;&nbsp;{DICE_UNICODE[b]}</div>",
            unsafe_allow_html=True
        )
        time.sleep(1 / fps)
    return placeholder

def init_state():
    if "purse" not in st.session_state:
        st.session_state.purse = 5000
    if "pot" not in st.session_state:
        st.session_state.pot = 0
    if "bet_choice" not in st.session_state:
        st.session_state.bet_choice = None
    if "rolled" not in st.session_state:
        st.session_state.rolled = False
    if "dice" not in st.session_state:
        st.session_state.dice = (None, None)
    if "result" not in st.session_state:
        st.session_state.result = None

# --- Main ---
def run():
    st.title("🎲 Cho-Han — Even or Odd Dice Game")
    st.markdown(
        """
        **Cho-Han** is a traditional Japanese dice game:  
        Two dice are rolled and you guess if the total is **even (CHO)** or **odd (HAN)**.  
        You start with **5000 mon**. The house takes a 10% fee from winnings.
        """
    )
    st.divider()

    init_state()

    st.markdown(f"### 💰 Purse: **{st.session_state.purse} mon**")

    # BETTING
    st.markdown("1️. Place Your Bet")
    st.session_state.pot = st.number_input(
        "Bet amount",
        min_value=1,
        max_value=st.session_state.purse or 1,
        value=100,
        step=50
    )

    # CHO / HAN
    st.markdown("2️. Choose CHO (Even) or HAN (Odd)")
    st.session_state.bet_choice = st.radio(
        "Your call:",
        ["CHO", "HAN"],
        horizontal=True,
    )

    # ROLL
    st.markdown("3️. Roll the Dice")
    if st.button("🎲 Roll Dice", key="roll_button"):
        st.session_state.rolled = True
        play_audio_if_exists(SHAKE_AUDIO)
        placeholder = animate_dice()
        play_audio_if_exists(SLAM_AUDIO)
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        st.session_state.dice = (d1, d2)
        placeholder.markdown(
            f"<div style='font-size:88px;text-align:center'>{DICE_UNICODE[d1]}&nbsp;&nbsp;{DICE_UNICODE[d2]}</div>",
            unsafe_allow_html=True,
        )
        st.session_state.result = (d1, d2)

    # RESULT SECTION
    if st.session_state.rolled and st.session_state.result:
        d1, d2 = st.session_state.result
        roll_sum = d1 + d2
        correct = "CHO" if roll_sum % 2 == 0 else "HAN"

        st.divider()
        st.markdown("4️. Outcome")
        st.markdown(f"**Rolled:** `{JAPANESE_NUMBERS[d1]} - {JAPANESE_NUMBERS[d2]}`  → ({d1} + {d2} = {roll_sum})")

        if st.session_state.bet_choice == correct:
            fee = st.session_state.pot // 10
            net = st.session_state.pot - fee
            st.success(f"You won! You take {net} mon (after {fee} mon house fee).")
            st.session_state.purse += net
        else:
            st.error(f"You lost {st.session_state.pot} mon! Correct was {correct}.")
            st.session_state.purse -= st.session_state.pot

        st.markdown(f"**💰 Updated Purse:** {st.session_state.purse} mon")

        # Play Again
        if st.button("🔁 Play Again", key="again_button"):
            st.session_state.rolled = False
            st.session_state.result = None
            st.session_state.pot = 0
            st.session_state.bet_choice = None
            st.rerun()

    st.divider()
    st.caption("🎋 Traditional Japanese dice game simulation — try bluffing yourself!")

if __name__ == "__main__":
    run()
