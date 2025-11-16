import streamlit as st
import math


# ------------------------------------------------------
# MAIN APP FUNCTION
# ------------------------------------------------------
def run():
    st.set_page_config(page_title="Factor Finder", layout="centered")

    st.title("🔢 Factor Finder — Number Analyzer")

    st.write("""
    Enter any **positive integer** and instantly see all its factors.

    ### ✅ Innovative Features Added
    - **Prime Badge:** Instant prime/composite detection  
    - **Factor Chart:** Visualizes all factors on a number line

    """)

    # -------------------------
    # INPUT
    # -------------------------
    n = st.number_input("Enter a positive whole number:", min_value=1, step=1)

    if st.button("Find Factors"):
        st.write("---")
        st.header(f"🧮 Factors of {n}")

        # -------------------------
        # FIND FACTORS
        # -------------------------
        factors = set()
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                factors.add(i)
                factors.add(n // i)

        factors = sorted(list(factors))

        st.code(", ".join(str(x) for x in factors))

        # -------------------------
        # PRIME BADGE
        # -------------------------
        st.write("### 🏷 Number Type")

        if len(factors) == 2:
            st.success("✅ **Prime Number**")
        else:
            st.info("🔷 **Composite Number**")

        # -------------------------
        # FACTOR CHART VISUALIZATION
        # -------------------------
        st.write("---")
        st.write("### 📊 Factor Chart")

        chart_data = {"factor": factors}
        st.bar_chart(chart_data)


if __name__ == "__main__":
    run()
