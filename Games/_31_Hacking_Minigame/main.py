import random
import streamlit as st

def run():

    # ------------------ PAGE CONFIG ------------------
    st.set_page_config(
        page_title="Hacking Minigame",
        layout="wide"
    )
    

    # ------------------ TERMINAL STYLE ------------------
    st.markdown("""
    <style>
    body {
        background-color: #0f1117;
    }
    .block-container {
        font-family: monospace;
    }
    .terminal {
        background-color: #000000;
        color: #33ff33;
        padding: 16px;
        border-radius: 6px;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

    # ------------------ WORD LIST ------------------
    WORDS = [
        "MONITOR", "CONTAIN", "RESOLVE", "CHICKEN", "ADDRESS",
        "DESPITE", "DISPLAY", "PENALTY", "IMPROVE", "REFUGEE",
        "CAPTURE", "COMPUTE", "HANGING", "MISSION", "NETWORK"
    ]

    MAX_TRIES = 4


    # ------------------ HELPERS ------------------
    def matching_letters(a, b):
        return sum(1 for i in range(len(a)) if a[i] == b[i])


    def heat_label(matches):
        if matches <= 1:
            return "🧊 Cold"
        elif matches <= 4:
            return "🌡 Warm"
        else:
            return "🔥 Hot"


    def reset_game():
        st.session_state.words = random.sample(WORDS, 12)
        st.session_state.secret = random.choice(st.session_state.words)
        st.session_state.tries = 0
        st.session_state.logs = []
        st.session_state.locked = False


    # ------------------ INIT STATE ------------------
    if "secret" not in st.session_state:
        reset_game()

    # ------------------ UI ------------------
    st.title("🖥️ Hacking Minigame")
    st.markdown(
        """
        
        - One of the displayed **7-letter words** is the password.
        - You have **4 attempts** to guess it.
        - Enter **only words shown** in the list.
        - After each guess, you’ll see:
        - **X/7 correct** → letters in the correct position
        - 🧊 Cold (0–1) | 🌡 Warm (2–4) | 🔥 Hot (5–6)
        - Guess correctly → **ACCESS GRANTED**
        - Run out of attempts → **SYSTEM LOCKED**
        """
    )

    st.markdown("#### Find the password in the computer memory")

    # ------------------ MEMORY DISPLAY ------------------
    memory_display = "\n".join(st.session_state.words)

    st.markdown(
        f"<div class='terminal'>{memory_display}</div>",
        unsafe_allow_html=True
    )

    # ------------------ INPUT ------------------
    guess = st.text_input(
        "Enter password",
        disabled=st.session_state.locked
    ).upper()

    if st.button("EXECUTE", disabled=st.session_state.locked):
        if guess not in st.session_state.words:
            st.warning("That is not one of the possible passwords.")
        else:
            st.session_state.tries += 1
            matches = matching_letters(st.session_state.secret, guess)
            heat = heat_label(matches)

            if guess == st.session_state.secret:
                st.session_state.logs.append("A C C E S S   G R A N T E D")
                st.success("ACCESS GRANTED")
                st.session_state.locked = True
            else:
                st.session_state.logs.append(
                    f"ACCESS DENIED ({matches}/7 correct) — {heat}"
                )

            if st.session_state.tries >= MAX_TRIES and not st.session_state.locked:
                st.session_state.logs.append(
                    f"SYSTEM LOCKED — PASSWORD WAS {st.session_state.secret}"
                )
                st.session_state.locked = True

    # ------------------ OUTPUT LOG ------------------
    if st.session_state.logs:
        st.markdown("#### Terminal Output")
        st.markdown(
            "<div class='terminal'>" + "\n".join(st.session_state.logs) + "</div>",
            unsafe_allow_html=True
        )

    # ------------------ RESTART ------------------
    if st.session_state.locked:
        if st.button("🔁 Restart Hack"):
            reset_game()
            st.rerun()



if __name__ == "__main__":
    run()
