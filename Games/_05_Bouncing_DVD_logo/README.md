## Bouncing DVD Logo
💡 Overview

If you grew up in the DVD era, you’ll remember those idle screens showing a colorful DVD logo bouncing around the screen, changing direction whenever it hit an edge.
This Python program recreates that nostalgic animation — complete with color changes and corner-hit counting — using the bext module for terminal-based graphics.


##  How It Works

Each DVD logo’s position is tracked using Cartesian coordinates:

x → horizontal position (increases to the right)

y → vertical position (increases downward)

The origin (0, 0) starts at the top-left corner of your terminal.

The program moves the logo diagonally across the screen, bouncing off edges when it reaches the boundaries.

Every time a logo hits a corner, a counter increments — those moments are rare and satisfying to watch!

Each logo is represented internally by a Python dictionary:

{
  'color': 'blue',
  'direction': 'ur',  # up-right, down-right, down-left, or up-left
  'x': 10,
  'y': 5
}


The bext.goto(x, y) function positions the logo in the terminal window at those coordinates.



##  Concepts Demonstrated

Coordinate system & screen mapping

Real-time terminal animation

Dictionary-based state tracking

Collision detection and direction reversal

Counting corner hits

##  Example Output

When you run the program, you’ll see multiple DVD logos moving diagonally, bouncing off walls, and changing colors — similar to this illustration:

╔════════════════════════════════╗
║    🟪 DVD                      ║
║                                ║
║                     🟨 DVD     ║
║                                ║
║          🟥 DVD                ║
╚════════════════════════════════╝


## TODO list

Multiple Logo Types
[ ] Instead of just “DVD”, allow users to pick custom text/logos (e.g., their name, emojis, etc.)

Trailing Effect
[ ] Keep a faint trail behind the moving logo (like a comet tail). You can simulate persistence by re-drawing slightly faded text for old positions.

Keyboard Control
[ ] Let user press keys to increase/decrease speed, pause animation, or add more logos live.

Live Corner Hit Stats
[ ] Display a stats dashboard: total corner hits, total bounces, active logos, etc.


Collision Sound (ASCII)
[ ] Each time the logo hits an edge or corner, print a funny message like “Oof!” or “Perfect Corner Hit!”.
