import streamlit as st
import random
import time
import numpy as np

# ------------------ Constants ------------------
TREE = "🌲"
FIRE = "🔥"
EMPTY = "⬜"

# Grid size
WIDTH = 40
HEIGHT = 25

# ------------------ Sidebar Controls ------------------
st.sidebar.title("⚙ Simulation Settings")

initial_tree_density = st.sidebar.slider("Initial Tree Density", 0.0, 1.0, 0.25)
grow_chance = st.sidebar.slider("Tree Growth Chance (per step)", 0.0, 1.0, 0.01)
fire_chance = st.sidebar.slider("Lightning Fire Chance (per step)", 0.0, 1.0, 0.01)

# 🔥 Additional Feature 1 — Fire Spread Probability
spread_chance = st.sidebar.slider("Fire Spread Chance", 0.0, 1.0, 0.60)

# 🌧 Additional Feature 2 — Rain reduces fire chance
rain_factor = st.sidebar.slider("Rain Level (reduces fire chance)", 0.0, 1.0, 0.3)

speed = st.sidebar.slider("Simulation Speed (seconds per step)", 0.01, 1.0, 0.15)

# ------------------ Init Session State ------------------
if "forest" not in st.session_state:
    forest = np.full((HEIGHT, WIDTH), EMPTY)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            if random.random() < initial_tree_density:
                forest[i][j] = TREE

    st.session_state.forest = forest


# ------------------ Simulation Step Function ------------------
def step():
    forest = st.session_state.forest
    new_forest = forest.copy()

    for i in range(HEIGHT):
        for j in range(WIDTH):

            if forest[i][j] == EMPTY:
                if random.random() < grow_chance:
                    new_forest[i][j] = TREE

            elif forest[i][j] == TREE:
                # Lightning strike → fire
                if random.random() < (fire_chance * (1 - rain_factor)):
                    new_forest[i][j] = FIRE

            elif forest[i][j] == FIRE:
                # Spread to neighbors with probability
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < HEIGHT and 0 <= nj < WIDTH:
                            if forest[ni][nj] == TREE and random.random() < spread_chance:
                                new_forest[ni][nj] = FIRE

                # Burned tree becomes empty
                new_forest[i][j] = EMPTY

    st.session_state.forest = new_forest

def run():
# ------------------ UI ------------------
    st.title("🌲🔥 Forest Fire Simulation ")

    placeholder = st.empty()

    # Auto-run loop
    for _ in range(300000):  # large number so it runs indefinitely
        board = "\n".join("".join(row) for row in st.session_state.forest)
        placeholder.markdown(f"``` \n{board}\n```")

        step()
        time.sleep(speed)

if __name__ == "__main__":
    run()

