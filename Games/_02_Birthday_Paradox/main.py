import streamlit as st
import datetime
import random
import matplotlib.pyplot as plt

def run():
    st.title("🎂 Birthday Paradox — Probability Simulator")

    st.markdown("""
    Ever wondered how likely it is for two people to share the same birthday?  
    This game simulates that famous probability puzzle — the **Birthday Paradox**! 🎉  

    **How it works:**  
    - Choose how many people are in the room.  
    - The program randomly generates birthdays for everyone.  
    - It then checks if any two birthdays match.  
    - Run multiple simulations to see how surprisingly often duplicates occur!  

    💡 *Fun fact:* With just **23 people**, there’s about a **50% chance** two share a birthday!
    """)
    st.divider()

    # --- Inputs ---
    numBDays = st.number_input("How many birthdays shall I generate? (1–100)", 1, 100, 23)
    simulations = st.number_input("How many simulations to run?", 100, 100000, 10000, step=100)

    # Button to trigger simulation
    if st.button("Run Simulation"):
        birthdays = getBirthdays(numBDays)
        match = getMatch(birthdays)

        # Store simulation results in session_state
        st.session_state["birthdays"] = birthdays
        st.session_state["match"] = match
        st.session_state["numBDays"] = numBDays
        st.session_state["simulations"] = simulations
        st.session_state["simMatch"] = sum(1 for _ in range(simulations) if getMatch(getBirthdays(numBDays)))

    # --- Show Results if simulation has already run ---
    if "birthdays" in st.session_state:
        birthdays = st.session_state["birthdays"]
        match = st.session_state["match"]
        numBDays = st.session_state["numBDays"]
        simulations = st.session_state["simulations"]
        simMatch = st.session_state["simMatch"]

        st.subheader("Generated Birthdays:")
        st.write(", ".join([f"{b.day} {b.strftime('%b')}" for b in birthdays]))

        if match:
            st.success(f"🎉 Match found on {match.day} {match.strftime('%b')}!")
        else:
            st.info("No matching birthdays in this simulation.")

        probability = round(simMatch / simulations * 100, 2)
        st.markdown(f"""
        Out of **{simulations}** simulations of **{numBDays}** people:
        - Matching birthday occurred **{simMatch} times**
        - Probability ≈ **{probability}%**
        """)

        # --- Graph with persistent state ---
        st.markdown("### 📊 Probability by Group Size")
        a, b = st.slider("Range of group sizes", 2, 100, (5, 70))

        if "probabilities" not in st.session_state or st.session_state.get("last_range") != (a, b):
            st.session_state["last_range"] = (a, b)
            st.session_state["probabilities"] = calculate_probabilities(a, b)

        fig, ax = plt.subplots()
        ax.plot(st.session_state["probabilities"]["sizes"], st.session_state["probabilities"]["values"])
        ax.set_xlabel("Group Size")
        ax.set_ylabel("Probability of a Match")
        ax.set_title("Birthday Paradox Simulation")
        st.pyplot(fig)

def calculate_probabilities(a, b):
    group_sizes = list(range(a, b))
    probabilities = []
    for group_size in group_sizes:
        match_count = 0
        for _ in range(1000):
            if getMatch(getBirthdays(group_size)):
                match_count += 1
        probabilities.append(match_count / 1000)
    return {"sizes": group_sizes, "values": probabilities}

def getBirthdays(num):
    start = datetime.date(2001, 1, 1)
    birthdays = [start + datetime.timedelta(random.randint(0, 364)) for _ in range(num)]
    return birthdays

def getMatch(birthdays):
    seen = set()
    for b in birthdays:
        if b in seen:
            return b
        seen.add(b)
    return None
