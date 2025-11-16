import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time
import random

# ---------------------------
# SAFE SESSION VALUES
# ---------------------------
if "feed_mode" not in st.session_state:
    st.session_state.feed_mode = False

if "food_positions" not in st.session_state:
    st.session_state.food_positions = []

# ---------------------------
# FISH TANK ASCII SETUP
# ---------------------------

WIDTH = 40
HEIGHT = 12

FISH = ["<><", "<=>", "><>"]

def draw_tank(food_list):
    tank = []

    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            if y == 0 or y == HEIGHT - 1:
                row += "#"
            elif x == 0 or x == WIDTH - 1:
                row += "#"
            else:
                if (x, y) in food_list:
                    row += "*"
                else:
                    row += " "
        tank.append(row)

    return "\n".join(tank)

# ---------------------------
# MAIN RUN FUNCTION
# ---------------------------

def run():

    st.title("🐟 Fish Tank")

    st.write("Tap anywhere on the canvas to drop food. Fish will move randomly.")

    # -------------------------------------------------
    # CANVAS (Exact same as your original)
    # -------------------------------------------------
    canvas = st_canvas(
        stroke_width=1,
        stroke_color="#000000",
        background_color="#ADD8E6",
        height=300,
        width=400,
        drawing_mode="point",
        key="canvas",
    )

    # -------------------------------------------------
    # SAFELY HANDLE feed_mode + canvas.json_data
    # -------------------------------------------------
    json_data = canvas.json_data if canvas and hasattr(canvas, "json_data") else None

    if st.session_state.feed_mode and json_data and "objects" in json_data:
        if len(json_data["objects"]) > 0:
            last = json_data["objects"][-1]
            cx = int(last["left"] / 10)
            cy = int(last["top"] / 25)

            st.session_state.food_positions.append((cx, cy))

    # -------------------------------------------------
    # DISPLAY TANK
    # -------------------------------------------------
    tank = draw_tank(st.session_state.food_positions)
    st.text(tank)

    # -------------------------------------------------
    # BUTTONS
    # -------------------------------------------------
    if st.button("Feed Mode"):
        st.session_state.feed_mode = True

    if st.button("Stop Feed"):
        st.session_state.feed_mode = False

    if st.button("Clear Food"):
        st.session_state.food_positions = []

