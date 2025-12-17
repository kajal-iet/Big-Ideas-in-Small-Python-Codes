import streamlit as st
import random
import time

# ================== CONFIG ==================
SUSPECTS = [
    "DUKE HAUTDOG", "MAXIMUM POWERS", "BILL MONOPOLIS",
    "SENATOR SCHMEAR", "MRS. FEATHERTOSS",
    "DR. JEAN SPLICER", "RAFFLES THE CLOWN",
    "ESPRESSA TOFFEEPOT", "CECIL EDGAR VANDERTON"
]

ITEMS = [
    "FLASHLIGHT", "CANDLESTICK", "RAINBOW FLAG",
    "HAMSTER WHEEL", "ANIME VHS TAPE",
    "JAR OF PICKLES", "ONE COWBOY BOOT",
    "CLEAN UNDERPANTS", "5 DOLLAR GIFT CARD"
]

PLACES = [
    "ZOO", "OLD BARN", "DUCK POND", "CITY HALL",
    "HIPSTER CAFE", "BOWLING ALLEY",
    "VIDEO GAME MUSEUM", "UNIVERSITY LIBRARY",
    "ALBINO ALLIGATOR PIT"
]

DIFFICULTY = {
    "Easy":   {"time": 420, "liars": 2},
    "Medium": {"time": 300, "liars": 3},
    "Hard":   {"time": 180, "liars": 4},
}

# ================== GAME INIT ==================
def init_game(level):
    suspects = SUSPECTS[:]
    items = ITEMS[:]
    places = PLACES[:]

    random.shuffle(suspects)
    random.shuffle(items)
    random.shuffle(places)

    culprit = random.choice(suspects)

    liars = random.sample(
        [s for s in suspects if s != culprit],
        DIFFICULTY[level]["liars"]
    )

    st.session_state.game = {
        "start_time": time.time(),
        "time_limit": DIFFICULTY[level]["time"],
        "culprit": culprit,
        "liars": liars,
        "suspects": suspects,
        "items": items,
        "places": places,
        "notes": [],
        "game_over": False,
        "result": None
    }

# ================== CLUE SYSTEM ==================
def get_clue(person):
    game = st.session_state.game
    truthful = person not in game["liars"]

    suspects = game["suspects"]
    items = game["items"]
    places = game["places"]

    culprit_index = suspects.index(game["culprit"])

    if truthful:
        return random.choice([
            f"Zophie was near the **{items[culprit_index]}**.",
            f"The culprit visited the **{places[culprit_index]}**.",
            f"The truth points to the **{places[culprit_index]}**."
        ])
    else:
        fake_indices = [i for i in range(len(suspects)) if i != culprit_index]
        fi = random.choice(fake_indices)
        return random.choice([
            f"Zophie was near the **{items[fi]}**.",
            f"The culprit visited the **{places[fi]}**.",
            f"The truth points to the **{places[fi]}**."
        ])

# ================== MAIN GAME ==================
def run():
    st.title("🕵️ J’ACCUSE!")
    st.caption("A logic & deduction mystery game")

    st.markdown("""
### 📜 Rules
- One suspect kidnapped **Zophie the Cat**
- Suspects **always lie OR always tell the truth**
- Gather clues and deduce who is lying
- Clicking **⚖️ J’ACCUSE!** ends the case instantly
- Choose wisely — one final verdict
""")

    # ---------- START ----------
    if "game" not in st.session_state:
        level = st.selectbox("Select Difficulty", DIFFICULTY.keys())
        if st.button("▶ Start Investigation"):
            init_game(level)
            st.rerun()
        return

    game = st.session_state.game

    # ---------- TIMER ----------
    elapsed = int(time.time() - game["start_time"])
    remaining = max(0, game["time_limit"] - elapsed)

    st.info(f"⏱ Time Left: {remaining // 60}m {remaining % 60}s")

    if remaining == 0 and not game["game_over"]:
        game["game_over"] = True
        game["result"] = f"⏰ Time’s up! Culprit was **{game['culprit']}**."

    # ---------- GAME OVER ----------
    if game["game_over"]:
        st.error(game["result"])
        if st.button("🔄 Play Again"):
            st.session_state.clear()
            st.rerun()
        return

    # ---------- INTERROGATION ----------
    suspect = st.selectbox("Choose a suspect", game["suspects"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("❓ Ask for Clue"):
            clue = get_clue(suspect)
            game["notes"].append(f"**{suspect}** says: {clue}")

    with col2:
        if st.button("⚖️ J’ACCUSE!"):
            game["game_over"] = True
            if suspect == game["culprit"]:
                game["result"] = f"🎉 Case Solved! **{suspect}** kidnapped Zophie!"
            else:
                game["result"] = f"❌ Wrong accusation. Culprit was **{game['culprit']}**."
            st.rerun()

    # ---------- NOTES ----------
    st.markdown("### 🗒 Investigation Notes")
    if game["notes"]:
        for n in game["notes"]:
            st.markdown(f"- {n}")
    else:
        st.markdown("_No clues collected yet._")
