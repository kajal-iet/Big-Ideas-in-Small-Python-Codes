import streamlit as st
import random
import time

# -------------------------
# ASCII DICE DATA
# -------------------------
def run():
    D1 = (['+-------+',
           '|       |',
           '|   O   |',
           '|       |',
           '+-------+'], 1)

    D2a = (['+-------+',
            '| O     |',
            '|       |',
            '|     O |',
            '+-------+'], 2)

    D2b = (['+-------+',
            '|     O |',
            '|       |',
            '| O     |',
            '+-------+'], 2)

    D3a = (['+-------+',
            '| O     |',
            '|   O   |',
            '|     O |',
            '+-------+'], 3)

    D3b = (['+-------+',
            '|     O |',
            '|   O   |',
            '| O     |',
            '+-------+'], 3)

    D4 = (['+-------+',
           '| O   O |',
           '|       |',
           '| O   O |',
           '+-------+'], 4)

    D5 = (['+-------+',
           '| O   O |',
           '|   O   |',
           '| O   O |',
           '+-------+'], 5)

    D6a = (['+-------+',
            '| O   O |',
            '| O   O |',
            '| O   O |',
            '+-------+'], 6)

    D6b = (['+-------+',
            '| O O O |',
            '|       |',
            '| O O O |',
            '+-------+'], 6)

    ALL_DICE = [D1, D2a, D2b, D3a, D3b, D4, D5, D6a, D6b]

    # -------------------------
    # INITIAL SESSION STATE
    # -------------------------
    defaults = {
        "game_started": False,
        "difficulty": None,
        "end_time": None,
        "score": 0,
        "sum_answer": 0,
        "canvas_str": "",
        "question_ready": False,
        "MIN_DICE": 2,
        "MAX_DICE": 6,
        "QUIZ_DURATION": 30,
        "REWARD": 4,
        "PENALTY": 1
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # -------------------------
    # UI
    # -------------------------
    st.title("🎲 Dice Math – Streamlit Edition")

    # Choose difficulty before starting
    if not st.session_state.game_started:

    # Show difficulty selection ONLY once
        if st.session_state.difficulty is None:

            st.subheader("Select Difficulty")
            difficulty = st.radio(
                "Difficulty Level",
                ["Easy", "Medium", "Hard"],
                key="difficulty_radio"
            )

            # Apply difficulty based on selection
            if difficulty == "Easy":
                st.session_state.MIN_DICE = 1
                st.session_state.MAX_DICE = 3
                st.session_state.QUIZ_DURATION = 40
                st.session_state.REWARD = 3
                st.session_state.PENALTY = 1

            elif difficulty == "Medium":
                st.session_state.MIN_DICE = 2
                st.session_state.MAX_DICE = 6
                st.session_state.QUIZ_DURATION = 30
                st.session_state.REWARD = 4
                st.session_state.PENALTY = 2

            elif difficulty == "Hard":
                st.session_state.MIN_DICE = 4
                st.session_state.MAX_DICE = 8
                st.session_state.QUIZ_DURATION = 20
                st.session_state.REWARD = 6
                st.session_state.PENALTY = 3

            if st.button("Start Quiz"):
                st.session_state.difficulty = difficulty  # ✅ lock difficulty
                st.session_state.game_started = True
                st.session_state.end_time = time.time() + st.session_state.QUIZ_DURATION
                st.session_state.question_ready = False
                st.session_state.score = 0
                st.rerun()

            st.stop()

        else:
            # ✅ Difficulty already chosen, no need to click twice
            st.session_state.game_started = True
            st.rerun()

    # -------------------------
    # TIMER + PROGRESS BAR
    # -------------------------
    time_left = int(st.session_state.end_time - time.time())
    time_left = max(time_left, 0)

    st.write(f"⏳ Time Left: **{time_left} sec**")

    # Progress bar (1.0 → full, 0.0 → empty)
    progress = time_left / st.session_state.QUIZ_DURATION
    st.progress(progress)

    if time_left <= 0:
        st.session_state.game_started = False
        st.error("⏱️ Time’s up!")
        st.success(f"✅ Final Score: {st.session_state.score}")
        st.stop()

    # -------------------------
    # GENERATE QUESTION
    # -------------------------
    def generate_question():
        canvas = [[" " for _ in range(60)] for _ in range(15)]
        used_positions = []
        sum_total = 0

        dice_count = random.randint(st.session_state.MIN_DICE, st.session_state.MAX_DICE)

        for _ in range(dice_count):
            die = random.choice(ALL_DICE)
            face, value = die
            sum_total += value

            while True:
                x = random.randint(0, 60 - 9)
                y = random.randint(0, 15 - 5)

                overlaps = any(px <= x < px + 9 and py <= y < py + 5 for px, py in used_positions)

                if not overlaps:
                    used_positions.append((x, y))
                    break

            for dy in range(5):
                for dx in range(9):
                    canvas[y + dy][x + dx] = face[dy][dx]

        return "\n".join("".join(row) for row in canvas), sum_total

    # New question
    if not st.session_state.question_ready:
        canvas_str, ans = generate_question()
        st.session_state.canvas_str = canvas_str
        st.session_state.sum_answer = ans
        st.session_state.question_ready = True

    # Show dice
    st.text(st.session_state.canvas_str)

    # Answer input
    user_answer = st.number_input("Enter total sum:", step=1, key="user_input")

    if st.button("Submit Answer", key="submit_button"):
        if user_answer == st.session_state.sum_answer:
            st.session_state.score += st.session_state.REWARD
            st.success("✅ Correct!")
        else:
            st.session_state.score -= st.session_state.PENALTY
            st.error(f"❌ Wrong! Correct answer: {st.session_state.sum_answer}")

        st.session_state.question_ready = False
        st.rerun()

    st.write(f"📊 **Score:** {st.session_state.score}")

    # Auto-refresh timer every second
    time.sleep(1)
    st.rerun()
