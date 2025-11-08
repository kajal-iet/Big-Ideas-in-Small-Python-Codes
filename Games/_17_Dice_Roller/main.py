import streamlit as st
import random


def run():
    st.title("🎲 Dice Roller – Streamlit Edition")

    st.write("""
Use RPG dice notation:

- **3d6**, **1d10+2**, **2d38-1**
- Works with ANY dice: `d17`, `d100`, `d999`, `d10000`
- Type **QUIT** to exit
""")

    # -----------------------------------------------------------
    # Session state for Quick Dice & Battle Mode
    # -----------------------------------------------------------
    if "dice_input_value" not in st.session_state:
        st.session_state.dice_input_value = ""

    if "battle_user_score" not in st.session_state:
        st.session_state.battle_user_score = 0
        st.session_state.battle_cpu_score = 0
        st.session_state.battle_round = 0

    if "last_total" not in st.session_state:
        st.session_state.last_total = None

    # -----------------------------------------------------------
    # Quick Roll Buttons (d17, d100, d999, d10000)
    # -----------------------------------------------------------
    st.subheader("✨ Quick Dice Shortcuts")

    col1, col2, col3, col4 = st.columns(4)

    if col1.button("Roll d17"):
        st.session_state.dice_input_value = "1d17"
        st.rerun()

    if col2.button("Roll d100"):
        st.session_state.dice_input_value = "1d100"
        st.rerun()

    if col3.button("Roll d999"):
        st.session_state.dice_input_value = "1d999"
        st.rerun()

    if col4.button("Roll d10000"):
        st.session_state.dice_input_value = "1d10000"
        st.rerun()

    # -----------------------------------------------------------
    # Dice input box (pre-filled if quick button was used)
    # -----------------------------------------------------------
    diceStr = st.text_input("Enter dice expression:",
                            value=st.session_state.dice_input_value,
                            key="dice_input_box")

    # -----------------------------------------------------------
    # MAIN ROLL BUTTON
    # -----------------------------------------------------------
    if st.button("Roll"):
        user_total = process_roll(diceStr)

        if user_total is not None:
            st.session_state.last_total = user_total

    # -----------------------------------------------------------
    # ROLL AGAIN BUTTON
    # -----------------------------------------------------------
    if st.session_state.dice_input_value:
        if st.button("🔁 Roll Again"):
            user_total = process_roll(st.session_state.dice_input_value)
            if user_total is not None:
                st.session_state.last_total = user_total

    # -----------------------------------------------------------
    # YOU VS COMPUTER (Uses your exact dice expression)
    # -----------------------------------------------------------
    st.divider()
    st.subheader("🤖 You vs Computer — Best of 5 (using YOUR dice)")

    st.write(f"**Round:** {st.session_state.battle_round} / 5")
    st.write(f"**Score:** You {st.session_state.battle_user_score} – {st.session_state.battle_cpu_score} Computer")

    if st.button("Play Round with My Dice"):
        if not diceStr:
            st.error("Enter a valid dice expression first!")
        else:
            # User roll
            user_total = process_roll(diceStr, display=False)

            if user_total is None:
                st.error("Invalid dice format!")
                return

            # Computer roll (same expression)
            cpu_total = process_roll(diceStr, display=False)

            st.write(f"🎲 **Your total:** {user_total}")
            st.write(f"🤖 **Computer total:** {cpu_total}")

            # Update round count
            st.session_state.battle_round += 1

            # Determine winner
            if user_total > cpu_total:
                st.session_state.battle_user_score += 1
                st.success("✅ You win this round!")
            elif cpu_total > user_total:
                st.session_state.battle_cpu_score += 1
                st.error("❌ Computer wins this round!")
            else:
                st.warning("⚠️ Draw — no points.")

            # End match after 5 rounds
            if st.session_state.battle_round >= 5:
                st.subheader("🏁 Final Result")
                if st.session_state.battle_user_score > st.session_state.battle_cpu_score:
                    st.success("🏆 YOU WIN THE MATCH!")
                elif st.session_state.battle_cpu_score > st.session_state.battle_user_score:
                    st.error("💀 COMPUTER WINS THE MATCH!")
                else:
                    st.warning("🤝 It's a tie!")

                # Reset
                st.session_state.battle_round = 0
                st.session_state.battle_user_score = 0
                st.session_state.battle_cpu_score = 0


# ======================================================================
# FUNCTION: Process Dice Roll (Original logic kept)
# ======================================================================
def process_roll(diceStr, display=True):
    try:
        if diceStr.upper() == "QUIT":
            st.success("Thanks for playing!")
            st.stop()

        original_input = diceStr
        clean = diceStr.lower().replace(" ", "")

        # Parse:
        dIndex = clean.find("d")
        if dIndex == -1:
            raise Exception('Missing the "d" character.')

        numDice = clean[:dIndex]
        if not numDice.isdecimal():
            raise Exception('Missing the number of dice.')
        numDice = int(numDice)

        # Modifier
        modIndex = clean.find("+")
        if modIndex == -1:
            modIndex = clean.find("-")

        # Sides
        if modIndex == -1:
            numSides = clean[dIndex + 1:]
        else:
            numSides = clean[dIndex + 1:modIndex]

        if not numSides.isdecimal():
            raise Exception("Missing number of sides.")
        numSides = int(numSides)

        # Modifier amount
        if modIndex == -1:
            modAmount = 0
        else:
            modAmount = int(clean[modIndex + 1:])
            if clean[modIndex] == "-":
                modAmount = -modAmount

        # Rolls
        rolls = [random.randint(1, numSides) for _ in range(numDice)]
        total = sum(rolls) + modAmount

        # Display
        if display:
            st.subheader("🎯 Result")
            st.write(f"**Input:** `{original_input}`")
            st.write(f"**Total:** `{total}`")
            st.write(f"**Rolls:** `{', '.join(str(r) for r in rolls)}`")

            if modAmount != 0:
                sign = "+" if modAmount > 0 else "-"
                st.write(f"**Modifier:** `{sign}{abs(modAmount)}`")

        return total

    except Exception as exc:
        if display:
            st.error("❌ Invalid input. Use `3d6`, `1d10+2`, etc.")
            st.write(f"Reason: {exc}")
        return None
