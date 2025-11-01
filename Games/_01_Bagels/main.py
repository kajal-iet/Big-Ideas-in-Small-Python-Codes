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
    st.title("🧩 Bagels – Deductive Logic Game")

    st.markdown("""
    Welcome to **Bagels**, a deductive logic guessing game inspired by *Al Sweigart’s Big Book of Small Python Projects*.

    ---
    **🎯 Goal:**  
    Guess the secret number with no repeating digits!  

    **💡 Clues:**  
    - **Fermi** → One digit is correct and in the right position  
    - **Pico** → One digit is correct but in the wrong position  
    - **Bagels** → No digit is correct  

    Try to guess the number before you run out of attempts!
    ---
    """)

    # --- Difficulty selection ---
    level = st.selectbox("Choose difficulty level", ["Easy", "Medium", "Hard"])

    if level == "Easy":
        num_digits, max_guesses, points = 3, 10, 1
    elif level == "Medium":
        num_digits, max_guesses, points = 4, 15, 2
    else:
        num_digits, max_guesses, points = 5, 20, 3

    # --- Track and handle difficulty change ---
    if "current_level" not in st.session_state:
        st.session_state.current_level = level

    if st.session_state.current_level != level:
        st.session_state.current_level = level
        st.session_state.secret = generate_secret_number(num_digits)
        st.session_state.guesses = []
        st.session_state.over = False
        st.session_state.input_key = 0
        st.session_state.score = 0
        st.rerun()

    # --- Initialize session state if not set ---
    if "secret" not in st.session_state:
        st.session_state.secret = generate_secret_number(num_digits)
        st.session_state.guesses = []
        st.session_state.score = 0
        st.session_state.over = False
        st.session_state.input_key = 0

    # --- Display Score + Remaining Guesses ---
    remaining = max_guesses - len(st.session_state.guesses)
    st.markdown(
        f"""
        <div style="
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 6px 12px;
            display: flex;
            justify-content: space-between;
            background-color: #f9f9f9;
            font-size: 13px;
            margin-bottom: 12px;
        ">
            <span>🧮 <b>Score:</b> {st.session_state.score}</span>
            <span>⏳ <b>Remaining Guesses:</b> {remaining}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Input + Submit ---
    guess = st.text_input(
        f"Enter your {num_digits}-digit guess:",
        key=f"guess_input_{st.session_state.input_key}"
    )

    if st.button("Submit Guess") and not st.session_state.over:
        if len(guess) == num_digits and guess.isdigit():
            clue = get_clues(guess, st.session_state.secret)
            st.session_state.guesses.append((guess, clue))

            if clue == "🎉 You got it!":
                st.success(f"🎯 You guessed it! The secret number was **{st.session_state.secret}**.")
                st.session_state.score += points
                st.session_state.over = True

            elif len(st.session_state.guesses) >= max_guesses:
                st.error(f"❌ Out of guesses! The number was **{st.session_state.secret}**.")
                st.session_state.over = True
        else:
            st.warning(f"⚠️ Please enter a valid {num_digits}-digit number.")

    # --- Show previous guesses ---
    if st.session_state.guesses:
        st.markdown("### 🧾 Your Guesses:")
        for g, c in st.session_state.guesses:
            st.write(f"**{g}** → {c}")

    # --- Play Again ---
    if st.session_state.over:
        if st.button("🔁 Play Again"):
            st.session_state.secret = generate_secret_number(num_digits)
            st.session_state.guesses = []
            st.session_state.over = False
            st.session_state.input_key += 1
            st.rerun()


# For running directly
if __name__ == "__main__":
    run()
