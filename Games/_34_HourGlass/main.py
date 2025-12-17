import streamlit as st
import random
import time

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Hourglass Simulation",
    layout="centered"
)

WIDTH = 30
HEIGHT = 24
SAND = "●"
EMPTY = " "
WALL = "#"

# ------------------ GLASS GEOMETRY ------------------
def glass_bounds(y):
    mid = HEIGHT // 2
    neck = 2

    if y < mid:
        spread = (mid - y) // 2
    else:
        spread = (y - mid) // 2

    center = WIDTH // 2
    left = center - neck - spread
    right = center + neck + spread
    return left, right


def inside_glass(x, y):
    left, right = glass_bounds(y)
    return left < x < right


# ------------------ INIT GRID ------------------
def create_hourglass():
    grid = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Draw walls
    for y in range(HEIGHT):
        left, right = glass_bounds(y)
        grid[y][left] = WALL
        grid[y][right] = WALL

    # Fill sand (top half only)
    for y in range(3, HEIGHT // 2 - 1):
        left, right = glass_bounds(y)
        for x in range(left + 1, right):
            grid[y][x] = SAND

    return grid


# ------------------ PHYSICS STEP ------------------
def step(grid):
    moved = False

    for y in range(HEIGHT - 2, -1, -1):
        xs = list(range(1, WIDTH - 1))
        random.shuffle(xs)  # ⭐ removes left/right bias

        for x in xs:
            if grid[y][x] != SAND:
                continue

            # Try straight down first
            if grid[y + 1][x] == EMPTY and inside_glass(x, y + 1):
                grid[y][x], grid[y + 1][x] = EMPTY, SAND
                moved = True
                continue

            # Try diagonals (random order per grain)
            directions = [(-1, 1), (1, 1)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < WIDTH
                    and ny < HEIGHT
                    and grid[ny][nx] == EMPTY
                    and inside_glass(nx, ny)
                ):
                    grid[y][x], grid[ny][nx] = EMPTY, SAND
                    moved = True
                    break

    return moved


# ------------------ RENDER ------------------
def render(grid):
    return "\n".join("".join(row) for row in grid)


# ------------------ APP ------------------
def run():
    st.title("⏳ Hourglass")
    st.caption("Inspired by Al Sweigart — Physics Visualization")

    st.markdown("""
### ⏳ Rules
- Sand falls due to **gravity**
- Grains slide diagonally along the **glass slope**
- Sand is constrained inside the **hourglass shape**
- Click **Flip Hourglass** to restart
    """)

    if "grid" not in st.session_state:
        st.session_state.grid = create_hourglass()

    col1, col2 = st.columns(2)

    with col1:
        speed = st.slider("Simulation Speed", 0.01, 0.3, 0.12)

    with col2:
        if st.button("🔄 Flip Hourglass"):
            st.session_state.grid = create_hourglass()

    moved = step(st.session_state.grid)

    st.code(render(st.session_state.grid))

    if moved:
        time.sleep(speed)
        st.rerun()
    else:
        st.info("Sand has settled. Flip the hourglass to continue.")


# ------------------ RUN ------------------
if __name__ == "__main__":
    run()
