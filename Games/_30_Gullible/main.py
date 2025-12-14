import streamlit as st

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Gullible",
    layout="centered"
)

def run():
    st.title("😄 Gullible")
    st.caption("Inspired by Al Sweigart — Big Book of Small Python Projects")

    st.markdown("""
    **Do you want to know how to keep a gullible person busy for hours?**  
    (Type **yes / y** or **no / n**)
    """)

    # ------------------ SESSION STATE ------------------
    if "yes_count" not in st.session_state:
        st.session_state.yes_count = 0
        st.session_state.finished = False
        st.session_state.message = ""

    # ------------------ INPUT ------------------
    response = st.text_input("Your response:", placeholder="y / n / yes / no")

    if st.button("Submit") and not st.session_state.finished:
        cleaned = response.strip().lower()

        if cleaned in ("n", "no"):
            st.session_state.finished = True

        elif cleaned in ("y", "yes"):
            st.session_state.yes_count += 1

            # Smart message every 5 yeses
            if st.session_state.yes_count % 5 == 0:
                st.session_state.message = "😄 Still waiting... aren’t you curious?"
            else:
                st.session_state.message = ""

        else:
            st.session_state.message = f'"{response}" is not a valid yes/no response.'

    # ------------------ OUTPUT ------------------
    if st.session_state.finished:
        st.success("Thank you. Have a nice day! 😊")
        st.info(f"🧮 You said **YES** {st.session_state.yes_count} times.")
    else:
        st.write("Do you want to know how to keep a gullible person busy for hours? Y/N")
        if st.session_state.message:
            st.warning(st.session_state.message)


# ------------------ RUN ------------------
if __name__ == "__main__":
    run()
