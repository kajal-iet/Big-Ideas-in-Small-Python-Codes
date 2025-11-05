# chohan_app.py
import streamlit as st
import random
import time
import os

# --- Constants ---
JAPANESE_NUMBERS = {1: 'ICHI', 2: 'NI', 3: 'SAN', 4: 'SHI', 5: 'GO', 6: 'ROKU'}
DICE_UNICODE = {1: '⚀', 2: '⚁', 3: '⚂', 4: '⚃', 5: '⚄', 6: '⚅'}

SHAKE_AUDIO = "shake.wav"  # optional: place in app folder
SLAM_AUDIO = "slam.wav"    # optional: place in app folder

# --- Helpers ---
def play_audio_if_exists(path):
    """Play audio if file exists in the app folder."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            st.audio(f.read())
        return True
    return False

def animate_dice(duration_secs=1.2, fps=12, placeholder=None):
    """Simple emoji-based dice 'rolling' animation."""
    frames = []
    # create simple frames of random dice icons
    for _ in range(int(duration_secs * fps)):
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        frames.append((a, b))
    # show frames
    for a, b in frames:
        if placeholder:
            placeholder.markdown(
                f"<div style='font-size:72px; text-align:center'>{DICE_UNICODE[a]}&nbsp;&nbsp;{DICE_UNICODE[b]}</div>",
                unsafe_allow_html=True
            )
        time.sleep(1 / fps)

def init_state():
    """Initialize session state keys we use."""
    if 'purse' not in st.session_state:
        st.session_state.purse = 5000
    if 'pot' not in st.session_state:
        st.session_state.pot = 0
    if 'bet_choice' not in st.session_state:
        st.session_state.bet_choice = None  # 'CHO' or 'HAN'
    if 'dice' not in st.session_state:
        st.session_state.dice = (None, None)
    if 'message' not in st.session_state:
        st.session_state.message = ""
    if 'step' not in st.session_state:
        st.session_state.step = 0  # 0: place bet, 1: choose CHO/HAN, 2: reveal, 3: result

# --- Main app ---
def run():
    st.set_page_config(page_title="🎲 Cho-Han", layout="centered")
    st.title("🎲 Cho-Han — Even or Odd Dice Game")
    st.markdown(
        """
        **Cho-Han** is a traditional Japanese dice game: two dice are rolled and you guess if the sum is **even (CHO)** or **odd (HAN)**.
        Start with **5000 mon**. The house takes a 10% fee from winnings.
        """
    )
    st.divider()

    init_state()

    # Show purse and controls in a compact layout
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown(f"### 💰 Purse: **{st.session_state.purse} mon**")
    with col_right:
        if st.button("🧹 Reset Session"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.experimental_rerun()

    st.write("")  # spacing

    # STEP 0: Place bet
    if st.session_state.step in (0, ):
        st.subheader("Place your bet")
        st.write("Enter how much you want to bet this round (or press QUIT).")
        pot_input = st.number_input("Bet amount", min_value=1, max_value=st.session_state.purse or 1, value=100, step=50, key="pot_input")
        col_b1, col_b2 = st.columns([2, 1])
        with col_b1:
            if st.button("Place Bet"):
                if pot_input <= 0:
                    st.warning("Please bet a positive amount.")
                elif pot_input > st.session_state.purse:
                    st.warning("You don't have enough money for that bet.")
                else:
                    st.session_state.pot = int(pot_input)
                    st.session_state.step = 1
                    st.session_state.message = ""
                    st.experimental_rerun()
        with col_b2:
            if st.button("QUIT"):
                st.info("Thanks for playing Cho-Han!")
                st.stop()

    # STEP 1: Choose CHO or HAN
    elif st.session_state.step == 1:
        st.subheader("CHO (even) or HAN (odd)?")
        st.write(f"Your current bet: **{st.session_state.pot} mon**")
        colc1, colc2 = st.columns(2)
        with colc1:
            if st.button("CHO (Even)"):
                st.session_state.bet_choice = 'CHO'
                st.session_state.step = 2
                st.experimental_rerun()
        with colc2:
            if st.button("HAN (Odd)"):
                st.session_state.bet_choice = 'HAN'
                st.session_state.step = 2
                st.experimental_rerun()

    # STEP 2: Animate roll & reveal
    elif st.session_state.step == 2:
        st.subheader("Rolling the dice...")
        st.write("Dealer swirls the bamboo cup and slams it down.")
        animation_placeholder = st.empty()

        # Play shake audio if available
        played = play_audio_if_exists(SHAKE_AUDIO)

        # animate
        animate_dice(duration_secs=1.2, fps=14, placeholder=animation_placeholder)

        # slam audio (optional)
        play_audio_if_exists(SLAM_AUDIO)

        # perform real roll
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        st.session_state.dice = (d1, d2)

        # show final dice big
        animation_placeholder.markdown(
            f"<div style='font-size:88px; text-align:center'>{DICE_UNICODE[d1]}&nbsp;&nbsp;{DICE_UNICODE[d2]}</div>",
            unsafe_allow_html=True
        )

        # show japanese numbers + numeric
        st.markdown(f"**Result:** `{JAPANESE_NUMBERS[d1]} - {JAPANESE_NUMBERS[d2]}`  &nbsp;&nbsp; **({d1} - {d2})**")

        st.session_state.step = 3

        # small pause so user sees result before pressing continue
        time.sleep(0.25)
        st.button("➡️ See Outcome", on_click=lambda: st.session_state.update({'step': 3}))

    # STEP 3: Outcome and scoring
    elif st.session_state.step == 3:
        d1, d2 = st.session_state.dice
        if d1 is None or d2 is None:
            st.error("No dice rolled. Please start a new round.")
            if st.button("Start New Round"):
                st.session_state.step = 0
                st.experimental_rerun()
            st.stop()

        roll_is_even = (d1 + d2) % 2 == 0
        correct = 'CHO' if roll_is_even else 'HAN'
        won = (st.session_state.bet_choice == correct)

        st.subheader("Outcome")
        if won:
            winnings = st.session_state.pot
            fee = winnings // 10  # 10% house fee
            net = winnings - fee
            st.success(f"You won! You take {winnings} mon. House collects {fee} mon fee. Net gain: {net} mon.")
            st.session_state.purse += net
        else:
            st.error(f"You lost {st.session_state.pot} mon.")
            st.session_state.purse -= st.session_state.pot

        # show final totals and roll outcome
        st.markdown(f"**Roll sum:** {d1 + d2} — **{correct}** was the correct call.")
        st.markdown(f"**Your bet:** {st.session_state.bet_choice} — **You {'won' if won else 'lost'}**")

        # Reset per-round fields but keep purse
        st.session_state.pot = 0
        st.session_state.bet_choice = None
        st.session_state.dice = (None, None)

        # Offer next actions
        coln1, coln2, coln3 = st.columns(3)
        with coln1:
            if st.button("🔁 New Round"):
                st.session_state.step = 0
                st.experimental_rerun()
        with coln2:
            if st.button("🏁 Cash Out & Quit"):
                st.success(f"You cash out with {st.session_state.purse} mon. Thanks for playing!")
                st.stop()
        with coln3:
            if st.button("🧹 Reset Session"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.experimental_rerun()

    # Footer / tips
    st.divider()
    st.caption("Tip: provide `shake.wav` and `slam.wav` in the app folder to enable audio effects. Use emoji dice or GIFs for richer visuals.")
    st.caption("Made with ❤️ — enjoy responsibly!")

# Run when executed directly
if __name__ == "__main__":
    run()
