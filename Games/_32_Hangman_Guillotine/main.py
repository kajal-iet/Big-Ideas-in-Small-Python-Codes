import random
import streamlit as st

def run():

    # ------------------ PAGE CONFIG ------------------
    st.set_page_config(
        page_title="Hangman & Guillotine",
        layout="wide"
    )

    # ------------------ TERMINAL STYLE ------------------
    st.markdown("""
    <style>
    body { background-color: #0f1117; }
    .block-container { font-family: monospace; }
    .terminal {
        background-color: #000000;
        color: #33ff33;
        padding: 16px;
        border-radius: 6px;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- ASCII ART ------------------
    HANGMAN_PICS = [
r"""
 +--+
 |  |
    |
    |
    |
    |
=====""",
r"""
 +--+
 |  |
 O  |
    |
    |
    |
=====""",
r"""
 +--+
 |  |
 O  |
 |  |
    |
    |
=====""",
r"""
 +--+
 |  |
 O  |
/|  |
    |
    |
=====""",
r"""
 +--+
 |  |
 O  |
/|\ |
    |
    |
=====""",
r"""
 +--+
 |  |
 O  |
/|\ |
/   |
    |
=====""",
r"""
 +--+
 |  |
 O  |
/|\ |
/ \ |
    |
====="""
    ]

    GUILLOTINE_PICS = [
r"""
|        |
|        |
|        |
|        |
|        |
|        |
|===     |""",
r"""
|   |    |
|   |    |
|   |    |
|   |    |
|   |    |
|   |    |
|===|    |""",
r"""
|===|    |
|   |    |
|   |    |
|   |    |
|   |    |
|   |    |
|===|    |""",
r"""
|===|    |
|| /|    |
||/ |    |
|   |    |
|   |    |
|   |    |
|===|    |""",
r"""
|===|    |
|| /|    |
||/ |    |
|   |    |
|   |    |
|/-\|    |
|===|    |""",
r"""
|===|    |
|| /|    |
||/ |    |
|   |    |
|\ /|    |
|/-\|    |
|===|    |""",
r"""
|===|    |
|| /|    |
||/ |    |
|   |    |
|\O/|    |
|/-\|    |
|===|    |"""
    ]

    # ---------------- WORD CATEGORIES ------------------
    CATEGORIES = {
        "Animals": "ANT BABOON BADGER BAT BEAR CAMEL CAT DOG DONKEY DUCK EAGLE FOX FROG GOAT LION MONKEY OTTER PIGEON RABBIT TIGER WOLF ZEBRA".split(),
        "Fruits": "APPLE BANANA CHERRY GRAPE MANGO ORANGE PAPAYA PEACH PEAR PINEAPPLE".split(),
        "Countries": "INDIA CANADA FRANCE GERMANY ITALY JAPAN NEPAL NORWAY SPAIN SWEDEN".split()
    }

    # ------------------ STATE HELPERS ------------------
    def reset_game(category):
        st.session_state.category = category
        st.session_state.secret = random.choice(CATEGORIES[category])
        st.session_state.missed = []
        st.session_state.correct = []
        st.session_state.game_over = False
        st.session_state.logs = []

    # ------------------ INIT STATE ------------------
    if "category" not in st.session_state:
        reset_game(random.choice(list(CATEGORIES.keys())))
        st.session_state.style = "Hangman"
        st.session_state.prev_category = st.session_state.category

    # ------------------ TITLE & RULES ------------------
    st.title("🪢 Hangman & Guillotine")

    st.markdown("""
    **Guess the secret word before the drawing is complete!**

    **Rules**
    - Select a **category**
    - Choose **Hangman** or **Guillotine** style
    - Guess **one letter at a time**
    - Wrong guesses advance the drawing
    - Finish the word → **YOU WIN**
    - Finish the drawing → **GAME OVER**
    """)

    # ------------------ SETTINGS ------------------
    col1, col2 = st.columns(2)

    with col1:
        category = st.selectbox(
            "Choose Category",
            list(CATEGORIES.keys()),
            index=list(CATEGORIES.keys()).index(st.session_state.category)
        )

    # 🔁 Restart game ONLY if category changes
    if category != st.session_state.prev_category:
        reset_game(category)
        st.session_state.prev_category = category
        st.rerun()

    with col2:
        style = st.selectbox("Choose Style", ["Hangman", "Guillotine"])

    pics = HANGMAN_PICS if style == "Hangman" else GUILLOTINE_PICS

    # ------------------ DRAW GAME ------------------
    art = pics[len(st.session_state.missed)]
    blanks = [
        letter if letter in st.session_state.correct else "_"
        for letter in st.session_state.secret
    ]

    game_screen = f"""
{art}

Category: {st.session_state.category}

Missed letters: {" ".join(st.session_state.missed) if st.session_state.missed else "None"}

{" ".join(blanks)}
"""

    st.markdown(f"<div class='terminal'>{game_screen}</div>", unsafe_allow_html=True)

    # ------------------ INPUT ------------------
    guess = st.text_input(
        "Guess a letter",
        max_chars=1,
        disabled=st.session_state.game_over
    ).upper()

    if st.button("GUESS", disabled=st.session_state.game_over):
        if not guess.isalpha():
            st.warning("Please enter a letter.")
        elif guess in st.session_state.missed + st.session_state.correct:
            st.warning("You already guessed that letter.")
        elif guess in st.session_state.secret:
            st.session_state.correct.append(guess)
            if all(l in st.session_state.correct for l in st.session_state.secret):
                st.session_state.logs.append(
                    f"🎉 YOU WON! Word was {st.session_state.secret}"
                )
                st.session_state.game_over = True
        else:
            st.session_state.missed.append(guess)
            if len(st.session_state.missed) == len(pics) - 1:
                st.session_state.logs.append(
                    f"💀 GAME OVER — Word was {st.session_state.secret}"
                )
                st.session_state.game_over = True
        st.rerun()

    # ------------------ OUTPUT LOG ------------------
    if st.session_state.logs:
        st.markdown("#### Terminal Output")
        st.markdown(
            "<div class='terminal'>" + "\n".join(st.session_state.logs) + "</div>",
            unsafe_allow_html=True
        )

    # ------------------ RESTART ------------------
    if st.session_state.game_over:
        if st.button("🔁 Restart Game"):
            reset_game(st.session_state.category)
            st.rerun()


if __name__ == "__main__":
    run()
