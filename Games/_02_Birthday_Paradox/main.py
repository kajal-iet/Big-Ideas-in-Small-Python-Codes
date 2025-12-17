import streamlit as st
import datetime
import random
import matplotlib.pyplot as plt

def run():

    # ---------------- UI STYLES (ONLY UI) ----------------
    st.markdown("""
    <style>
    .bp-container {
        max-width: 600px;
        margin: auto;
        padding: 10px;
    }
    .bp-card {
        border: 1px solid #e5e5e5;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
        background: #ffffff;
    }
    button {
        width: 100%;
        border-radius: 12px;
        font-size: 16px;
    }
    .stSlider, .stNumberInput {
        padding-top: 6px;
        padding-bottom: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="bp-container">', unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.title("🎂 Birthday Paradox — Probability Simulator")

    st.markdown("""
    Ever wondered how likely it is for two people to share the same birthday?  

    **Birthday Paradox** shows how fast probability rises — even with small groups 🎉
    """)

    # ---------------- INPUT CARD ----------------
    st.markdown('<div class="bp-card">', unsafe_allow_html=True)

    numBDays = st.number_input(
        "👥 Number of people (1–100)",
        1, 100, 23
    )

    simulations = st.number_input(
        "🔁 Simulations to run",
        100, 100000, 10000, step=100
    )

    if st.button("▶ Run Simulation"):
        birthdays = getBirthdays(numBDays)
        match = getMatch(birthdays)

        st.session_state["birthdays"] = birthdays
        st.session_state["match"] = match
        st.session_state["numBDays"] = numBDays
        st.session_state["simulations"] = simulations
        st.session_state["simMatch"] = sum(
            1 for _ in range(simulations)
            if getMatch(getBirthdays(numBDays))
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- RESULTS ----------------
    if "birthdays" in st.session_state:

        st.markdown('<div class="bp-card">', unsafe_allow_html=True)

        birthdays = st.session_state["birthdays"]
        match = st.session_state["match"]
        numBDays = st.session_state["numBDays"]
        simulations = st.session_state["simulations"]
        simMatch = st.session_state["simMatch"]

        st.subheader("🎈 Generated Birthdays")
        st.write(", ".join([f"{b.day} {b.strftime('%b')}" for b in birthdays]))

        if match:
            st.success(f"🎉 Match found on **{match.day} {match.strftime('%b')}**!")
        else:
            st.info("No matching birthdays in this simulation.")

        probability = round(simMatch / simulations * 100, 2)

        st.markdown(f"""
        **Results**
        - Simulations run: **{simulations}**
        - People per group: **{numBDays}**
        - Matches found: **{simMatch}**
        - Probability: **{probability}%**
        """)

        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------- GRAPH CARD ----------------
        st.markdown('<div class="bp-card">', unsafe_allow_html=True)
        st.subheader("📊 Probability by Group Size")

        a, b = st.slider(
            "Group size range",
            2, 100, (5, 70)
        )

        if "probabilities" not in st.session_state or st.session_state.get("last_range") != (a, b):
            st.session_state["last_range"] = (a, b)
            st.session_state["probabilities"] = calculate_probabilities(a, b)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(
            st.session_state["probabilities"]["sizes"],
            st.session_state["probabilities"]["values"]
        )
        ax.set_xlabel("Group Size")
        ax.set_ylabel("Probability of a Match")
        ax.set_title("Birthday Paradox Simulation")

        st.pyplot(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- LOGIC (UNCHANGED) ----------------
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
