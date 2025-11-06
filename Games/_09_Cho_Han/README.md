🎲 
## Cho-Han — The Ancient Japanese Dice Bluff
🏯 Overview

Cho-Han (丁半) is a traditional Japanese gambling game that dates back to the Edo period. Two dice are rolled inside a bamboo cup by the dealer, and players must guess whether the total is even (Cho) or odd (Han).

This digital version of Cho-Han brings the timeless floor game to life with sound effects, animation potential, and an immersive betting system — perfect for beginners learning randomness, probability, and simple math logic in Python.


## How It Works

You start with 5,000 mon (the ancient currency).
Decide how much you’d like to bet each round — or type QUIT to leave the game.
Guess whether the dice sum is:
🎎 CHO (Even) — if the total of the two dice is even
🥢 HAN (Odd) — if the total is odd
The dealer shakes the dice in a bamboo cup and reveals the outcome dramatically.
If you win, you earn double your bet — minus a small house fee.
If you lose, your bet is lost to the dealer.
Continue until you run out of mon… or your luck runs out 🍀

## Game Logic

Two six-sided dice are rolled using Python’s random.randint(1, 6)

The total is checked using % 2:

if (die1 + die2) % 2 == 0:
    result = "CHO"
else:
    result = "HAN"


Simple conditional logic decides the outcome — ideal for learning control flow and random number simulation.






## TODO List
[Done] Animate the dice roll with Streamlit emoji frames or GIFs.
[ ] Add bamboo cup shake and slam sounds using the st.audio() feature.
[ ] Use Japanese-style colors (gold, red, black) and kanji labels for “Cho” (丁) and “Han” (半).
[ ] Limit guessing time — if you don’t respond quickly, the dealer automatically decides!
[ ] Include a scoreboard box showing “Player Mon” and “House Cut”