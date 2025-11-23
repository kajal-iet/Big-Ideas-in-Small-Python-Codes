# flooder_streamlit.py
"""
Flooder - Streamlit Edition (Fixed Button Rendering)

Changes in this version:
 - Buttons now show readable color names (not raw HTML)
 - Colored tiles are displayed separately below buttons
 - Rules are clarified at top of UI
"""

import streamlit as st
import random
import copy

# --- Configurable constants ---
BOARD_WIDTH = 12
BOARD_HEIGHT = 10
MOVES_PER_GAME = 20

TILE_TYPES = (0, 1, 2, 3, 4, 5)
COLORS_MAP = {0: 'red', 1: 'green', 2: 'blue', 3: 'yellow', 4: 'cyan', 5: 'purple'}
COLOR_NAMES = {0: 'Red', 1: 'Green', 2: 'Blue', 3: 'Yellow', 4: 'Cyan', 5: 'Purple'}
SHAPES_MAP = {0: '♥', 1: '▲', 2: '♦', 3: '•', 4: '♣', 5: '♠'}

# CSS for tile display
TILE_CSS = """
<style>
.tile {
  display:inline-block;
  width: 34px;
  height: 34px;
  line-height:34px;
  text-align:center;
  border-radius:4px;
  margin: 2px;
  font-weight: 700;
  font-size: 18px;
  user-select: none;
}
.row {
  margin-bottom: 2px;
}
.controls {
  margin-top: 10px;
}
.small {
  font-size:12px; color: #888;
}
</style>
"""

# -------------------------
# Utility and game logic
# -------------------------
def get_new_board(width=BOARD_WIDTH, height=BOARD_HEIGHT):
    board = {}
    for x in range(width):
        for y in range(height):
            board[(x, y)] = random.choice(TILE_TYPES)
    for i in range(width * height):
        x = random.randint(0, width - 2)
        y = random.randint(0, height - 1)
        board[(x + 1, y)] = board[(x, y)]
    return board

def flood_fill(board, x, y, new_tile, width=BOARD_WIDTH, height=BOARD_HEIGHT):
    old = board[(x, y)]
    if new_tile == old:
        return
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
        if cx > 0:
            stack.append((cx - 1, cy))
        if cy > 0:
            stack.append((cx, cy - 1))
        if cx < width - 1:
            stack.append((cx + 1, cy))
        if cy < height - 1:
            stack.append((cx, cy + 1))

def has_won(board):
    tile = board[(0, 0)]
    return all(board[(x, y)] == tile for x in range(BOARD_WIDTH) for y in range(BOARD_HEIGHT))

def simulate_one_move_gain(board, tile_choice):
    board_copy = copy.deepcopy(board)
    flood_fill(board_copy, 0, 0, tile_choice)
    target = board_copy[(0,0)]
    return sum(1 for x in range(BOARD_WIDTH) for y in range(BOARD_HEIGHT) if board_copy[(x,y)] == target)

# -------------------------
# Session State Handling
# -------------------------
def init_session_state():
    if 'board' not in st.session_state:
        st.session_state.board = get_new_board()
        st.session_state.moves_left = MOVES_PER_GAME
        st.session_state.display_mode = 'color'
        st.session_state.history = []
        st.session_state.message = ''
        st.session_state.hint = None

def push_history():
    state_copy = copy.deepcopy(st.session_state.board)
    st.session_state.history.append((state_copy, st.session_state.moves_left))
    if len(st.session_state.history) > 50:
        st.session_state.history.pop(0)

def undo_last():
    if st.session_state.history:
        board_prev, moves_prev = st.session_state.history.pop()
        st.session_state.board = board_prev
        st.session_state.moves_left = moves_prev
        st.session_state.message = 'Undid last move.'
    else:
        st.session_state.message = 'No moves to undo.'

def pick_color(tile_idx):
    if st.session_state.moves_left <= 0:
        st.session_state.message = 'No moves left!'
        return
    push_history()
    flood_fill(st.session_state.board, 0, 0, tile_idx)
    st.session_state.moves_left -= 1
    st.session_state.hint = None
    if has_won(st.session_state.board):
        st.session_state.message = 'You have won! 🎉'
    elif st.session_state.moves_left == 0:
        st.session_state.message = 'Out of moves — game over.'
    else:
        st.session_state.message = f'Picked {COLOR_NAMES[tile_idx]}. Moves left: {st.session_state.moves_left}'

def compute_hint():
    current = st.session_state.board[(0,0)]
    best = None
    best_count = -1
    for t in TILE_TYPES:
        if t == current:
            continue
        gain = simulate_one_move_gain(st.session_state.board, t)
        if gain > best_count:
            best = t
            best_count = gain
    st.session_state.hint = best
    st.session_state.message = f'Suggested next: {COLOR_NAMES[best]}'

def reset_game():
    st.session_state.board = get_new_board()
    st.session_state.moves_left = MOVES_PER_GAME
    st.session_state.history = []
    st.session_state.message = 'New game started!'
    st.session_state.hint = None

# -------------------------
# Rendering
# -------------------------
def render_board_html():
    html_parts = [TILE_CSS, '<div>']
    for y in range(BOARD_HEIGHT):
        html_parts.append('<div class="row">')
        for x in range(BOARD_WIDTH):
            t = st.session_state.board[(x, y)]
            color = COLORS_MAP[t]
            html_parts.append(
                f'<div class="tile" style="background:{color}"></div>'
            )
        html_parts.append('</div>')
    html_parts.append('</div>')
    return ''.join(html_parts)

# -------------------------
# MAIN UI
# -------------------------
def main():
    st.set_page_config(page_title="Flooder", layout="centered")
    init_session_state()

    st.markdown("### 🎮 How to Play")
    st.markdown("""
    - You start at **top-left** tile  
    - DOuble Click a color to **expand your connected region**
    - Goal -> **Make entire board one color**
    - You have **limited moves**
    - Flooding spreads only to **adjacent (↑↓←→)** cells
    """)

    with st.sidebar:
        st.header("Game Controls")
        st.write("Moves left:", st.session_state.moves_left)
        if st.button("📌 New Game"):
            reset_game()
        if st.button("↩ Undo"):
            undo_last()
        if st.button("💡 Hint"):
            compute_hint()
        st.write("")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(render_board_html(), unsafe_allow_html=True)

    with col2:
        st.subheader("Pick a Color")

        for t in TILE_TYPES:
            label = COLOR_NAMES[t]
            if st.button(label, key=f"btn_{t}"):
                pick_color(t)

            # Show visual color block below button
            st.markdown(
                f"<div style='background:{COLORS_MAP[t]}; width:60px; height:20px; border-radius:4px; margin-bottom:8px;'></div>",
                unsafe_allow_html=True
            )

        st.write(f"**Message:** {st.session_state.message}")

    st.markdown("---")
    if has_won(st.session_state.board):
        st.success("You won! 🎉")
    elif st.session_state.moves_left <= 0:
        st.error("No moves left. Try again!")

def run():
    main()


if __name__ == "__main__":
    run()
