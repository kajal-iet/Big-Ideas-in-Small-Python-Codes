import streamlit as st
import time, random


# ------------------------------------------------------
# Session State Initialization
# ------------------------------------------------------
def init_stats():
    defaults = {
        "attempts": 0,
        "wins": 0,
        "losses": 0,
        "times": [],
        "draw_time": None,
        "waiting": False,
        "phase": "idle",  # idle → waiting → draw
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ------------------------------------------------------
# MAIN GAME FUNCTION
# ------------------------------------------------------
def run():
    st.set_page_config(page_title="Fast Draw", layout="centered")
    init_stats()

    st.title("🤠 Fast Draw — Reflex Tester")

    st.write("""
    Your goal: **Click as soon as DRAW appears.**  
    Clicking early = Lose instantly.

    ### 🎮 Difficulty Levels
    - Easy → 0.5 seconds  
    - Normal → 0.3 seconds  
    - Hard → 0.2 seconds  
    - Insane → 0.1 seconds  
    """)

    mode = st.selectbox(
        "Select Difficulty:",
        ["Easy (0.5s)", "Normal (0.3s)", "Hard (0.2s)", "Insane (0.1s)"]
    )

    allowed = {
        "Easy": 0.5,
        "Normal": 0.3,
        "Hard": 0.2,
        "Insane": 0.1
    }[mode.split()[0]]

    # ------------------------------------------------------
    # START ROUND
    # ------------------------------------------------------
    if st.button("Start Round"):
        st.session_state.phase = "waiting"
        st.session_state.draw_time = None
        st.rerun()

    # ------------------------------------------------------
    # WAITING PHASE
    # ------------------------------------------------------
    if st.session_state.phase == "waiting" and st.session_state.draw_time is None:
        st.subheader("⏳ It is high noon... get ready.")
        wait = random.uniform(2, 4)
        time.sleep(wait)

        # Transition to DRAW phase
        st.session_state.draw_time = time.time()
        st.session_state.phase = "draw"
        st.rerun()

    # ------------------------------------------------------
    # DRAW PHASE
    # ------------------------------------------------------
    if st.session_state.phase == "draw":
        st.markdown("## 🎯 **DRAW!**")

    # ------------------------------------------------------
    # CLICK NOW BUTTON (ALWAYS SHOW)
    # ------------------------------------------------------
    clicked = st.button(
        "CLICK NOW!",
        disabled=(st.session_state.phase != "draw"),  # Only active when draw phase
        use_container_width=True
    )

    if clicked and st.session_state.phase == "draw":
        reaction = time.time() - st.session_state.draw_time
        st.session_state.attempts += 1

        if reaction <= allowed:
            st.success(f"🔥 FAST! Reaction time: **{round(reaction,4)}s**")
            st.session_state.wins += 1
            st.session_state.times.append(reaction)
        else:
            st.error(f"Too slow! ({round(reaction,4)}s)")
            st.session_state.losses += 1
            st.session_state.times.append(reaction)

        st.session_state.phase = "idle"
        st.session_state.draw_time = None

    # ------------------------------------------------------
    # DASHBOARD (Beautiful UI)
    # ------------------------------------------------------
    st.write("---")
    st.header("📊 Performance Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Attempts", st.session_state.attempts)
    col2.metric("Wins", st.session_state.wins)
    col3.metric("Losses", st.session_state.losses)

    if st.session_state.times:
        best = min(st.session_state.times)
        worst = max(st.session_state.times)
        avg = sum(st.session_state.times) / len(st.session_state.times)

        st.write("### Reaction Summary")
        c1, c2, c3 = st.columns(3)
        c1.info(f"**Best:** {round(best,4)}s")
        c2.warning(f"**Average:** {round(avg,4)}s")
        c3.error(f"**Worst:** {round(worst,4)}s")

        st.write("### Reaction Timeline")
        st.bar_chart(st.session_state.times)

    if st.button("Reset Stats"):
        for k in ["attempts","wins","losses","times","draw_time","waiting","phase"]:
            st.session_state[k] = 0 if k in ["attempts","wins","losses"] else []
        st.success("✅ Stats Cleared!")
        st.rerun()
