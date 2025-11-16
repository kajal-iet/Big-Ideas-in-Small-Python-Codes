# etching_drawer_streamlit.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Unicode characters for drawing
UP_DOWN_CHAR         = chr(9474)   # │
LEFT_RIGHT_CHAR      = chr(9472)   # ─
DOWN_RIGHT_CHAR      = chr(9484)   # ┌
DOWN_LEFT_CHAR       = chr(9488)   # ┐
UP_RIGHT_CHAR        = chr(9492)   # └
UP_LEFT_CHAR         = chr(9496)   # ┘
UP_DOWN_RIGHT_CHAR   = chr(9500)   # ├
UP_DOWN_LEFT_CHAR    = chr(9508)   # ┤
DOWN_LEFT_RIGHT_CHAR = chr(9516)   # ┬
UP_LEFT_RIGHT_CHAR   = chr(9524)   # ┴
CROSS_CHAR           = chr(9532)   # ┼

CANVAS_WIDTH = 40
CANVAS_HEIGHT = 20


# ✅ Central classifier — used by both text and PNG renderers
def classify(d):
    if not d:
        return ' '

    if d.issubset({'W', 'S'}):
        return UP_DOWN_CHAR

    if d.issubset({'A', 'D'}):
        return LEFT_RIGHT_CHAR

    if d == {'S', 'D'}:
        return DOWN_RIGHT_CHAR
    if d == {'A', 'S'}:
        return DOWN_LEFT_CHAR
    if d == {'W', 'D'}:
        return UP_RIGHT_CHAR
    if d == {'W', 'A'}:
        return UP_LEFT_CHAR

    if d == {'W', 'S', 'D'}:
        return UP_DOWN_RIGHT_CHAR
    if d == {'W', 'S', 'A'}:
        return UP_DOWN_LEFT_CHAR
    if d == {'A', 'S', 'D'}:
        return DOWN_LEFT_RIGHT_CHAR
    if d == {'W', 'A', 'D'}:
        return UP_LEFT_RIGHT_CHAR

    if d == {'W', 'A', 'S', 'D'}:
        return CROSS_CHAR

    return ' '


def get_canvas_string(canvas, cx, cy):
    canvas_str = ''
    for row in range(CANVAS_HEIGHT):
        for col in range(CANVAS_WIDTH):
            if col == cx and row == cy:
                canvas_str += '#'
                continue

            cell = canvas.get((col, row))
            if cell is None:
                canvas_str += ' '
            else:
                canvas_str += classify(cell)
        canvas_str += '\n'
    return canvas_str


def render_image(canvas):
    img = Image.new('RGB', (CANVAS_WIDTH*20, CANVAS_HEIGHT*20), color='white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    for (x, y), directions in canvas.items():
        draw.text((x*20, y*20), classify(directions), fill='black', font=font)

    return img


def run():
    st.title("🖌 Etching Drawer")

    if 'canvas' not in st.session_state:
        st.session_state.canvas = {}
        st.session_state.cursor = [0, 0]
        st.session_state.moves = []
        st.session_state.redo_stack = []

    cursorX, cursorY = st.session_state.cursor

    st.text("Use WASD buttons to draw. Undo, Redo, Download as PNG available.")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button('W'):
            st.session_state.moves.append('W')
    with col2:
        if st.button('A'):
            st.session_state.moves.append('A')
    with col3:
        if st.button('S'):
            st.session_state.moves.append('S')
    with col4:
        if st.button('D'):
            st.session_state.moves.append('D')
    with col5:
        if st.button('Clear'):
            st.session_state.canvas = {}
            st.session_state.moves = []
            st.session_state.redo_stack = []

    undo_col, redo_col, download_col = st.columns(3)
    with undo_col:
        if st.button('Undo'):
            if st.session_state.moves:
                move = st.session_state.moves.pop()
                st.session_state.redo_stack.append(move)
    with redo_col:
        if st.button('Redo'):
            if st.session_state.redo_stack:
                st.session_state.moves.append(st.session_state.redo_stack.pop())
    with download_col:
        if st.button('Download PNG'):
            img = render_image(st.session_state.canvas)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            st.download_button(
                label="Download Drawing",
                data=buf.getvalue(),
                file_name="drawing.png",
                mime="image/png"
            )

    # Rebuild canvas from moves
    st.session_state.canvas = {}
    cursorX, cursorY = 0, 0

    for command in st.session_state.moves:
        if (cursorX, cursorY) not in st.session_state.canvas:
            st.session_state.canvas[(cursorX, cursorY)] = set()

        if command == 'W' and cursorY > 0:
            st.session_state.canvas[(cursorX, cursorY)].add('W')
            cursorY -= 1
            st.session_state.canvas.setdefault((cursorX, cursorY), set()).add('S')

        elif command == 'S' and cursorY < CANVAS_HEIGHT - 1:
            st.session_state.canvas[(cursorX, cursorY)].add('S')
            cursorY += 1
            st.session_state.canvas.setdefault((cursorX, cursorY), set()).add('W')

        elif command == 'A' and cursorX > 0:
            st.session_state.canvas[(cursorX, cursorY)].add('A')
            cursorX -= 1
            st.session_state.canvas.setdefault((cursorX, cursorY), set()).add('D')

        elif command == 'D' and cursorX < CANVAS_WIDTH - 1:
            st.session_state.canvas[(cursorX, cursorY)].add('D')
            cursorX += 1
            st.session_state.canvas.setdefault((cursorX, cursorY), set()).add('A')

    st.markdown(
    """
    <style>
    .etching {
        font-family: "DejaVu Sans Mono", "Cascadia Mono", "Fira Code", monospace;
        letter-spacing: 0px;
        line-height: 1.0;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
        f"<pre class='etching'>{get_canvas_string(st.session_state.canvas, cursorX, cursorY)}</pre>",
        unsafe_allow_html=True
    )

