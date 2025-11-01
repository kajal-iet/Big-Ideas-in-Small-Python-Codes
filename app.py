import streamlit as st
from Games._01_Bagels import main as bagels
from Games._02_Birthday_Paradox import main as bdayParadox
from Games._03_BitMap_Message import main as bitmapMessage

# -----------------------
# 🎮 MAIN APP STARTS HERE
# -----------------------
st.set_page_config(page_title="Mini Python Arcade", page_icon="🎲", layout="wide")

st.title("🎮 Tiny Python Games Hub")
st.markdown("Welcome! Choose a game below to play:")

# Sidebar navigation
game_choice = st.sidebar.selectbox(
    "Select a game",
    ["🏠 Home", "🎲 Bagels", "🎂 Birthday Paradox", "🗺️ Bitmap Message"]
)



# Display game based on user selection
if game_choice == "🏠 Home":
    st.subheader("About this project")
    st.write("""
    This app is a collection of mini Python games inspired by *The Big Book of Small Python Projects* by Al Sweigart.
    I’ve recreated and modernized them into playable web versions using **Streamlit**.
    
    Try each game from the sidebar to experience logic, randomness, and ASCII fun — all coded in Python!
    """)
    st.markdown("---")
    st.markdown("#### 📚 Games Included:")
    st.markdown("- 🎲 Bagels(guess number))")
    st.markdown("- 🎂 Birthday Paradox (probability simulator)")
    st.markdown("- 🗺️ Bitmap Message (text-art generator)")
    st.markdown("- 🔢 Guess the Number (classic number guessing)")

elif game_choice == "🎲 Bagels":
    bagels.run()

elif game_choice == "🎂 Birthday Paradox":
    bdayParadox.run()

elif game_choice == "🗺️ Bitmap Message":
    bitmapMessage.run()
