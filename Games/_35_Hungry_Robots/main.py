import streamlit as st
import random

# ------------------ CONFIG ------------------
WIDTH = 15
HEIGHT = 12
NUM_ROBOTS = 8
NUM_TELEPORTS = 2

EMPTY = " "
PLAYER = "🧍"
ROBOT = "🤖"
DEAD = "💥"
WALL = "⬛"

# ------------------ RULES ------------------
RULES = """
## 🤖 Hungry Robots — Rules

- You are trapped in a maze with **hungry robots**
- Robots move **one step toward you every turn**
- Robots do **not avoid obstacles**
- If robots collide → they **destroy each other**
- If a robot reaches you → **Game Over**
- You can:
  - Move in **8 directions**
  - Use **Teleport** (limited uses)
- Win by destroying **all robots**
"""

# ------------------ HELPERS ------------------
def empty_board():
    board = {}
    for x in range(WIDTH):
        for y in range(HEIGHT):
            board[(x, y)] = EMPTY

    for x in range(WIDTH):
        board[(x, 0)] = WALL
        board[(x, HEIGHT - 1)] = WALL
    for y in range(HEIGHT):
        board[(0, y)] = WALL
        board[(WIDTH - 1, y)] = WALL

    return board


def random_empty(board, occupied):
    while True:
        x = random.randint(1, WIDTH - 2)
        y = random.randint(1, HEIGHT - 2)
        if board[(x, y)] == EMPTY and (x, y) not in occupied:
            return (x, y)


def move_robot(rx, ry, px, py):
    dx = 1 if px > rx else -1 if px < rx else 0
    dy = 1 if py > ry else -1 if py < ry else 0
    return rx + dx, ry + dy


# ------------------ GAME INIT ------------------
def reset_game():
    st.session_state.board = empty_board()
    st.session_state.player = random_empty(st.session_state.board, [])
    st.session_state.robots = [
        random_empty(st.session_state.board, [])
        for _ in range(NUM_ROBOTS)
    ]
    st.session_state.teleports = NUM_TELEPORTS
    st.session_state.score = 0
    st.session_state.over = False


# ------------------ RENDER ------------------
def render():
    grid = ""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pos = (x, y)
            if pos == st.session_state.player:
                grid += PLAYER
            elif pos in st.session_state.robots:
                grid += ROBOT
            else:
                grid += st.session_state.board[pos]
        grid += "\n"
    st.code(grid)


# ------------------ GAME STEP ------------------
def step(move=None, teleport=False):
    if st.session_state.over:
        return

    px, py = st.session_state.player

    if teleport and st.session_state.teleports > 0:
        st.session_state.teleports -= 1
        st.session_state.player = random_empty(
            st.session_state.board, st.session_state.robots
        )

    elif move:
        nx, ny = px + move[0], py + move[1]
        if st.session_state.board[(nx, ny)] == EMPTY:
            st.session_state.player = (nx, ny)

    # Move robots
    next_positions = {}
    survivors = []

    for rx, ry in st.session_state.robots:
        nx, ny = move_robot(rx, ry, *st.session_state.player)

        if (nx, ny) == st.session_state.player:
            st.session_state.over = True
            return

        next_positions.setdefault((nx, ny), 0)
        next_positions[(nx, ny)] += 1

    for pos, count in next_positions.items():
        if count == 1:
            survivors.append(pos)
        else:
            st.session_state.score += count

    st.session_state.robots = survivors

    if not survivors:
        st.session_state.over = True


# ------------------ UI ------------------
def run():
    st.set_page_config("Hungry Robots", layout="centered")
    st.title("🤖 Hungry Robots")
    st.caption("Inspired by Al Sweigart — Big Book of Small Python Projects")

    st.markdown(RULES)

    if "board" not in st.session_state:
        reset_game()

    # -------- Board --------
    render()

    # -------- Stats --------
    s1, s2, s3 = st.columns(3)
    s1.metric("🤖 Robots", len(st.session_state.robots))
    s2.metric("💥 Score", st.session_state.score)
    s3.metric("🌀 Teleports", st.session_state.teleports)

    # -------- Controls BELOW board --------
    st.markdown("### 🎮 Move")

    # Top row
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("↖"):
            step((-1, -1)); st.rerun()
    with c2:
        if st.button("⬆"):
            step((0, -1)); st.rerun()
    with c3:
        if st.button("↗"):
            step((1, -1)); st.rerun()

    # Middle row
    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("⬅"):
            step((-1, 0)); st.rerun()
    with c5:
        st.markdown("<div style='text-align:center;'>🧍</div>", unsafe_allow_html=True)
    with c6:
        if st.button("➡"):
            step((1, 0)); st.rerun()

    # Bottom row
    c7, c8, c9 = st.columns(3)
    with c7:
        if st.button("↙"):
            step((-1, 1)); st.rerun()
    with c8:
        if st.button("⬇"):
            step((0, 1)); st.rerun()
    with c9:
        if st.button("↘"):
            step((1, 1)); st.rerun()

    # -------- Actions --------
    st.markdown("---")
    a1, a2 = st.columns(2)
    with a1:
        if st.button("🌀 Teleport"):
            step(teleport=True); st.rerun()
    with a2:
        if st.button("🔄 Restart"):
            reset_game(); st.rerun()

    # -------- End states --------
    if st.session_state.over:
        if st.session_state.robots:
            st.error("💀 You were caught by a robot!")
        else:
            st.success("🎉 All robots destroyed! You win!")


# ------------------ RUN ------------------
if __name__ == "__main__":
    run()
