"""
Bouncing DVD Logo
A bouncing DVD logo animation. You have to be "of a certain age" to
appreciate this. Press Ctrl-C to stop.

NOTE: Do not resize the terminal window while this program is running.
This code is available at https://nostarch.com/big-book-small-python-programming
Tags: short, artistic, bext

"""

import sys, random, time

try:
    import bext
except ImportError:
    print('This program requires the bext module, which you')
    print('can install by following the instructions at')
    print('https://pypi.org/project/Bext/')
    sys.exit()

# Set up the constants:
WIDTH, HEIGHT = bext.size()
# We can't print to the last column on Windows without it adding a
# newline automatically, so reduce the width by one:
WIDTH -= 1

NUMBER_OF_LOGOS = 1  # (!) Try changing this to 1 or 100.
PAUSE_AMOUNT = 0.2  # (!) Try changing this to 1.0 or 0.0.
# (!) Try changing this list to fewer colors:
COLORS = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

UP_RIGHT   = 'ur'
UP_LEFT    = 'ul'
DOWN_RIGHT = 'dr'
DOWN_LEFT  = 'dl'
DIRECTIONS = (UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT)

# Key names for logo dictionaries:
COLOR = 'color'
X = 'x'
Y = 'y'
DIR = 'direction'


# Custom logo text(s):
LOGO_TEXTS = ['DVD', '💿', 'KP', '⭐']  # (!) You can edit or input your own


def main():
    bext.clear()

    logos = []
    for i in range(NUMBER_OF_LOGOS):
        text = random.choice(LOGO_TEXTS)
        logos.append({
            COLOR: random.choice(COLORS),
            X: random.randint(1, WIDTH - len(text)),
            Y: random.randint(1, HEIGHT - 4),
            DIR: random.choice(DIRECTIONS),
            'text': text
        })

    cornerBounces = 0

    while True:
        for logo in logos:
            # Erase current logo
            bext.goto(max(0, logo[X]), max(0, logo[Y]))
            print(' ' * len(logo['text']), end='')

            originalDirection = logo[DIR]

            # Handle corner and wall bounces:
            if logo[X] <= 0 and logo[Y] <= 0:
                logo[DIR] = DOWN_RIGHT
                cornerBounces += 1
            elif logo[X] <= 0 and logo[Y] >= HEIGHT - 1:
                logo[DIR] = UP_RIGHT
                cornerBounces += 1
            elif logo[X] >= WIDTH - len(logo['text']) and logo[Y] <= 0:
                logo[DIR] = DOWN_LEFT
                cornerBounces += 1
            elif logo[X] >= WIDTH - len(logo['text']) and logo[Y] >= HEIGHT - 1:
                logo[DIR] = UP_LEFT
                cornerBounces += 1

            # Bounce from edges
            elif logo[X] <= 0 and logo[DIR] in (UP_LEFT, DOWN_LEFT):
                logo[DIR] = UP_RIGHT if logo[DIR] == UP_LEFT else DOWN_RIGHT
            elif logo[X] >= WIDTH - len(logo['text']) and logo[DIR] in (UP_RIGHT, DOWN_RIGHT):
                logo[DIR] = UP_LEFT if logo[DIR] == UP_RIGHT else DOWN_LEFT
            elif logo[Y] <= 0 and logo[DIR] in (UP_LEFT, UP_RIGHT):
                logo[DIR] = DOWN_LEFT if logo[DIR] == UP_LEFT else DOWN_RIGHT
            elif logo[Y] >= HEIGHT - 1 and logo[DIR] in (DOWN_LEFT, DOWN_RIGHT):
                logo[DIR] = UP_LEFT if logo[DIR] == DOWN_LEFT else UP_RIGHT

            # Change color when direction changes
            if logo[DIR] != originalDirection:
                logo[COLOR] = random.choice(COLORS)

            # Move logo
            if logo[DIR] == UP_RIGHT:
                logo[X] += 2; logo[Y] -= 1
            elif logo[DIR] == UP_LEFT:
                logo[X] -= 2; logo[Y] -= 1
            elif logo[DIR] == DOWN_RIGHT:
                logo[X] += 2; logo[Y] += 1
            elif logo[DIR] == DOWN_LEFT:
                logo[X] -= 2; logo[Y] += 1

            # ✅ Clamp values to stay in valid range
            logo[X] = max(0, min(WIDTH - len(logo['text']), logo[X]))
            logo[Y] = max(0, min(HEIGHT - 1, logo[Y]))

        # Show stats
        bext.goto(5, 0)
        bext.fg('white')
        print('Corner bounces:', cornerBounces, end='')

        # Draw all logos
        for logo in logos:
            bext.goto(max(0, logo[X]), max(0, logo[Y]))
            bext.fg(logo[COLOR])
            print(logo['text'], end='')

        bext.goto(0, 0)
        sys.stdout.flush()
        time.sleep(PAUSE_AMOUNT)

# If this program was run (instead of imported), run the game:
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('Bouncing DVD Logo, by Al Sweigart')
        sys.exit()  # When Ctrl-C is pressed, end the program.