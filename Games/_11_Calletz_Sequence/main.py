import streamlit as st
import pandas as pd
import time

# -----------------------------------------
# Collatz sequence function
# -----------------------------------------
def collatz_sequence(n: int):
    seq = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        seq.append(n)
    return seq


# -----------------------------------------
# Main Streamlit App
# -----------------------------------------
def run():
    st.title("🔢 Collatz Sequence Explorer")

    st.markdown("""
    The **Collatz sequence** (also called the *3n + 1 problem*) works like this:
    - If `n` is **even**, next value = `n / 2`  
    - If `n` is **odd**, next value = `3n + 1`  
    - Repeat until the value becomes **1**  

    This app helps you **generate**, **analyze**, and **compare** Collatz sequences.
    """)

    st.divider()

    # -----------------------------------------
    # Mode: Single or Compare
    # -----------------------------------------
    mode = st.radio(
        "Choose mode:",
        ["Single Sequence", "Compare Multiple Sequences"],
        horizontal=True
    )

    # ================================================================
    # ✅ SINGLE SEQUENCE MODE
    # ================================================================
    if mode == "Single Sequence":

        n = st.number_input("Enter a starting number (>0):",
                            min_value=1, value=27, step=1)

        animate = st.checkbox("Animate sequence step-by-step", value=True)

        if st.button("Generate Sequence"):
            sequence = collatz_sequence(n)

            # Animation
            if animate:
                place = st.empty()
                temp = []
                for value in sequence:
                    temp.append(value)
                    place.write(temp)
                    time.sleep(0.15)
            else:
                st.write(sequence)

            st.subheader("📊 Statistics")
            df = pd.DataFrame({
                "Value": sequence,
                "Odd / Even": ["Odd" if x % 2 else "Even" for x in sequence]
            })

            st.write(df.style.apply(
                lambda col: ["background-color:#ffd1d1" if v == "Odd" 
                             else "background-color:#d1ffd7" 
                             for v in col] 
                if col.name == "Odd / Even" else [""] * len(col),
                axis=0
            ))

            # Charts
            st.line_chart(sequence)
            st.bar_chart(sequence)

            # Stats
            st.markdown(f"**Length:** {len(sequence)} numbers")
            st.markdown(f"**Maximum value reached:** {max(sequence)}")
            st.markdown(f"**Odd values:** {sum(x % 2 for x in sequence)}")
            st.markdown(f"**Even values:** {sum(x % 2 == 0 for x in sequence)}")

            # Download TXT
            st.download_button(
                "📥 Download as TXT",
                data=", ".join(map(str, sequence)),
                file_name=f"collatz_{n}.txt",
                mime="text/plain"
            )

            # Download CSV
            csv_data = pd.DataFrame(sequence, columns=["Value"]).to_csv(index=False)
            st.download_button(
                "📥 Download as CSV",
                data=csv_data,
                file_name=f"collatz_{n}.csv",
                mime="text/csv"
            )

    # ================================================================
    # ✅ COMPARISON MODE
    # ================================================================
    else:
        st.subheader("Compare multiple Collatz sequences")

        nums = st.text_input("Enter starting numbers separated by commas (e.g., 5, 12, 27):")

        if st.button("Compare"):
            try:
                nums_list = [int(x.strip()) for x in nums.split(",") if x.strip()]

                results = []
                for num in nums_list:
                    seq = collatz_sequence(num)
                    results.append({
                        "Start": num,
                        "Length": len(seq),
                        "Max Value": max(seq)
                    })

                df_compare = pd.DataFrame(results)
                df_compare = df_compare.sort_values("Length", ascending=False)

                st.write("### 📊 Comparison Table")
                st.write(df_compare)

                st.bar_chart(df_compare.set_index("Start")["Length"])

                st.success("Comparison complete!")

            except:
                st.error("Please enter valid integers separated by commas.")
