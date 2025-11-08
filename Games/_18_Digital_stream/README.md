# Overview

Matrix Digital Rain is a reusable Streamlit visual module that renders a smooth, fullscreen, Matrix-style “digital rain” animation using HTML5 Canvas + JavaScript. It works as a standalone visualization or can be embedded into another Streamlit app (e.g., dashboards, timers, or interactive tools).

The animation is non-blocking, highly efficient, and runs entirely in the user's browser — ensuring Streamlit’s Python workflow remains fully responsive.

# Features

Smooth, 50 FPS Matrix-style falling characters

Uses original binary characters (0 and 1)

Non-blocking JavaScript animation (no UI freeze)

Clean run(height=...) wrapper for reuse

Works inside any Streamlit page via st.components.html()

Fully self-contained (no dependencies)



# TODO List
[ ] Character Set Switcher: Toggle between
Binary (01), Hex, ASCII, Emoji, Katakana.

Intelligent Effects

[ ] Message Reveal: Rain slowly morphs into readable text (e.g., “ACCESS GRANTED”).

[ ] Wave Mode: Rain oscillates horizontally in sine-wave motion for a surreal effect.
