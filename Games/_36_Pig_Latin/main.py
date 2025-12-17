import streamlit as st
import random
import re

# ------------------ CONFIG ------------------
VOWELS = ("a", "e", "i", "o", "u")

SENTENCES = [
    "Pig Latin is fun",
    "Hello world!",
    "This game is awesome",
    "Python makes coding enjoyable",
    "Streamlit is very powerful",
    "Can you translate this sentence?",
    "Programming is not magic",
    "String manipulation is tricky",
    "Watch out for punctuation!",
    "HELLO THERE",
    "I love Python!",
    "Do robots eat food?",
    "Artificial Intelligence is fascinating",
    "Quick brown fox jumps",
    "Why is Pig Latin funny?",
    "Multiple players make it fun",
    "Try not to cheat!",
    "Practice makes progress",
    "Never stop learning"
]

# ------------------ PIG LATIN LOGIC ------------------
def english_to_pig_latin(sentence):
    output = []

    for word in sentence.split():
        prefix = re.match(r"^\W*", word).group()
        suffix = re.search(r"\W*$", word).group()
        core = word[len(prefix):len(word) - len(suffix)]

        if not core.isalpha():
            output.append(word)
            continue

        was_upper = core.isupper()
        was_title = core.istitle()

        core = core.lower()

        match = re.match(r"[^aeiou]+", core)
        if match:
            cons = match.group()
            pig = core[len(cons):] + cons + "ay"
        else:
            pig = core + "yay"

        if was_upper:
            pig = pig.upper()
        elif was_title:
            pig = pig.capitalize()

        output.append(prefix + pig + suffix)

    return " ".join(output)

# ------------------ GAME STATE ------------------
def new_round():
    text = random.choice(SENTENCES)
    st.session_state.question = text
    st.session_state.answer = english_to_pig_latin(text)
    st.session_state.user_input = ""
    st.session_state.submitted = False
    st.session_state.correct = None

def reset_game():
    st.session_state.scores = [0, 0]
    st.session_state.turn = 0
    new_round()

# ------------------ UI ------------------
def run():
    st.set_page_config("Pig Latin Multiplayer", layout="centered")

    st.title("🐷 Pig Latin – Multiplayer")
    # -------- Rules --------
    with st.expander("📜 Rules"):
        st.markdown("""
- **Vowel start → `yay`** → `apple → appleyay`
- **Consonant start → move consonants + `ay`** → `pig → igpay`
- Preserve **punctuation & capitalization**
- Correct answer gives **+1 point**
        """)

    if "scores" not in st.session_state:
        reset_game()

    # -------- Scoreboard --------
    c1, c2 = st.columns(2)
    c1.metric("🧑 Player 1", st.session_state.scores[0])
    c2.metric("🧑 Player 2", st.session_state.scores[1])

    current_player = st.session_state.turn + 1
    st.markdown(f"### 🔄 Player {current_player}'s Turn")

    # -------- Question --------
    st.markdown("### 🔤 Convert to Pig Latin:")
    st.code(st.session_state.question)

    # -------- Input --------
    st.session_state.user_input = st.text_input(
        "Your answer:",
        disabled=st.session_state.submitted
    )

    # -------- Submit --------
    if st.button("✅ Submit", disabled=st.session_state.submitted):
        st.session_state.submitted = True
        if st.session_state.user_input.strip() == st.session_state.answer:
            st.session_state.correct = True
            st.session_state.scores[st.session_state.turn] += 1
        else:
            st.session_state.correct = False

    # -------- Feedback --------
    if st.session_state.submitted:
        if st.session_state.correct:
            st.success("🎉 Correct!")
        else:
            st.error("❌ Incorrect")
            st.info(f"Correct answer:\n**{st.session_state.answer}**")

        if st.button("➡ Next Turn"):
            st.session_state.turn = 1 - st.session_state.turn
            new_round()
            st.rerun()

    # -------- Restart --------
    st.markdown("---")
    if st.button("🔄 Restart Game"):
        reset_game()
        st.rerun()

# ------------------ RUN ------------------
if __name__ == "__main__":
    run()
