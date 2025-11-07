import streamlit as st
import time
import sevseg
import pandas as pd

# ----------------------------------------
# CONSTANTS
# ----------------------------------------
WORK_TIME = 25 * 60     # 25 min
BREAK_TIME = 5 * 60     # 5 min


# ----------------------------------------
# COLORED PROGRESS BAR FUNCTION
# ----------------------------------------
def colored_progress(pct, color):
    filled = int(pct * 100)
    return f"""
    <div style="background:#ddd; width:100%; border-radius:8px; height:18px; margin-top:10px;">
        <div style="
            width:{filled}%;
            background:{color};
            height:18px;
            border-radius:8px;">
        </div>
    </div>
    """


# ----------------------------------------
# MAIN APP
# ----------------------------------------
def run():
    st.title("⏱ Seven-Segment Countdown Timer")
    st.markdown("""
## 📘 How to Use

**1. Choose Mode**
- **Normal Countdown:** Enter seconds (only timers **≥ 60s** are saved).
- **Pomodoro 25/5:** Auto cycles between **25-min work** and **5-min break**.

**2. Controls**
- ▶ Start ⏸ Pause ⏵ Resume 🔁 Reset

**3. Timer Display**
- Bar + digits change color: **Green → Orange → Red** as time runs out.

**4. Productivity Tracking**
- Tracks: **Work sessions, Break sessions, Total focus minutes.**
- History includes:
  - ✅ Work (Pomodoro)
  - ✅ Break (Pomodoro)
  - ✅ Countdown ≥ 60 seconds

That's it — stay focused!
""")


    # ----------------------------------------
    # STATE INIT
    # ----------------------------------------
    if "running" not in st.session_state:
        st.session_state.running = False

    if "paused" not in st.session_state:
        st.session_state.paused = False

    if "remaining" not in st.session_state:
        st.session_state.remaining = 0

    if "total_time" not in st.session_state:
        st.session_state.total_time = 0

    if "pomodoro_mode" not in st.session_state:
        st.session_state.pomodoro_mode = "work"

    if "stats" not in st.session_state:
        st.session_state.stats = {
            "work_sessions": 0,
            "break_sessions": 0,
            "total_focus_minutes": 0,
            "history": []
        }

    # ----------------------------------------
    # MODE SELECTION
    # ----------------------------------------
    mode = st.selectbox("Mode:", ["Normal Countdown", "Pomodoro 25/5"])

    if mode == "Normal Countdown":
        user_seconds = st.number_input("Seconds:", min_value=1, value=30)

    # ----------------------------------------
    # BUTTONS
    # ----------------------------------------
    colA, colB, colC, colD = st.columns(4)
    start = colA.button("▶ Start")
    pause = colB.button("⏸ Pause")
    resume = colC.button("⏵ Resume")
    reset = colD.button("🔁 Reset")

    # ----------------------------------------
    # BUTTON LOGIC
    # ----------------------------------------
    if start:
        st.session_state.paused = False
        st.session_state.running = True

        if mode == "Normal Countdown":
            st.session_state.remaining = int(user_seconds)
            st.session_state.total_time = int(user_seconds)
        else:
            if st.session_state.pomodoro_mode == "work":
                st.session_state.remaining = WORK_TIME
                st.session_state.total_time = WORK_TIME
            else:
                st.session_state.remaining = BREAK_TIME
                st.session_state.total_time = BREAK_TIME

    if pause:
        st.session_state.paused = True

    if resume:
        st.session_state.paused = False
        st.session_state.running = True

    if reset:
        st.session_state.running = False
        st.session_state.paused = False
        st.session_state.remaining = 0
        st.session_state.total_time = 0

    # ----------------------------------------
    # ACTIVE TIMER LOOP
    # ----------------------------------------
    if st.session_state.running and not st.session_state.paused:
        remaining = st.session_state.remaining
        total = st.session_state.total_time

        # ----------- COLOR LOGIC -----------
        pct = remaining / total if total else 1

        if pct > 0.5:
            color = "green"
        elif pct > 0.25:
            color = "orange"
        else:
            color = "red"

        # ----------- COLORED PROGRESS BAR -----------
        st.markdown(colored_progress(1 - pct, color), unsafe_allow_html=True)

        # ----------- TIME FORMAT -----------
        hours = str(remaining // 3600)
        minutes = str((remaining % 3600) // 60)
        seconds_s = str(remaining % 60)

        hT, hM, hB = sevseg.getSevSegStr(hours, 2).splitlines()
        mT, mM, mB = sevseg.getSevSegStr(minutes, 2).splitlines()
        sT, sM, sB = sevseg.getSevSegStr(seconds_s, 2).splitlines()

        st.markdown(f"<span style='color:{color}; font-weight:bold;'>", unsafe_allow_html=True)
        st.code(
f"""{hT}   {mT}   {sT}
{hM} * {mM} * {sM}
{hB} * {mB} * {sB}"""
        )
        st.markdown("</span>", unsafe_allow_html=True)

        # ----------- END OF TIMER -----------
        if remaining == 0:

            if mode == "Normal Countdown":
                st.success("💥 BOOM! Time's up!")
                st.session_state.running = False

                if st.session_state.total_time >= 60:
                    st.session_state.stats["history"].append({
                        "type": "countdown",
                        "minutes": st.session_state.total_time // 60,
                        "seconds": st.session_state.total_time,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })


            else:
                # Pomodoro logic
                if st.session_state.pomodoro_mode == "work":
                    st.session_state.stats["work_sessions"] += 1
                    st.session_state.stats["total_focus_minutes"] += WORK_TIME // 60
                    st.session_state.stats["history"].append({
                        "type": "work",
                        "minutes": WORK_TIME // 60,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })

                    st.success("✅ Work session done! Break time!")
                    st.session_state.pomodoro_mode = "break"
                    st.session_state.remaining = BREAK_TIME
                    st.session_state.total_time = BREAK_TIME

                else:
                    st.session_state.stats["break_sessions"] += 1
                    st.session_state.stats["history"].append({
                        "type": "break",
                        "minutes": BREAK_TIME // 60,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })

                    st.success("✅ Break over! Back to work!")
                    st.session_state.pomodoro_mode = "work"
                    st.session_state.remaining = WORK_TIME
                    st.session_state.total_time = WORK_TIME

            time.sleep(1)
            st.rerun()

        else:
            time.sleep(1)
            st.session_state.remaining -= 1
            st.rerun()

    # ----------------------------------------
    # PRODUCTIVITY DASHBOARD
    # ----------------------------------------
    st.header("📊 Productivity Dashboard")
    stats = st.session_state.stats

    c1, c2, c3 = st.columns(3)
    c1.metric("✅ Work Sessions", stats["work_sessions"])
    c2.metric("🧘 Break Sessions", stats["break_sessions"])
    c3.metric("⏳ Focus Minutes", stats["total_focus_minutes"])

    if stats["history"]:
        st.subheader("History")
        st.table(pd.DataFrame(stats["history"]))
    else:
        st.info("No productivity data yet.")


# ----------------------------------------
# RUN APP
# ----------------------------------------
if __name__ == "__main__":
    run()
