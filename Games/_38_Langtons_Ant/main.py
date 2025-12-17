import streamlit as st
import random
import time

# ================== CONSTANTS ==================
NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

# ================== RULES ==================
RULES_TEXT = """
### 🐜 Langton’s Ant — Rules

- The board is a 2D grid of **white** and **black** cells
- Each ant follows these rules **every step**:

**If the ant is on a WHITE cell:**
1. Turn **right**
2. Flip the cell to **black**
3. Move forward one step

**If the ant is on a BLACK cell:**
1. Turn **left**
2. Flip the cell to **white**
3. Move forward one step

- The grid **wraps around** at edges
- Multiple ants can occupy the same cell
- Simple rules → **complex emergent behavior**
"""

# ================== INITIALIZATION ==================
def init_game(grid_size, num_ants):
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    ants = []

    for _ in range(num_ants):
        ants.append({
            "x": grid_size // 2,
            "y": grid_size // 2,
            "dir": random.choice(DIRECTIONS)
        })

    st.session_state.ant_game = {
        "grid": grid,
        "ants": ants,
        "running": False,
        "steps": 0
    }

# ================== STEP LOGIC ==================
def step_simulation():
    game = st.session_state.ant_game
    grid = game["grid"]
    size = len(grid)

    for ant in game["ants"]:
        x, y = ant["x"], ant["y"]

        if grid[y][x] == 0:  # WHITE
            ant["dir"] = (ant["dir"] + 1) % 4
            grid[y][x] = 1
        else:               # BLACK
            ant["dir"] = (ant["dir"] - 1) % 4
            grid[y][x] = 0

        if ant["dir"] == NORTH:
            ant["y"] = (y - 1) % size
        elif ant["dir"] == SOUTH:
            ant["y"] = (y + 1) % size
        elif ant["dir"] == EAST:
            ant["x"] = (x + 1) % size
        elif ant["dir"] == WEST:
            ant["x"] = (x - 1) % size

    game["steps"] += 1

# ================== RENDER ==================
def render_grid():
    game = st.session_state.ant_game
    grid = game["grid"]
    ants = game["ants"]
    size = len(grid)

    ant_positions = {(a["x"], a["y"]) for a in ants}

    display = []
    for y in range(size):
        row = ""
        for x in range(size):
            if (x, y) in ant_positions:
                row += "🐜"
            else:
                row += "⬛" if grid[y][x] else "⬜"
        display.append(row)

    return "\n".join(display)

# ================== MAIN ENTRY ==================
def run():
    st.title("🐜 Langton’s Ant")
    st.caption("Cellular Automata Simulation — Emergent Behavior")

    with st.expander("📜 Rules", expanded=True):
        st.markdown(RULES_TEXT)

    # ---------- Controls ----------
    with st.sidebar:
        st.subheader("⚙️ Controls")
        grid_size = st.slider("Grid Size", 20, 60, 30, step=5)
        num_ants = st.slider("Number of Ants", 1, 10, 1)
        speed = st.slider("Speed (seconds)", 0.01, 0.3, 0.1)

        if st.button("🔄 Reset"):
            init_game(grid_size, num_ants)
            st.rerun()

        if "ant_game" in st.session_state:
            st.session_state.ant_game["running"] = st.toggle(
                "▶ Run Simulation",
                st.session_state.ant_game["running"]
            )

        if st.button("⏭ Step Once"):
            if "ant_game" in st.session_state:
                step_simulation()
                st.rerun()

    # ---------- Init ----------
    if "ant_game" not in st.session_state:
        init_game(grid_size, num_ants)

    game = st.session_state.ant_game

    # ---------- Simulation ----------
    if game["running"]:
        step_simulation()
        time.sleep(speed)
        st.rerun()

    # ---------- Display ----------
    st.markdown(f"**Steps:** {game['steps']}")
    st.code(render_grid())

# ================== REQUIRED ==================
if __name__ == "__main__":
    run()
