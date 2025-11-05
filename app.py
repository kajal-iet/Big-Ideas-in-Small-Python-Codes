import streamlit as st
from Games._01_Bagels import main as bagels
from Games._02_Birthday_Paradox import main as bdayParadox
from Games._03_BitMap_Message import main as bitmapMessage
from Games._04_BlackJack import main as blackJack
from Games._05_Bouncing_DVD_logo import main as bouncingDVD
from Games._06_Caesar_Cipher import main as caeserCipher
from Games._07_Calendar_Maker import main as calendarMaker
from Games._08_Carrot_Bluff import main as carrotBluff
from Games._09_Cho_Han import main as choHan

# -----------------------
# 🎮 MAIN APP STARTS HERE
# -----------------------
st.set_page_config(page_title="Mini Python Arcade", page_icon="🎲", layout="wide")

# Sidebar navigation
game_choice = st.sidebar.selectbox(
    "🎮 Choose a Game",
    [
        "🏠 Home",
        "🎲 Bagels",
        "🎂 Birthday Paradox",
        "🗺️ Bitmap Message",
        "🃏 BlackJack",
        "💿 Bouncing DVD Logo",
        "🔑 Caesar Cipher",
        "📅 Calendar Maker",
        "🥕 Carrot Bluff",
        "🎲 Cho Han"
    ],
)

# ------------------------------------------
# 🏠 HOME PAGE — SHOW INTRODUCTION & DETAILS
# ------------------------------------------
if game_choice == "🏠 Home":
    st.title("🎮 Tiny Python Games Hub")
    st.markdown("Welcome! Choose a game from the sidebar to start playing.")
    st.divider()

    st.subheader("📚 About this Project")
    st.write("""
    This app is a collection of mini Python games inspired by  
    *The Big Book of Small Python Projects* by **Al Sweigart**.

    Each game has been modernized and recreated as a playable web version using **Streamlit** —
    showcasing Python logic, randomness, and creative design ✨
    """)

    st.markdown("---")
    st.subheader("🎯 Games Included:")
    st.markdown("""
    - 🎲 **Bagels** — Guess the secret number  
    - 🎂 **Birthday Paradox** — Probability simulator  
    - 🗺️ **Bitmap Message** — Text-art generator  
    - 🃏 **BlackJack** — Classic 21 card game  
    - 💿 **Bouncing DVD Logo** — Nostalgic animation  
    - 🔑 **Caesar Cipher** — Encrypt, decrypt & hack messages  
    - 📅 **Calendar Maker** — Build monthly notes & to-do lists  
    - 🥕 **Carrot Bluff** — Funny bluffing game for two players
    - 🎲 **Cho Han** — Roll Dice gambling game
    """)

    st.markdown("---")
    st.caption("Made with ❤️ in Streamlit")

# ------------------------------------------
# 🎮 INDIVIDUAL GAME PAGES
# ------------------------------------------
else:
    # Hide global title for a cleaner game screen
    st.markdown(
        """
        <style>
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Load the selected game’s run function
    if game_choice == "🎲 Bagels":
        bagels.run()

    elif game_choice == "🎂 Birthday Paradox":
        bdayParadox.run()

    elif game_choice == "🗺️ Bitmap Message":
        bitmapMessage.run()

    elif game_choice == "🃏 BlackJack":
        blackJack.run()

    elif game_choice == "💿 Bouncing DVD Logo":
        bouncingDVD.run()

    elif game_choice == "🔑 Caesar Cipher":
        caeserCipher.run()

    elif game_choice == "📅 Calendar Maker":
        calendarMaker.run()

    elif game_choice == "🥕 Carrot Bluff":
        carrotBluff.run()

    elif game_choice== "🎲 Cho Han":
        choHan.run()
