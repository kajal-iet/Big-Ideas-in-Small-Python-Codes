import streamlit as st
import time

# ----------------------------
# FUNCTIONS
# ----------------------------
def display_outline_diamond(size):
    lines = []
    for i in range(size):
        lines.append(' ' * (size - i - 1) + '/' + ' ' * (i * 2) + '\\')
    for i in range(size):
        lines.append(' ' * i + '\\' + ' ' * ((size - i - 1) * 2) + '/')
    return lines

def display_filled_diamond(size):
    lines = []
    for i in range(size):
        lines.append(' ' * (size - i - 1) + '/' * (i + 1) + '\\' * (i + 1))
    for i in range(size):
        lines.append(' ' * i + '\\' * (size - i) + '/' * (size - i))
    return lines

def rotate_lines_90(lines):
    max_len = max(len(line) for line in lines)
    padded = [line.ljust(max_len) for line in lines]
    rotated = [''.join(row[::-1]) for row in zip(*padded)]
    return rotated

def render_lines(lines, placeholder):
    placeholder.text("\n".join(lines))

# ----------------------------
# STREAMLIT UI
# ----------------------------
def run():
    st.title("""
     # 💎 Animated Diamonds

        **Animated Diamonds** is a fun, interactive Streamlit app that lets users create and animate ASCII art diamonds. You can:

        - Generate **Outline or Filled diamonds**.
        - Choose the **size** of your diamond.
        - Apply animations:
        - **Pulsating**: diamond grows and shrinks.
        - **Rotating**: diamond rotates 90°, 180°, and 270°.
        - Control the **animation speed**.
        - Start and stop animations anytime.
    """)

    # Diamond type
    diamond_type = st.radio("Diamond Type", ["Outline", "Filled"], key="diamond_type")

    # Base size
    size = st.slider("Base Size", 1, 10, 4, key="size_slider")

    # Animation type
    animation_type = st.radio("Animation", ["None", "Pulsating", "Rotating"], key="animation_type")

    # Animation speed
    speed = st.slider("Animation Speed (seconds)", 0.05, 0.5, 0.2, 0.01, key="speed_slider")

    # Start / Stop buttons
    if "animating" not in st.session_state:
        st.session_state.animating = False

    start = st.button("Start Animation", key="start_button")
    stop = st.button("Stop Animation", key="stop_button")

    if start:
        st.session_state.animating = True
    if stop:
        st.session_state.animating = False

    placeholder = st.empty()

    # ----------------------------
    # ANIMATION LOOP
    # ----------------------------
    if st.session_state.animating:
        if animation_type == "Pulsating":
            # Grow and shrink repeatedly
            for s in list(range(1, size + 1)) + list(range(size - 1, 0, -1)):
                if not st.session_state.animating:
                    break
                lines = display_outline_diamond(s) if diamond_type=="Outline" else display_filled_diamond(s)
                render_lines(lines, placeholder)
                time.sleep(speed)

        elif animation_type == "Rotating":
            lines = display_outline_diamond(size) if diamond_type=="Outline" else display_filled_diamond(size)
            rotations = [lines]
            for _ in range(3):
                lines = rotate_lines_90(lines)
                rotations.append(lines)
            while st.session_state.animating:
                for r in rotations:
                    if not st.session_state.animating:
                        break
                    render_lines(r, placeholder)
                    time.sleep(speed)

        else:  # No animation
            lines = display_outline_diamond(size) if diamond_type=="Outline" else display_filled_diamond(size)
            render_lines(lines, placeholder)
