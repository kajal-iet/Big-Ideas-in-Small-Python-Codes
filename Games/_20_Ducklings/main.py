import streamlit as st
import random
import time
import datetime

# ---------------------------
# CONSTANTS
# ---------------------------
PAUSE = 0.20
DENSITY = 0.10

DUCKLING_WIDTH = 5
LEFT = 'left'
RIGHT = 'right'
BEADY = 'beady'
WIDE = 'wide'
HAPPY = 'happy'
ALOOF = 'aloof'
CHUBBY = 'chubby'
VERY_CHUBBY = 'very chubby'
OPEN = 'open'
CLOSED = 'closed'
OUT = 'out'
DOWN = 'down'
UP = 'up'
HEAD = 'head'
BODY = 'body'
FEET = 'feet'


def get_seasonal_hat():
    if "seasonal" not in st.session_state:
        return ""

    if not st.session_state.seasonal:
        return ""

    month = datetime.datetime.now().month

    if month == 12:
        return "^🎅"
    if month == 10:
        return "^🎃"
    if month in [5, 6]:
        return "^🎓"

    return ""


# ------------------------------------------------------
# DUCKLING CLASS
# ------------------------------------------------------
class Duckling:
    def __init__(self):
        self.direction = random.choice([LEFT, RIGHT])
        self.body = random.choice([CHUBBY, VERY_CHUBBY])
        self.mouth = random.choice([OPEN, CLOSED])
        self.wing = random.choice([OUT, UP, DOWN])

        if self.body == CHUBBY:
            self.eyes = BEADY
        else:
            self.eyes = random.choice([BEADY, WIDE, HAPPY, ALOOF])

        self.partToDisplayNext = HEAD

    def getHeadStr(self):
        headStr = ''

        if self.direction == LEFT:
            headStr += '>' if self.mouth == OPEN else '='
            if self.eyes == BEADY and self.body == CHUBBY:
                headStr += '"'
            elif self.eyes == BEADY:
                headStr += '" '
            elif self.eyes == WIDE:
                headStr += "''"
            elif self.eyes == HAPPY:
                headStr += '^^'
            elif self.eyes == ALOOF:
                headStr += '``'
            headStr += ') '

        if self.direction == RIGHT:
            headStr += ' ('
            if self.eyes == BEADY and self.body == CHUBBY:
                headStr += '"'
            elif self.eyes == BEADY:
                headStr += ' "'
            elif self.eyes == WIDE:
                headStr += "''"
            elif self.eyes == HAPPY:
                headStr += '^^'
            elif self.eyes == ALOOF:
                headStr += '``'
            headStr += '<' if self.mouth == OPEN else '='

        if self.body == CHUBBY:
            headStr += ' '

        headStr = get_seasonal_hat() + headStr
        return headStr

    def getBodyStr(self):
        bodyStr = '('

        if self.direction == LEFT:
            bodyStr += ' ' if self.body == CHUBBY else '  '
            bodyStr += {'out': '>', 'up': '^', 'down': 'v'}[self.wing]
        else:
            bodyStr += {'out': '<', 'up': '^', 'down': 'v'}[self.wing]
            bodyStr += ' ' if self.body == CHUBBY else '  '

        bodyStr += ')'

        if self.body == CHUBBY:
            bodyStr += ' '
        return bodyStr

    def getFeetStr(self):
        return ' ^^  ' if self.body == CHUBBY else ' ^ ^ '

    def getNextBodyPart(self):
        if self.partToDisplayNext == HEAD:
            self.partToDisplayNext = BODY
            return self.getHeadStr()
        elif self.partToDisplayNext == BODY:
            self.partToDisplayNext = FEET
            return self.getBodyStr()
        elif self.partToDisplayNext == FEET:
            self.partToDisplayNext = None
            return self.getFeetStr()


# ------------------------------------------------------
# STREAMLIT VERSION
# ------------------------------------------------------
def run():
    st.title("🦆 Ducklings Animation – Streamlit Edition")

    st.subheader("📘 How It Works")
    st.markdown("""
- A continuous stream of ASCII ducklings scrolls across the screen.
- Ducklings are randomly generated:
  - Direction (Left/Right)
  - Eye style
  - Mouth style
  - Wing position
  - Body type
- Over 90 unique duck combinations!
""")

    st.divider()

    st.subheader("🐥 Duckling Display Options")

    mode = st.selectbox(
        "Choose Mode:",
        ["Random Falling Ducks", "Duck Parade"]
    )

    st.session_state.seasonal = st.checkbox("Enable Seasonal Ducks 🎉")

    col1, col2 = st.columns(2)
    with col1:
        density = st.slider("Duck Density", 0.01, 0.50, 0.10, step=0.01)
    with col2:
        speed = st.slider("Speed (lower = faster)", 0.05, 1.0, 0.20, step=0.05)

    if st.button("▶ Start Animation"):
        placeholder = st.empty()

        lanes = [""] * 20

        if mode == "Duck Parade":
            parade_duck = Duckling()

        while True:

            # -------------------------------------------------
            # PARADE MODE
            # -------------------------------------------------
            # ✅ ✅ PARADE MODE (3-row ASCII)
            if mode == "Duck Parade":

                # Get all 3 parts at once
                head = parade_duck.getHeadStr()
                body = parade_duck.getBodyStr()
                feet = parade_duck.getFeetStr()

                # If duck is finished, spawn new
                parade_duck = Duckling()

                # Build 3-row ASCII
                top_row = head * len(lanes)
                mid_row = body * len(lanes)
                bottom_row = feet * len(lanes)

                parade_frame = top_row + "\n" + mid_row + "\n" + bottom_row

                placeholder.code(parade_frame, language="text")

                time.sleep(speed)
                continue


            # -------------------------------------------------
            # NORMAL RANDOM MODE
            # -------------------------------------------------
            # ✅ ✅ NORMAL MODE -------------
            top_row = ""
            mid_row = ""
            bottom_row = ""

            for i in range(len(lanes)):

                if lanes[i] == "":
                    if random.random() <= density:
                        lanes[i] = Duckling()

                if isinstance(lanes[i], Duckling):
                    head = lanes[i].getHeadStr()
                    body = lanes[i].getBodyStr()
                    feet = lanes[i].getFeetStr()

                    top_row += head
                    mid_row += body
                    bottom_row += feet

                    # remove duck after showing full 3 parts
                    lanes[i] = ""
                else:
                    top_row += " " * DUCKLING_WIDTH
                    mid_row += " " * DUCKLING_WIDTH
                    bottom_row += " " * DUCKLING_WIDTH

            # ✅ Combine into 3-line ASCII block
            line = top_row + "\n" + mid_row + "\n" + bottom_row

            placeholder.code(line, language="text")
            time.sleep(speed)

if __name__ == "__main__":
    run()
