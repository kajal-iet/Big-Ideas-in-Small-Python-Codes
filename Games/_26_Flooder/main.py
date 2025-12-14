# flooder_streamlit.py
import streamlit as st
import random
import copy

# ------------------ CONFIG ------------------
BOARD_WIDTH = 12
BOARD_HEIGHT = 10
MOVES_PER_GAME = 20

TILE_TYPES = (0, 1, 2, 3, 4, 5)
COLORS_MAP = {0: 'red', 1: 'green', 2: 'blue', 3: 'yellow', 4: 'cyan', 5: 'purple'}
COLOR_NAMES = {0: 'Red', 1: 'Green', 2: 'Blue', 3: 'Yellow', 4: 'Cyan', 5: 'Purple'}

TILE_CSS = """
<style>
.tile {
  display:inline-block;
  width:34px;
  height:34px;
  border-radius:4px;
  margin:2px;
}
.row { margin-bottom:2px; }
</style>
"""

# ------------------ GAME LOGIC ------------------
def get_new_board():
    board = {}
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            board[(x, y)] = random.choice(TILE_TYPES)

    # create clusters
    for _ in range(BOARD_WIDTH * BOARD_HEIGHT):
        x = random.randint(0, BOARD_WIDTH - 2)
        y = random.randint(0, BOARD_HEIGHT - 1)
        board[(x + 1, y)] = board[(x, y)]
    return board


def flood_fill(board, x, y, new_tile):
    old = board[(x, y)]
    if new_tile == old:
        return False  # ❗ no actual change

    stack = [(x, y)]
    visited = set()

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))

        if board[(cx, cy)] != old:
            continue

        board[(cx, cy)] = new_tile

        if cx > 0: stack.append((cx - 1, cy))
        if cy > 0: stack.append((cx, cy - 1))
        if cx < BOARD_WIDTH - 1: stack.append((cx + 1, cy))
        if cy < BOARD_HEIGHT - 1: stack.append((cx, cy + 1))

    return True  # ✅ board changed


def has_won(board):
    target = board[(0, 0)]
    return all(board[(x, y)] == target for x in range(BOARD_WIDTH) for y in range(BOARD_HEIGHT))


def simulate_gain(board, tile_choice):
    copy_board = copy.deepcopy(board)
    flood_fill(copy_board, 0, 0, tile_choice)
    t = copy_board[(0, 0)]
    return sum(1 for x in range(BOARD_WIDTH) for y in range(BOARD_HEIGHT) if copy_board[(x, y)] == t)

# ------------------ SESSION STATE ------------------
def init_state():
    if "board" not in st.session_state:
        st.session_state.board = get_new_board()
        st.session_state.moves_left = MOVES_PER_GAME
        st.session_state.history = []
        st.session_state.message = ""
        st.session_state.hint = None


def push_history():
    st.session_state.history.append(
        (copy.deepcopy(st.session_state.board), st.session_state.moves_left)
    )


def undo():
    if st.session_state.history:
        board, moves = st.session_state.history.pop()
        st.session_state.board = board
        st.session_state.moves_left = moves
        st.session_state.message = "Undid last move."


def pick_color(tile_idx):
    if st.session_state.moves_left <= 0:
        return

    current = st.session_state.board[(0, 0)]
    if tile_idx == current:
        st.session_state.message = "Already that color."
        return

    push_history()

    changed = flood_fill(st.session_state.board, 0, 0, tile_idx)
    if not changed:
        return

    st.session_state.moves_left -= 1
    st.session_state.hint = None

    if has_won(st.session_state.board):
        st.session_state.message = "You won! 🎉"
    elif st.session_state.moves_left == 0:
        st.session_state.message = "Out of moves — game over."
    else:
        st.session_state.message = f"Picked {COLOR_NAMES[tile_idx]}. Moves left: {st.session_state.moves_left}"


def compute_hint():
    current = st.session_state.board[(0, 0)]
    best, best_score = None, -1
    for t in TILE_TYPES:
        if t == current:
            continue
        score = simulate_gain(st.session_state.board, t)
        if score > best_score:
            best, best_score = t, score
    st.session_state.hint = best
    st.session_state.message = f"Suggested next: {COLOR_NAMES[best]}"


def reset_game():
    st.session_state.board = get_new_board()
    st.session_state.moves_left = MOVES_PER_GAME
    st.session_state.history = []
    st.session_state.message = "New game started!"
    st.session_state.hint = None

# ------------------ RENDER ------------------
def render_board():
    html = [TILE_CSS, "<div>"]
    for y in range(BOARD_HEIGHT):
        html.append("<div class='row'>")
        for x in range(BOARD_WIDTH):
            t = st.session_state.board[(x, y)]
            html.append(f"<div class='tile' style='background:{COLORS_MAP[t]}'></div>")
        html.append("</div>")
    html.append("</div>")
    return "".join(html)

# ------------------ UI ------------------
def run():
    st.set_page_config(page_title="Flooder", layout="centered")
    init_state()

    st.markdown("### 🎮 Flooder — How to Play")
    st.markdown("""
- Start from the **top-left tile**
- Pick a color to **flood your connected region**
- Flooding spreads **↑ ↓ ← → only**
- Each valid color change uses **1 move**
- Make the **entire board one color** to win
    """)

    with st.sidebar:
        st.write("Moves left:", st.session_state.moves_left)
        if st.button("📌 New Game"):
            reset_game()
            st.rerun()
        if st.button("↩ Undo"):
            undo()
            st.rerun()
        if st.button("💡 Hint"):
            compute_hint()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(render_board(), unsafe_allow_html=True)

    with col2:
        st.subheader("Pick a Color")
        for t in TILE_TYPES:
            if st.button(COLOR_NAMES[t], key=f"color_{t}"):
                pick_color(t)
                st.rerun()

            st.markdown(
                f"<div style='background:{COLORS_MAP[t]}; width:60px; height:18px; border-radius:4px; margin-bottom:8px;'></div>",
                unsafe_allow_html=True
            )

        st.write(f"**Message:** {st.session_state.message}")

    if has_won(st.session_state.board):
        st.success("🎉 You won!")
    elif st.session_state.moves_left <= 0:
        st.error("No moves left. Try again!")

if __name__ == "__main__":
    run()
