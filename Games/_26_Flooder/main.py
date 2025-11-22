import streamlit as st
import random

# -------------------------------------------------------
# ------------------ GAME CONSTANTS ---------------------
# -------------------------------------------------------

DIFFICULTY_SETTINGS = {
    "Easy": {"width": 10, "height": 8, "moves": 25},
    "Medium": {"width": 16, "height": 14, "moves": 20},
    "Hard": {"width": 22, "height": 18, "moves": 15},
}

TILE_TYPES = (0, 1, 2, 3, 4, 5)

COLORS_MAP = {
    0: "#FF4C4C",   # red
    1: "#3CC25B",   # green
    2: "#3E75FF",   # blue
    3: "#FFD93D",   # yellow
    4: "#3CFFFF",   # cyan
    5: "#B056FF",   # purple
}

SHAPES_MAP = {
    0: "♥",
    1: "▲",
    2: "♦",
    3: "•",
    4: "♣",
    5: "♠"
}

COLOR_MODE = "color"
SHAPE_MODE = "shape"


# -------------------------------------------------------
# ------------------ GAME FUNCTIONS ---------------------
# -------------------------------------------------------

def generate_board():
    """Create a clustered random board."""
    board = {}
    for x in range(st.session_state.width):
        for y in range(st.session_state.height):
            board[(x, y)] = random.choice(TILE_TYPES)

    # Create clusters for playability
    for _ in range(st.session_state.width * st.session_state.height):
        x = random.randint(0, st.session_state.width - 2)
        y = random.randint(0, st.session_state.height - 1)
        board[(x + 1, y)] = board[(x, y)]
    return board


def change_tile(board, x, y, tile_type, char_to_change=None):
    """Recursive flood fill."""
    if x == 0 and y == 0:
        char_to_change = board[(x, y)]
        if tile_type == char_to_change:
            return

    board[(x, y)] = tile_type

    if x > 0 and board[(x - 1, y)] == char_to_change:
        change_tile(board, x - 1, y, tile_type, char_to_change)
    if y > 0 and board[(x, y - 1)] == char_to_change:
        change_tile(board, x, y - 1, tile_type, char_to_change)
    if x < st.session_state.width - 1 and board[(x + 1, y)] == char_to_change:
        change_tile(board, x, y, tile_type, char_to_change)
    if y < st.session_state.height - 1 and board[(x, y + 1)] == char_to_change:
        change_tile(board, x, y + 1, tile_type, char_to_change)


def has_won(board):
    tile = board[(0, 0)]
    return all(board[(x, y)] == tile
               for x in range(st.session_state.width)
               for y in range(st.session_state.height))


# -------------------------------------------------------
# ------------------ STREAMLIT APP ----------------------
# -------------------------------------------------------

def new_game():
    st.session_state.board = generate_board()
    st.session_state.moves_left = st.session_state.total_moves
    st.session_state.current_moves_used = 0


def run():
    st.set_page_config(page_title="Flooder Game", layout="centered")
    st.title("🎨 Flooder Game")

    # ---------------- Difficulty Settings ----------------
    st.sidebar.header("Game Settings")

    difficulty = st.sidebar.selectbox("Select Difficulty:", list(DIFFICULTY_SETTINGS.keys()))

    if "difficulty" not in st.session_state or st.session_state.difficulty != difficulty:
        st.session_state.width = DIFFICULTY_SETTINGS[difficulty]["width"]
        st.session_state.height = DIFFICULTY_SETTINGS[difficulty]["height"]
        st.session_state.total_moves = DIFFICULTY_SETTINGS[difficulty]["moves"]
        st.session_state.difficulty = difficulty
        new_game()

    # ---------------- Mode Selection ----------------
    mode = st.sidebar.radio("Display Mode:", ["Color Mode", "Colorblind Shape Mode"])
    st.session_state.mode = SHAPE_MODE if mode.startswith("Colorblind") else COLOR_MODE

    # ---------------- Rules ----------------
    with st.expander("📌 How to Play"):
        st.markdown("""
        **Goal:** Fill the entire board with one color/shape before you run out of moves.
        - Click a color button to change the top-left tile.
        - The change spreads to all connected tiles of the same original color.
        - Win when every tile matches!
        """)

    # ---------------- Score History Feature ----------------
    if "best_score" not in st.session_state:
        st.session_state.best_score = None

    # ---------------- Display Board ----------------
    board = st.session_state.board

    for y in range(st.session_state.height):
        cols = st.columns(st.session_state.width)
        for x in range(st.session_state.width):
            tile = board[(x, y)]

            if st.session_state.mode == COLOR_MODE:
                cols[x].button(
                    " ",
                    key=f"{x}-{y}",
                    disabled=True,
                    help=str(tile),
                    use_container_width=True,
                    style=f"background-color: {COLORS_MAP[tile]}; height:22px;"
                )
            else:
                cols[x].button(
                    SHAPES_MAP[tile],
                    key=f"{x}-{y}",
                    disabled=True,
                    use_container_width=True,
                    style=f"background-color:black; color:{COLORS_MAP[tile]}; font-size:18px; height:30px;"
                )

    # ---------------- Move Buttons ----------------
    st.write("### Select Move:")

    cols = st.columns(6)
    for i in range(len(COLORS_MAP)):
        label = SHAPES_MAP[i] if st.session_state.mode == SHAPE_MODE else " "
        if cols[i].button(label, key=f"move-{i}"):
            change_tile(board, 0, 0, i)
            st.session_state.moves_left -= 1
            st.session_state.current_moves_used += 1

    # ---------------- Display Stats ----------------
    st.write(f"### 🕹 Moves Left: **{st.session_state.moves_left}**")

    # Check Win/Lose
    if has_won(board):
        st.success("🎉 You Won!")
        if st.session_state.best_score is None or st.session_state.current_moves_used < st.session_state.best_score:
            st.session_state.best_score = st.session_state.current_moves_used
        st.write(f"🏆 **Best Score:** {st.session_state.best_score} moves")

    elif st.session_state.moves_left <= 0:
        st.error("❌ Out of Moves!")

    # Reset Button
    if st.button("🔄 Restart Game"):
        new_game()
        st.rerun()


if __name__ == "__main__":
    run()
