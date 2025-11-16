import streamlit as st
import random
import time
from streamlit_drawable_canvas import st_canvas

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
WIDTH = 70
HEIGHT = 25
FPS = 5

FISH_TYPES = [
    {'right': ['><>'], 'left': ['<><']},
    {'right': ['>||>'], 'left': ['<||<']},
    {'right': ['>))>'], 'left': ['<[[<']},
]

CRAB_FRAMES = ["(\\_/)=", "=(\\_/)"]
SAND_CHAR = "░"

# KELP PATTERNS
KELP_CHARS = ["(", ")"]

# ---------------------------------------------------------
# INIT SESSION STATE
# ---------------------------------------------------------
if "fishes" not in st.session_state:
    st.session_state.fishes = []

if "crabs" not in st.session_state:
    st.session_state.crabs = []

if "foods" not in st.session_state:
    st.session_state.foods = []        # food pellets

if "kelps" not in st.session_state:
    st.session_state.kelps = []

if "bubbles" not in st.session_state:
    st.session_state.bubbles = []

if "bubblers" not in st.session_state:
    st.session_state.bubblers = [10, 30, 55]   # bubble sources

if "frame" not in st.session_state:
    st.session_state.frame = 0

if "feed_mode" not in st.session_state:
    st.session_state.feed_mode = False


# ---------------------------------------------------------
# UTILITY
# ---------------------------------------------------------
def empty_grid():
    return [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

def place_text(grid, x, y, text):
    if 0 <= y < HEIGHT:
        for i, ch in enumerate(text):
            if 0 <= x + i < WIDTH:
                grid[y][x + i] = ch


# ---------------------------------------------------------
# GENERATORS
# ---------------------------------------------------------
def generate_fish():
    f = random.choice(FISH_TYPES)
    return {
        "x": random.randint(0, WIDTH-4),
        "y": random.randint(2, HEIGHT-6),
        "right": f['right'],
        "left": f['left'],
        "dir": random.choice([1, -1]),
        "speed": random.randint(3, 6)
    }

def generate_crab():
    return {
        "x": random.randint(0, WIDTH-6),
        "y": HEIGHT - 2,
        "dir": random.choice([1, -1]),
        "frame": 0
    }

def generate_kelp():
    height = random.randint(5, 12)
    return {
        "x": random.randint(1, WIDTH - 2),
        "segments": [random.choice(KELP_CHARS) for _ in range(height)]
    }

# ---------------------------------------------------------
# FEED MODE TOGGLE
# ---------------------------------------------------------
def toggle_feed():
    st.session_state.feed_mode = not st.session_state.feed_mode


# ---------------------------------------------------------
# SIMULATION
# ---------------------------------------------------------
def simulate():
    # FISH MOVEMENT
    for fish in st.session_state.fishes:
        # If food exists, move toward nearest
        if st.session_state.foods:
            nearest = min(
                st.session_state.foods,
                key=lambda f: abs(f["x"] - fish["x"]) + abs(f["y"] - fish["y"])
            )

            if nearest["x"] > fish["x"]:
                fish["x"] += 1
                fish["dir"] = 1
            elif nearest["x"] < fish["x"]:
                fish["x"] -= 1
                fish["dir"] = -1

            if nearest["y"] > fish["y"]:
                fish["y"] += 1
            elif nearest["y"] < fish["y"]:
                fish["y"] -= 1
        else:
            # Free swim horizontal
            if st.session_state.frame % fish["speed"] == 0:
                fish["x"] += fish["dir"]
                if fish["x"] <= 0 or fish["x"] >= WIDTH - 4:
                    fish["dir"] *= -1

    # CRABS
    for c in st.session_state.crabs:
        c["x"] += c["dir"]
        if c["x"] <= 0 or c["x"] >= WIDTH - 6:
            c["dir"] *= -1
        c["frame"] = (c["frame"] + 1) % 2

    # KELP WAVING
    for kelp in st.session_state.kelps:
        for i in range(len(kelp["segments"])):
            if random.randint(1, 10) == 1:
                kelp["segments"][i] = "(" if kelp["segments"][i] == ")" else ")"

    # BUBBLES RISING
    for b in st.session_state.bubblers:
        # chance of bubble
        if random.randint(1, 6) == 1:
            st.session_state.bubbles.append({"x": b, "y": HEIGHT-3})

    for bub in st.session_state.bubbles:
        bub["y"] -= 1

    st.session_state.bubbles = [
        b for b in st.session_state.bubbles if b["y"] > 0
    ]

    # FOOD FALLING
    for f in st.session_state.foods:
        f["y"] += 1

    st.session_state.foods = [
        f for f in st.session_state.foods if f["y"] < HEIGHT-2
    ]


# ---------------------------------------------------------
# DRAW FRAME
# ---------------------------------------------------------
def draw_frame():
    grid = empty_grid()

    # KELP
    for kelp in st.session_state.kelps:
        bx = kelp["x"]
        for idx, seg in enumerate(kelp["segments"]):
            y = HEIGHT - 2 - idx
            x = bx if seg == "(" else bx + 1
            place_text(grid, x, y, seg)

    # BUBBLES
    for b in st.session_state.bubbles:
        place_text(grid, b["x"], b["y"], "o")

    # FOOD
    for food in st.session_state.foods:
        place_text(grid, food["x"], food["y"], ".")

    # FISH
    for f in st.session_state.fishes:
        frame = st.session_state.frame % len(f["right"])
        fish_str = f["right"][frame] if f["dir"] == 1 else f["left"][frame]
        place_text(grid, f["x"], f["y"], fish_str)

    # CRABS
    for c in st.session_state.crabs:
        place_text(grid, c["x"], c["y"], CRAB_FRAMES[c["frame"]])

    # SAND
    place_text(grid, 0, HEIGHT - 1, SAND_CHAR * WIDTH)

    return "\n".join("".join(row) for row in grid)


# ---------------------------------------------------------
# MAIN UI
# ---------------------------------------------------------
def run():
    st.title("🐠 Fish Tank – FULL Version")
    st.subheader("Now with Kelp, Bubbles, Crabs, Feed Mode, and Click Support")

    st.markdown("""
    ### ✅ RULES:
    - Press **Add Fish** to spawn a fish  
    - Press **Add Crab** to spawn a crab  
    - Press **Add Kelp** to grow underwater plants  
    - Press **Toggle Feed Mode** and **click inside the tank** to drop food  
    - Fish will move toward food pellets  
    - Crabs walk along the sand  
    - Kelp waves automatically  
    - Bubbles rise from random bubblers  
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Add Fish"):
            st.session_state.fishes.append(generate_fish())
    with col2:
        if st.button("Add Crab"):
            st.session_state.crabs.append(generate_crab())
    with col3:
        if st.button("Add Kelp"):
            st.session_state.kelps.append(generate_kelp())

    st.button("Toggle Feed Mode", on_click=toggle_feed)

    # CLICKABLE CANVAS FOR FOOD PLACEMENT
    canvas = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=0,
        background_color="#000000",
        height=HEIGHT*12,
        width=WIDTH*10,
        drawing_mode="point",
        key="canvas",
    )

    if st.session_state.feed_mode and canvas.json_data:
        if len(canvas.json_data["objects"]) > 0:
            last = canvas.json_data["objects"][-1]
            cx = int(last["left"] / 10)
            cy = int(last["top"] / 12)
            st.session_state.foods.append({"x": cx, "y": cy})

    # DISPLAY TANK
    placeholder = st.empty()

    # ANIMATION LOOP
    while True:
        simulate()
        frame = draw_frame()
        placeholder.code(frame, language="text")
        st.session_state.frame += 1
        time.sleep(1 / FPS)
