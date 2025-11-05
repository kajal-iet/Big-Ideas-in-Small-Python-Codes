import streamlit as st
import random

def run():
    st.set_page_config(page_title="🥕 Carrot Bluff", layout="centered")
    st.title("🥕 Carrot Bluff Game")
    st.markdown("""
**Carrot in a Box** is a two-player bluffing game where:

- Two boxes are placed before the players — one has a carrot, one doesn’t  
- Player 1 secretly peeks into their box  
- They can tell the truth or bluff about whether their box contains the carrot  
- Player 2 then decides whether to swap boxes or keep their own  
- Finally, both boxes are opened to reveal who gets the carrot — and who’s been fooled 🥕😄
""")

    # --- Initialize session state ---
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'carrot_in_red' not in st.session_state:
        st.session_state.carrot_in_red = random.choice([True, False])
    if 'swapped' not in st.session_state:
        st.session_state.swapped = False
    if 'peeked' not in st.session_state:
        st.session_state.peeked = False
    if 'p1_name' not in st.session_state:
        st.session_state.p1_name = ""
    if 'p2_name' not in st.session_state:
        st.session_state.p2_name = ""
    if 'p1_score' not in st.session_state:
        st.session_state.p1_score = 0
    if 'p2_score' not in st.session_state:
        st.session_state.p2_score = 0

    # --- Reset functions ---
    def reset_round():
        st.session_state.step = 1
        st.session_state.carrot_in_red = random.choice([True, False])
        st.session_state.swapped = False
        st.session_state.peeked = False
        st.rerun()

    def reset_all():
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    def go_to_step(next_step: int):
        st.session_state.step = next_step
        st.rerun()

    # --- Scoreboard Box ---
    st.markdown(
        f"""
        <div style="
            border: 2px solid #FFB74D;
            border-radius: 10px;
            background-color: #FFF3E0;
            padding: 10px;
            margin-bottom: 20px;
            text-align: center;">
            <h4>🏆 Scoreboard</h4>
            <div style="display: flex; justify-content: space-around; font-size: 18px;">
                <div><b>{st.session_state.p1_name or 'Player 1'}</b><br>{st.session_state.p1_score}</div>
                <div><b>{st.session_state.p2_name or 'Player 2'}</b><br>{st.session_state.p2_score}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Step 0: Get player names ---
    if st.session_state.step == 0:
        st.subheader("🎭 Enter Player Names")
        st.session_state.p1_name = st.text_input("Player 1 name (Red Box):", st.session_state.p1_name)
        st.session_state.p2_name = st.text_input("Player 2 name (Gold Box):", st.session_state.p2_name)

        if st.button("Start Game ▶️"):
            if st.session_state.p1_name and st.session_state.p2_name:
                go_to_step(1)
            else:
                st.warning("Please enter both names to start.")

    # --- Step 1: Player 1 peeks ---
    elif st.session_state.step == 1:
        st.subheader(f"{st.session_state.p1_name}, it's your turn to peek 👀")
        st.caption(f"{st.session_state.p2_name}, please look away!")

        if not st.session_state.peeked:
            if st.button("🔎 Peek inside the Red Box"):
                st.session_state.peeked = True
                st.rerun()
        else:
            if st.session_state.carrot_in_red:
                st.success("🥕 You see the carrot inside the RED box!")
            else:
                st.info("❌ The carrot is NOT in your box.")

            st.button("➡️ Continue", on_click=lambda: go_to_step(2))

    # --- Step 2: Swap or Not ---
    elif st.session_state.step == 2:
        st.subheader(f"{st.session_state.p2_name}, your move 🎲")
        st.caption(f"Now {st.session_state.p2_name}, you can choose to swap boxes or keep your own.")

        col1, col2 = st.columns(2)
        with col1:
            st.button("🔄 Swap Boxes", on_click=lambda: [st.session_state.update({'swapped': True}), go_to_step(3)])
        with col2:
            st.button("✅ Keep Boxes", on_click=lambda: go_to_step(3))

    # --- Step 3: Reveal and Score ---
    elif st.session_state.step == 3:
        st.subheader("🎉 Reveal Time!")
        carrot_in_red = st.session_state.carrot_in_red
        swapped = st.session_state.swapped

        # Adjust for swap
        if swapped:
            carrot_in_red = not carrot_in_red

        if carrot_in_red:
            winner = st.session_state.p1_name
            st.success(f"🥕 The carrot was in the **Red Box!** {winner} wins this round! 🎉")
            st.session_state.p1_score += 1
        else:
            winner = st.session_state.p2_name
            st.success(f"🥕 The carrot was in the **Gold Box!** {winner} wins this round! 🎉")
            st.session_state.p2_score += 1

        st.balloons()
        st.divider()

        c1, c2 = st.columns(2)
        c1.button("🔁 New Round", on_click=reset_round)
        c2.button("🧹 Reset All", on_click=reset_all)

    # --- Footer ---
    st.divider()
