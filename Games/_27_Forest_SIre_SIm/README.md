# forest_fire_sim.py
"""
Forest Fire Simulator – Streamlit Edition
(A + C Hybrid Model)
- Simple spread rules
- Advanced wind direction influence
- Firebreak wall tiles
- Flooder-style layout + CSS tile rendering
"""

import streamlit as st
import random
import copy

# ----------------------------
# Constants
# ----------------------------
WIDTH = 16
HEIGHT = 12

TREE = 0
FIRE = 1
ASH = 2
EMPTY = 3
WALL = 4

TILE_NAMES = {
    TREE: "Tree",
    FIRE: "Fire",
    ASH: "Ash",
    EMPTY: "Empty",
    WALL: "Wall"
}

TILE_COLORS = {
    TREE: "green",
    FIRE: "red",
    ASH: "gray",
    EMPTY: "white",
    WALL: "black"
}

# Wind vectors
WIND_DIRECTIONS = {
    "None": (0, 0),
    "North ↑": (0, -1),
    "South ↓": (0, 1),
    "West ←": (-1, 0),
    "East →": (1, 0)
}

# ----------------------------
# Tile CSS
# ----------------------------
CSS = """
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
.row { margin-bottom: 2px; }
</style>
"""

# ----------------------------
# Utilities
# ----------------------------
def init_board():
    board = {}
    for x in range(WIDTH):
        for y in range(HEIGHT):
            board[(x, y)] = TREE if random.random() < 0.85 else EMPTY
    return board

def in_bounds(x, y):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT

def ignite(x, y):
    if st.session_state.board[(x, y)] == TREE:
        st.session_state.board[(x, y)] = FIRE

def toggle_wall(x, y):
    cur = st.session_state.board[(x, y)]
    if cur == WALL:
        st.session_state.board[(x, y)] = TREE
    elif cur == TREE:
        st.session_state.board[(x, y)] = WALL

# ----------------------------
# Simulation Step
# ----------------------------
def step_simulation():
    old_board = copy.deepcopy(st.session_state.board)
    wind_dx, wind_dy = WIND_DIRECTIONS[st.session_state.wind]

    for x in range(WIDTH):
        for y in range(HEIGHT):
            cur = old_board[(x, y)]

            if cur == FIRE:
                st.session_state.board[(x, y)] = ASH

            elif cur == TREE:
                neighbors = [
                    (x-1, y), (x+1, y),
                    (x, y-1), (x, y+1)
                ]

                fire_near = any(
                    in_bounds(nx, ny) and old_board[(nx, ny)] == FIRE
                    for nx, ny in neighbors
                )

                if fire_near:
                    # Wind boosted chance
                    wind_boost = 0
                    wx = x + wind_dx
                    wy = y + wind_dy
                    if in_bounds(wx, wy) and old_board.get((wx, wy)) == FIRE:
                        wind_boost = 1  # Guaranteed burn if wind pushes it

                    if wind_boost == 1 or random.random() < 0.45:
                        st.session_state.board[(x, y)] = FIRE

# ----------------------------
# Render Board
# ----------------------------
def render_board_html():
    html = [CSS, "<div>"]

    for y in range(HEIGHT):
        html.append('<div class="row">')
        for x in range(WIDTH):
            tile = st.session_state.board[(x, y)]
            color = TILE_COLORS[tile]
            html.append(
                f'<div class="tile" style="background:{color}"></div>'
            )
        html.append('</div>')
    html.append("</div>")
    return "".join(html)

# ----------------------------
# MAIN UI
# ----------------------------
def main():
    st.set_page_config(page_title="Forest Fire Simulator")

    if "board" not in st.session_state:
        st.session_state.board = init_board()
        st.session_state.wind = "None"
        st.session_state.mode = "ignite"

    st.markdown("## 🌲🔥 Forest Fire Simulator")
    st.markdown("""
- Click tiles to **Ignite Fire** or place **Walls**  
- Fire spreads to adjacent cells  
- Wind pushes fire more strongly  
- Burning cells → Ash next turn  
    """)

    with st.sidebar:
        st.header("Controls")
        if st.button("New Forest"):
            st.session_state.board = init_board()

        st.selectbox(
            "Interaction Mode",
            ["ignite", "wall"],
            key="mode"
        )

        st.selectbox(
            "Wind Direction",
            list(WIND_DIRECTIONS.keys()),
            key="wind"
        )

        if st.button("Step Simulation"):
            step_simulation()

    # Render + Clickable Grid
    for y in range(HEIGHT):
        cols = st.columns(WIDTH)
        for x in range(WIDTH):
            tile = TILE_NAMES[st.session_state.board[(x, y)]]
            btn = cols[x].button(" ", key=f"{x}_{y}")

            if btn:
                if st.session_state.mode == "ignite":
                    ignite(x, y)
                else:
                    toggle_wall(x, y)

            cols[x].markdown(
                f"<div class='tile' style='background:{TILE_COLORS[st.session_state.board[(x, y)]]}'></div>",
                unsafe_allow_html=True
            )

def run():
    main()

if __name__ == "__main__":
    run()
