# Overview

Conway’s Game of Life is a zero-player cellular automaton created by mathematician John Conway in 1970.
It is a simulation in which simple rules applied to a grid of cells produce incredibly complex, emergent patterns.

Each cell is either alive or dead, and the grid evolves step-by-step based entirely on its current state—no memory, no randomness after initialization.

Despite the simplicity, the Game of Life is Turing complete, capable of modeling computation, logic gates, self-replicating systems, oscillators, gliders, and even digital universes.

This project provides a Python implementation of the Game of Life using dictionaries and coordinate tuples to represent the grid state.


TODO List (Practical & Interesting Enhancements)

[ ] Let the user adjust grid size (WIDTH, HEIGHT).

[ ] Let the user set the percentage of starting alive cells instead of 50%.

[ ] Allow loading a custom starting grid from a text file.

[ ] Add preset patterns (Glider, Pulsar, Gosper Glider Gun).

[ ]Add color-based visualization (alive = green, dead = black).

Add a GUI or Streamlit version with:

[ ] click-to-toggle cells

[ ] play/pause/step buttons

[ ] speed control slider

[ ] Show statistics (alive cell count, generation number).
