import random
import streamlit as st


def generate_secret_number(num_digits):
    numbers = list('0123456789')
    random.shuffle(numbers)
    return ''.join(numbers[:num_digits])


def get_clues(guess, secret):
    if guess == secret:
        return "🎉 You got it!"
    clues = []
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            clues.append("Fermi")
        elif guess[i] in secret:
            clues.append("Pico")
    if not clues:
        return "Bagels"
    return ' '.join(sorted(clues))


def run():

    # ---------------- UI STYLES (ONLY UI) ----------------
    st.markdown("""
    <style>
    .game-container {
        max-width: 520px;
        margin: auto;
        padding: 10px;
    }
    .info-bar {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        margin-bottom: 12px;
        flex-wrap: wrap;
    }
    .info-chip {
        flex: 1;
        min-width: 140px;
        padding: 8px 12px;
        border-radius: 12px;
        background: #f4f6f8;
        text-align: center;
        font-size: 14px;
    }
    input[type="text"] {
        font-size: 18px !important;
        text-align: center;
        letter-spacing: 4px;
    }
    button {
        width: 100%;
        border-radius: 14px;
        font-size: 16px;
        padding: 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="game-container">', unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.title("🧩 Bagels – Deductive Logic Game")

    st.markdown("""
    Guess the **secret number** with **no repeated digits**.

    **Clues**
    - **Fermi** → Correct digit & position  
    - **Pico** → Correct digit, wrong position  
    - **Bagels** → No digits correct  
    """)

    # ---------------- DIFFICULTY ----------------
    level = st.selectbox(
        "🎚️ Difficulty",
        ["Easy", "Medium", "Hard"],
        index=0
    )

    if level == "Easy":
        num_digits, max_guesses, points = 3, 10, 1
    elif level == "Medium":
        num_digits, max_guesses, points = 4, 15, 2
    else:
        num_digits, max_guesses, points = 5, 20, 3

    # ---------------- SESSION STATE ----------------
    if "current_level" not in st.session_state:
        st.session_state.current_level = level

    if st.session_state.current_level != level:
        st.session_state.current_level = level
        st.session_state.secret = generate_secret_number(num_digits)
        st.session_state.guesses = []
        st.session_state.over = False
        st.session_state.input_key = 0
        st.session_state.score = 0
        st.session_state.moves_used = 0
        st.rerun()

    if "secret" not in st.session_state:
        st.session_state.secret = generate_secret_number(num_digits)
        st.session_state.guesses = []
        st.session_state.score = 0
        st.session_state.over = False
        st.session_state.input_key = 0
        st.session_state.moves_used = 0

    # ---------------- INFO BAR ----------------
    remaining = max_guesses - st.session_state.moves_used

    st.markdown(
        f"""
        <div class="info-bar">
            <div class="info-chip">🧮 <b>Score</b><br>{st.session_state.score}</div>
            <div class="info-chip">⏳ <b>Remaining</b><br>{remaining}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- INPUT ----------------
    guess = st.text_input(
        f"Enter {num_digits}-digit guess",
        max_chars=num_digits,
        key=f"guess_input_{st.session_state.input_key}"
    )

    if st.button("▶ Submit Guess", disabled=st.session_state.over):
     if len(guess) == num_digits and guess.isdigit():
        clue = get_clues(guess, st.session_state.secret)
        st.session_state.guesses.append((guess, clue))
        st.session_state.moves_used += 1  # one move per submit

        if clue == "🎉 You got it!":
            st.success(f"🎯 Correct! The number was **{st.session_state.secret}**")
            st.session_state.score += points
            st.session_state.over = True

        elif st.session_state.moves_used >= max_guesses:
            st.error(f"❌ Out of guesses! The number was **{st.session_state.secret}**")
            st.session_state.over = True

        st.rerun()  # 🔑 force UI to update immediately


    # ---------------- GUESS HISTORY ----------------
    if st.session_state.guesses:
        st.markdown("### 🧾 Your Guesses")
        for g, c in st.session_state.guesses[::-1]:
            st.markdown(f"**{g}** → {c}")

    # ---------------- PLAY AGAIN ----------------
    if st.session_state.over:
        if st.button("🔁 Play Again"):
            st.session_state.secret = generate_secret_number(num_digits)
            st.session_state.guesses = []
            st.session_state.moves_used = 0
            st.session_state.over = False
            st.session_state.input_key += 1
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    run()
