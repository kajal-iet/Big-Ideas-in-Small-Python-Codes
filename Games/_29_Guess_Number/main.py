import random
import streamlit as st

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Guess the Number",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------ RESPONSIVE CSS ------------------
st.markdown("""
<style>
@media (max-width: 768px) {
    h1 { font-size: 1.6rem; }
    .block-container { padding: 1rem; }
}
div.stButton > button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


# ------------------ RESET GAME ------------------
def reset_game(max_num, max_attempts):
    st.session_state.secret = random.randint(1, max_num)
    st.session_state.history = []
    st.session_state.attempt_count = 0
    st.session_state.over = False
    st.session_state.max_attempts = max_attempts


# ------------------ APP ------------------
def run():
    st.title("🎯 Guess the Number")
    st.markdown(
        """
    - The system picks a **secret number** within the selected range.
    - Choose a **difficulty level**:
    - Easy: 1–50
    - Medium: 1–100
    - Hard: 1–500
    - You have a **limited number of attempts** to guess correctly.
    - Each guess counts as **one attempt**.
    - After every guess, you’ll get a hint:
    - 🔽 Too Low
    - 🔼 Too High
    - 🎉 Correct
    - When attempts run out → **Game Over**
    - Changing the difficulty **restarts the game**.
    """
    )

    # -------- Difficulty --------
    level = st.selectbox("Choose difficulty", ["Easy", "Medium", "Hard"])

    if level == "Easy":
        max_num, max_attempts = 50, 10
    elif level == "Medium":
        max_num, max_attempts = 100, 10
    else:
        max_num, max_attempts = 500, 12

    # -------- Track difficulty change --------
    if "current_level" not in st.session_state:
        st.session_state.current_level = level
        reset_game(max_num, max_attempts)

    if st.session_state.current_level != level:
        st.session_state.current_level = level
        reset_game(max_num, max_attempts)
        st.rerun()

    # -------- Input --------
    guess = st.number_input(
        "Enter your guess",
        min_value=1,
        max_value=max_num,
        step=1
    )

    # -------- Submit --------
    if st.button("Submit Guess", disabled=st.session_state.over):
        if st.session_state.attempt_count < max_attempts:
            st.session_state.attempt_count += 1  # ✅ FIRST MOVE COUNTS

            if guess == st.session_state.secret:
                st.session_state.history.append((guess, "🎉 Correct"))
                st.success("🎉 Correct! You guessed the number!")
                st.session_state.over = True
            elif guess < st.session_state.secret:
                st.session_state.history.append((guess, "🔽 Too Low"))
            else:
                st.session_state.history.append((guess, "🔼 Too High"))

            if st.session_state.attempt_count >= max_attempts and not st.session_state.over:
                st.error(f"❌ Game Over! Number was **{st.session_state.secret}**")
                st.session_state.over = True

        st.rerun()  # 🔑 FORCE UI TO UPDATE IMMEDIATELY

    # -------- Remaining (CALCULATED AFTER SUBMIT) --------
    remaining = max_attempts - st.session_state.attempt_count

    st.markdown(f"""
    <div style="
        display:flex;
        justify-content:space-between;
        padding:8px;
        border-radius:8px;
        background:#f9f9f9;
        margin-bottom:12px;
        font-size:14px;
    ">
        <span>🎯 Range: 1 – {max_num}</span>
        <span>⏳ Remaining Attempts: {remaining}</span>
    </div>
    """, unsafe_allow_html=True)

    # -------- Guess History --------
    if st.session_state.history:
        st.markdown("### 🧾 Guess History")
        for g, hint in st.session_state.history:
            st.write(f"**{g}** → {hint}")

    # -------- Smart Hint --------
    if remaining <= 3 and not st.session_state.over:
        lows = [g for g, h in st.session_state.history if "Low" in h]
        highs = [g for g, h in st.session_state.history if "High" in h]
        low = max(lows) if lows else 1
        high = min(highs) if highs else max_num
        st.info(f"💡 Hint: Number is between **{low} and {high}**")

    # -------- Restart --------
    if st.session_state.over:
        if st.button("🔁 Play Again"):
            reset_game(max_num, max_attempts)
            st.rerun()


# ------------------ RUN ------------------
if __name__ == "__main__":
    run()
