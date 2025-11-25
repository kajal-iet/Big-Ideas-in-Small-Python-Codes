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
from Games._10_Clickbait_Headline_Gen import main as headlinesGen
from Games._11_Calletz_Sequence import main as collatz
# from Games._12_Conways_Game import main as conwaysGame
from Games._13_CountDown import main as countDown
# from Games._14_DeepCave import main as deepCave
from Games._15_Diamond import main as diamondGen
from Games._16_Dice_math import main as Mathquiz
from Games._17_Dice_Roller import main as diceRoll
from Games._18_Digital_stream import main as digStream
from Games._19_DNA_visualization import main as dnaVis
from Games._20_Ducklings import main as ducklings
from Games._21_Etching_drawer import main as etching
from Games._22_Factor_Finder import main as factorFinder
from Games._23_Fast_Draw import main as fastDraw
from Games._24_Fibonacci import main as fibonacci
from Games._25_Fish_Tank import main as fishTank
from Games._26_Flooder import main as flooder
from Games._27_Forest_SIre_SIm import main as forestSireSim
from Games._28_Four_in_a_row import main as fourInaRow


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
        "🎲 Cho Han",
        "📢 Clickbait Headlines",
        "🔢 Collatz Sequence Explore",
        # "🧬 Conway’s Game of Life",
        "⏱ Countdown Timer",
        # "🕳️ Deep Cave",
        "💎 Animated Diamonds",
        "🎲 Dice Math",
        "🐉 Dice Roller",
        "💻 Matrix Digital Rain",
        "🧬 DNA Visualization",
        "🐥 Ducklings",
        "🌀 Fibonacci",
        "🤠 Fast Draw",
        "🔢 Factor Finder",
        # "🎨 Etching Drawer",
        "🐟 Fish Tank",
        "🎨 Flooder",
        "🌲🔥 Forest Fire Simulation"
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
    - 📢 **Clickbait Headlines**- Generates headlines based on your chosen words
    - 🔢 **Collatz Sequence Explore**- also called 3n+1 problem
    # - 🧬 **Conway’s Game of Life**- cell multiplication simulator
    - ⏱ **Countdown Timer**- Allows you to track productivity
    # - 🕳️ **Deep Cave** – Tunnel Dodger mechanics
    - 💎 **Animated Diamonds** - Generate rotating and pulsating diamonds
    - 🎲 **Dice Math** Quiz to guess dice nu,bers sum on screen
    - 🐉 **Dice Roller** Inspired from dungeons and dragons
    - 💻 **Matrix Digital Rain** Gives hacker visualization
    - 🧬 **DNA Visualization**,
    - 🌀 **Fibonacci** Sequence Generator
    - 🤠 **Fast Draw** Reflex Tester
    - 🔢 **Factor Finder** - Number Analyzer
    # - 🎨 **Etching Drawer** - draws with lines,
    - 🎨 **Flooder**- puzzle game,
    - 🌲🔥 **Forest Fire Simulation **

                
    """)

    st.markdown("---")
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
    
    elif game_choice== "📢 Clickbait Headlines":
        headlinesGen.run()

    elif game_choice=="🔢 Collatz Sequence Explore":
        collatz.run()

    # elif game_choice=="🧬 Conway’s Game of Life":
    #     conwaysGame.run()

    elif game_choice== "⏱ Countdown Timer":
        countDown.run()

    # elif game_choice=="🕳️ Deep Cave":
    #     deepCave.run()

    elif game_choice=="💎 Animated Diamonds":
        diamondGen.run()

    elif game_choice=="🎲 Dice Math":
        Mathquiz.run()

    elif game_choice=="🐉 Dice Roller":
        diceRoll.run()

    elif game_choice=="💻 Matrix Digital Rain":
        digStream.run()

    elif game_choice=="🧬 DNA Visualization":
        dnaVis.run()

    elif game_choice=="🐥 Ducklings":
        ducklings.run()

    elif game_choice=="🌀 Fibonacci":
        fibonacci.run()

    elif game_choice=="🤠 Fast Draw":
        fastDraw.run()
    
    elif game_choice=="🔢 Factor Finder":
        factorFinder.run()

    # elif game_choice=="🎨 Etching Drawer":
    #     etching.run()
    
    elif game_choice=="🐟 Fish Tank":
        fishTank.run()

    elif game_choice=="🎨 Flooder":
        flooder.run()

    elif game_choice=="🌲🔥 Forest Fire Simulation":
        forestSireSim.run()
        

  

    
