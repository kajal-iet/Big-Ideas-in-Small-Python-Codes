# forestfire_streamlit.py
"""
Forest Fire Simulator - Streamlit Edition (reduced-grid interactive)
Updated UI: dropdown-based controls (Low/Medium/High) instead of sliders,
so effects are clear to the user.

Features:
 - Clickable tiles (click to ignite)
 - Step / Start (auto-run) / Stop / Reset
 - Dropdown controls for initial density, grow chance, lightning, spread chance
 - Rain factor reduces lightning & spread (implemented feature)
 - Uses a 20x15 grid (300 buttons) for responsive UI
Includes main() and run() entrypoint
"""

import streamlit as st
import random
import time
import numpy as np
import copy

# ------------------ Constants & Defaults ------------------
TREE = "🌲"
FIRE = "🔥"
EMPTY = "⬜"
ASH = "⬛"   # burned / ash

WIDTH = 20   # Reduced grid width
HEIGHT = 15  # Reduced grid height

# Default numeric mappings for dropdown choices
INITIAL_DENSITY_MAP = {"Sparse": 0.15, "Normal": 0.25, "Dense": 0.40}
GROW_MAP = {"Low": 0.005, "Normal": 0.01, "High": 0.02}
LIGHTNING_MAP = {"Low": 0.005, "Normal": 0.01, "High": 0.02}
SPREAD_MAP = {"Low": 0.3, "Normal": 0.6, "High": 0.9}
RAIN_MAP = {"None": 0.0, "Light": 0.3, "Heavy": 0.6}
SPEED_MAP = {"Fast": 0.03, "Normal": 0.12, "Slow": 0.4}

# ------------------ Session Initialization ------------------
def init_session_state():
    if "forest" not in st.session_state:
        st.session_state.forest = create_forest(INITIAL_DENSITY_MAP["Normal"])
    if "running" not in st.session_state:
        st.session_state.running = False
    if "moves" not in st.session_state:
        st.session_state.moves = 0
    if "last_action" not in st.session_state:
        st.session_state.last_action = None

# ------------------ Forest Creation ------------------
def create_forest(initial_density):
    # 2D list of strings
    board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if random.random() < initial_density:
                board[i][j] = TREE
    return board

# ------------------ Simulation Step ------------------
def step_simulation(grow_chance, lightning_chance, spread_chance, rain_factor):
    """
    One simulation timestep:
    - EMPTY -> TREE with probability grow_chance
    - TREE -> FIRE by lightning (lightning_chance * (1 - rain_factor))
    - FIRE spreads to neighbor TREES with probability spread_chance * (1 - rain_factor)
    - FIRE -> ASH (burned) after spreading
    """
    old = st.session_state.forest
    new = copy.deepcopy(old)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            cell = old[i][j]

            if cell == EMPTY:
                if random.random() < grow_chance:
                    new[i][j] = TREE

            elif cell == TREE:
                # lightning (reduced by rain)
                if random.random() < (lightning_chance * (1 - rain_factor)):
                    new[i][j] = FIRE

            elif cell == FIRE:
                # spread to neighbors (4-directional)
                for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < HEIGHT and 0 <= nj < WIDTH:
                        if old[ni][nj] == TREE:
                            if random.random() < (spread_chance * (1 - rain_factor)):
                                new[ni][nj] = FIRE
                # burned becomes ash next step
                new[i][j] = ASH

            elif cell == ASH:
                # Ash -> EMPTY gradually (50% chance per step)
                if random.random() < 0.5:
                    new[i][j] = EMPTY
                else:
                    new[i][j] = ASH

    st.session_state.forest = new
    st.session_state.moves += 1

# ------------------ Utility: draw grid as buttons ------------------
def render_grid(interaction_mode="ignite"):
    """Render grid using st.columns rows. Clicking a button ignites that cell."""
    for i in range(HEIGHT):
        cols = st.columns(WIDTH)
        for j in range(WIDTH):
            label = st.session_state.forest[i][j]
            # button shows emoji representing the cell
            clicked = cols[j].button(label, key=f"cell_{i}_{j}")
            if clicked:
                # Click = ignite immediately (set to FIRE)
                st.session_state.forest[i][j] = FIRE
                # Immediately update the UI to reflect the ignition
                st.rerun()

# ------------------ MAIN UI ------------------
def main():
    st.set_page_config(page_title="Forest Fire Simulator", layout="centered")
    init_session_state()

    st.title("🌲🔥 Forest Fire Simulator (interactive)")

    # Sidebar controls (dropdowns instead of sliders)
    st.sidebar.header("Simulation Settings (dropdowns)")

    initial_density_label = st.sidebar.selectbox(
        "Initial Tree Density",
        options=["Sparse", "Normal", "Dense"],
        index=1,
        help="How many trees are placed on a fresh forest."
    )
    initial_density = INITIAL_DENSITY_MAP[initial_density_label]

    grow_label = st.sidebar.selectbox(
        "Tree Growth Rate",
        options=["Low", "Normal", "High"],
        index=1,
        help="Higher -> empty cells regrow into trees more often."
    )
    grow_chance = GROW_MAP[grow_label]

    lightning_label = st.sidebar.selectbox(
        "Lightning Likelihood",
        options=["Low", "Normal", "High"],
        index=1,
        help="Higher -> trees are more frequently struck by lightning."
    )
    lightning_chance = LIGHTNING_MAP[lightning_label]

    spread_label = st.sidebar.selectbox(
        "Fire Spread Aggression",
        options=["Low", "Normal", "High"],
        index=1,
        help="Higher -> fire is more likely to spread to neighboring trees."
    )
    spread_chance = SPREAD_MAP[spread_label]

    rain_label = st.sidebar.selectbox(
        "Rain Level",
        options=["None", "Light", "Heavy"],
        index=0,
        help="Higher -> reduces lightning and spread probabilities."
    )
    rain_factor = RAIN_MAP[rain_label]

    speed_label = st.sidebar.selectbox(
        "Auto-run Speed",
        options=["Fast", "Normal", "Slow"],
        index=1,
        help="Control step delay when auto-running the simulation."
    )
    speed = SPEED_MAP[speed_label]

    # Show numeric values next to dropdowns for clarity
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Selected numeric values**")
    st.sidebar.markdown(f"- Initial density = **{initial_density:.3f}**")
    st.sidebar.markdown(f"- Grow chance = **{grow_chance:.4f}** per step")
    st.sidebar.markdown(f"- Lightning chance = **{lightning_chance:.4f}** per tree per step")
    st.sidebar.markdown(f"- Spread chance = **{spread_chance:.3f}**")
    st.sidebar.markdown(f"- Rain factor = **{rain_factor:.2f}**")
    st.sidebar.markdown(f"- Auto-run delay = **{speed:.2f}s**")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Actions**")
    if st.sidebar.button("Reset forest"):
        st.session_state.forest = create_forest(initial_density)
        st.session_state.moves = 0
        st.session_state.running = False
        st.rerun()

    if st.sidebar.button("Ignite random tree"):
        trees = [(i, j) for i in range(HEIGHT) for j in range(WIDTH) if st.session_state.forest[i][j] == TREE]
        if trees:
            i, j = random.choice(trees)
            st.session_state.forest[i][j] = FIRE
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Auto-run controls**")
    col1, col2 = st.sidebar.columns(2)
    start = col1.button("Start")
    stop = col2.button("Stop")
    step = st.sidebar.button("Step")

    # Handle Start / Stop / Step
    if start:
        st.session_state.running = True
        st.session_state.last_action = "start"
        st.rerun()
    if stop:
        st.session_state.running = False
        st.session_state.last_action = "stop"
        st.rerun()
    if step:
        step_simulation(grow_chance, lightning_chance, spread_chance, rain_factor)
        st.rerun()

    # Info & legend
    st.markdown("### Controls & Legend")
    st.write(f"Steps run: **{st.session_state.moves}**")
    st.markdown(f"- {TREE} = Tree")
    st.markdown(f"- {FIRE} = Fire")
    st.markdown(f"- {ASH} = Ash (recently burned)")
    st.markdown(f"- {EMPTY} = Empty")

    st.markdown("---")
    st.markdown("### Click grid to ignite a cell (clicking sets it to FIRE)")

    # Grid rendering (clickable)
    render_grid(interaction_mode="ignite")

    # Auto-run: when running is True, do a single step, wait, rerun (loop behavior)
    if st.session_state.running:
        step_simulation(grow_chance, lightning_chance, spread_chance, rain_factor)
        # small delay to control speed
        time.sleep(speed)
        # rerun to update UI and continue loop
        st.rerun()

    # Footer: small notes
    st.markdown("---")
    st.markdown("Notes: Rain reduces both lightning ignition and neighbor spread by multiplying probabilities with (1 - rain level).")

def run():
    main()

if __name__ == "__main__":
    run()
