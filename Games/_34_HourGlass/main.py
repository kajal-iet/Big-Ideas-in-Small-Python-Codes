"""
Hourglass (Borderless Version), by Al Sweigart
Modified: Adjustable speed + auto flip
"""

import random, sys, time

try:
    import bext
except ImportError:
    print('This program requires the bext module.')
    sys.exit()

# ------------------ CONSTANTS ------------------
PAUSE_LENGTH = 0.15     # ⭐ Feature 1: speed tuning
WIDE_FALL_CHANCE = 50

SCREEN_WIDTH = 79
SCREEN_HEIGHT = 25
X, Y = 0, 1
SAND = chr(9617)

# ------------------ INITIAL SAND ------------------
INITIAL_SAND = set()
for y in range(8):
    for x in range(30, 49):
        INITIAL_SAND.add((x, y + 4))

# ------------------ MAIN ------------------
def main():
    bext.fg('yellow')
    bext.clear()

    bext.goto(0, 0)
    print('Ctrl-C to quit. Hourglass simulation running...', end='')

    while True:
        allSand = list(INITIAL_SAND)

        for sand in allSand:
            bext.goto(sand[X], sand[Y])
            print(SAND, end='')

        runSimulation(allSand)

# ------------------ SIMULATION ------------------
def runSimulation(allSand):
    while True:
        random.shuffle(allSand)
        sandMoved = False

        for i, sand in enumerate(allSand):
            if sand[Y] >= SCREEN_HEIGHT - 1:
                continue

            below = (sand[X], sand[Y] + 1)
            if below not in allSand:
                moveSand(allSand, i, sand, 0)
                sandMoved = True
                continue

            directions = []
            if sand[X] > 0 and (sand[X] - 1, sand[Y] + 1) not in allSand:
                directions.append(-1)
            if sand[X] < SCREEN_WIDTH - 1 and (sand[X] + 1, sand[Y] + 1) not in allSand:
                directions.append(1)

            if directions:
                d = random.choice(directions)
                if random.randint(1, 100) <= WIDE_FALL_CHANCE:
                    d *= random.choice((1, 2))
                moveSand(allSand, i, sand, d)
                sandMoved = True

        sys.stdout.flush()
        time.sleep(PAUSE_LENGTH)

        # ⭐ Feature 2: Auto flip (reset when settled)
        if not sandMoved:
            time.sleep(1.5)
            clearSand(allSand)
            break

# ------------------ HELPERS ------------------
def moveSand(allSand, index, sand, dx):
    bext.goto(sand[X], sand[Y])
    print(' ', end='')
    new_pos = (sand[X] + dx, sand[Y] + 1)
    bext.goto(new_pos[X], new_pos[Y])
    print(SAND, end='')
    allSand[index] = new_pos

def clearSand(allSand):
    for sand in allSand:
        bext.goto(sand[X], sand[Y])
        print(' ', end='')

# ------------------ RUN ------------------
def run():
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    run()
