# 🎲 Dice Roller

**Dice Roller** is a simple and flexible dice-rolling simulator based on classic
tabletop RPG notation such as **3d6**, **1d10+2**, or **2d38-1**.  
It supports traditional dice (d4, d6, d8, d10, d20) as well as any custom number
of sides, even imaginary dice like **d38** or **d1000**.

The program parses user input, validates the format, rolls the dice using
`random.randint()`, applies optional modifiers, and displays both the total and
the individual roll results.

---

## ✅ Features

- Supports standard RPG dice notation:  
  - `XdY` → roll X dice with Y sides  
  - `XdY+N` → add modifier  
  - `XdY-N` → subtract modifier
- Rolls **any number** of dice with **any number of sides**.
- Displays:
  - Total result  
  - Individual roll results  
  - Modifier used (if any)
- Detects invalid input and guides the user to correct the format.
- Quit anytime by typing **QUIT**.

---

## ✅ Example Usage

3d6
7 (3, 2, 2)

1d10+2
9 (7, +2)

2d38-1
32 (20, 13, -1)

yaml
Copy code

---

## ✅ How It Works

The program breaks down user input into three components:

1. **Number of dice** (before the `d`)
2. **Number of sides** (after the `d`)
3. **Optional modifier** (`+N` or `-N`)


# TODO List

[Done] Roll: d17, d100, d999, d10000
No physical dice app lets you do that easily.

[DOne] You vs Computer, both roll- highest wins, best of 5

[ ] Shared multiplayer rooms

[Done] "Roll again" quick button

[ ] Graphical dice images
