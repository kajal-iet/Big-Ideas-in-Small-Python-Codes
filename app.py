import streamlit as st

# -----------------------
# 🎮 GAME IMPORTS
# -----------------------
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
from Games._13_CountDown import main as countDown
from Games._15_Diamond import main as diamondGen
from Games._16_Dice_math import main as mathQuiz
from Games._17_Dice_Roller import main as diceRoll
from Games._18_Digital_stream import main as digStream
from Games._19_DNA_visualization import main as dnaVis
from Games._20_Ducklings import main as ducklings
from Games._22_Factor_Finder import main as factorFinder
from Games._23_Fast_Draw import main as fastDraw
from Games._24_Fibonacci import main as fibonacci
from Games._25_Fish_Tank import main as fishTank
from Games._26_Flooder import main as flooder
from Games._27_Forest_SIre_SIm import main as forestFire
from Games._28_Four_in_a_row import main as fourInaRow
from Games._29_Guess_Number import main as guessNum
from Games._30_Gullible import main as gullible
from Games._31_Hacking_Minigame import main as hacking
from Games._32_Hangman_Guillotine import main as hangman
from Games._33_HexGrid import main as hexgrid
from Games._34_HourGlass import main as hourglass
from Games._35_Hungry_Robots import main as robots
from Games._36_Pig_Latin import main as pigLatin
from Games._37_JAccuse import main as jaccuse
from Games._38_Langtons_Ant import main as langtonsAnt


# -----------------------
# ⚙️ PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Tiny Python Arcade",
    page_icon="🎮",
    layout="wide"
)

# -----------------------
# 🧠 SESSION STATE
# -----------------------
if "active_game" not in st.session_state:
    st.session_state.active_game = None


# -----------------------
# 🎯 GAME REGISTRY
# -----------------------
GAMES = [
    {"id": "bagels", "emoji": "🎲", "name": "Bagels", "desc": "Guess the secret number", "run": bagels.run},
    {"id": "birthday", "emoji": "🎂", "name": "Birthday Paradox", "desc": "Probability simulation", "run": bdayParadox.run},
    {"id": "bitmap", "emoji": "🗺️", "name": "Bitmap Message", "desc": "Text art generator", "run": bitmapMessage.run},
    {"id": "blackjack", "emoji": "🃏", "name": "BlackJack", "desc": "Classic 21 card game", "run": blackJack.run},
    {"id": "dvd", "emoji": "💿", "name": "Bouncing DVD Logo", "desc": "Retro animation", "run": bouncingDVD.run},
    {"id": "caesar", "emoji": "🔑", "name": "Caesar Cipher", "desc": "Encrypt and decrypt messages", "run": caeserCipher.run},
    {"id": "calendar", "emoji": "📅", "name": "Calendar Maker", "desc": "Build calendars & notes", "run": calendarMaker.run},
    {"id": "carrot", "emoji": "🥕", "name": "Carrot Bluff", "desc": "Funny bluffing game", "run": carrotBluff.run},
    {"id": "chohan", "emoji": "🎲", "name": "Cho Han", "desc": "Dice gambling game", "run": choHan.run},
    {"id": "clickbait", "emoji": "📢", "name": "Clickbait Headlines", "desc": "Generate viral headlines", "run": headlinesGen.run},
    {"id": "collatz", "emoji": "🔢", "name": "Collatz Sequence", "desc": "Explore 3n + 1", "run": collatz.run},
    {"id": "countdown", "emoji": "⏱️", "name": "Countdown Timer", "desc": "Track productivity", "run": countDown.run},
    {"id": "diamond", "emoji": "💎", "name": "Animated Diamonds", "desc": "Rotating diamond art", "run": diamondGen.run},
    {"id": "dice_math", "emoji": "🎲", "name": "Dice Math", "desc": "Dice sum quiz", "run": mathQuiz.run},
    {"id": "dice_roll", "emoji": "🐉", "name": "Dice Roller", "desc": "DnD style roller", "run": diceRoll.run},
    {"id": "matrix", "emoji": "💻", "name": "Matrix Rain", "desc": "Hacker animation", "run": digStream.run},
    {"id": "dna", "emoji": "🧬", "name": "DNA Visualization", "desc": "Visualize DNA strands", "run": dnaVis.run},
    {"id": "ducklings", "emoji": "🐥", "name": "Ducklings", "desc": "Cute terminal animation", "run": ducklings.run},
    {"id": "fibonacci", "emoji": "🌀", "name": "Fibonacci", "desc": "Sequence generator", "run": fibonacci.run},
    {"id": "fastdraw", "emoji": "🤠", "name": "Fast Draw", "desc": "Test your reflexes", "run": fastDraw.run},
    {"id": "factor", "emoji": "🔢", "name": "Factor Finder", "desc": "Analyze numbers", "run": factorFinder.run},
    {"id": "fish", "emoji": "🐟", "name": "Fish Tank", "desc": "Aquarium simulation", "run": fishTank.run},
    {"id": "flooder", "emoji": "🎨", "name": "Flooder", "desc": "Color puzzle game", "run": flooder.run},
    {"id": "forest", "emoji": "🌲🔥", "name": "Forest Fire", "desc": "Fire spread simulation", "run": forestFire.run},
    {"id": "fourinarow", "emoji": "🎮", "name": "Four in a Row", "desc": "Connect four game", "run": fourInaRow.run},
    {"id": "guess", "emoji": "📱", "name": "Guess Number", "desc": "Find the secret number", "run": guessNum.run},
    {"id": "gullible", "emoji": "😄", "name": "Gullible", "desc": "Prank game", "run": gullible.run},
    {"id": "hacking", "emoji": "🖥️", "name": "Hacking Minigame", "desc": "Crack the code", "run": hacking.run},
    {"id": "hangman", "emoji": "🪓", "name": "Hangman Guillotine", "desc": "Guess before doom", "run": hangman.run},
    {"id": "hexgrid", "emoji": "✏️", "name": "HexGrid", "desc": "Carpet design", "run": hexgrid.run},
    {"id": "hourglass", "emoji": "⏳", "name": "Hourglass", "desc": "Time visualization", "run": hourglass.run},
    {"id": "robots", "emoji": "🤖", "name": "Hungry Robots", "desc": "Robot eats robot", "run": robots.run},
    {"id": "piglatin", "emoji": "🐷", "name": "Pig Latin", "desc": "Language fun", "run": pigLatin.run},
    {"id": "jaccuse", "emoji": "🕵️", "name": "J’ACCUSE!", "desc": "Mystery deduction game", "run": jaccuse.run},
    {"id": "langton", "emoji": "🐜", "name": "Langton’s Ant", "desc": "Emergent behavior", "run": langtonsAnt.run},
]


# -----------------------
# 🎨 GLOBAL STYLES
# -----------------------
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
button {
    width: 100%;
    border-radius: 14px;
}
.game-card {
    border: 1px solid #e6e6e6;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    margin-bottom: 18px;
    background: white;
            
}
.game-title {
    font-size: 20px;
    font-weight: 600;
    color: #000000;
}
.game-desc {
    color: #666;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------
# 🏠 HOME PAGE
# -----------------------
def home_page():
    st.title("🎮 Tiny Python Arcade")
    st.caption("Tap a game card to start playing")

    cols = st.columns(2 if st.session_state.get("is_mobile", False) else 3)

    for i, game in enumerate(GAMES):
        with cols[i % len(cols)]:
            st.markdown(
                f"""
                <div class="game-card">
                    <div class="game-title">{game['emoji']} {game['name']}</div>
                    <div class="game-desc">{game['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"▶ Play", key=game["id"]):
                st.session_state.active_game = game
                st.rerun()


# -----------------------
# 🎮 GAME PAGE
# -----------------------
def game_page(game):
    st.button("⬅ Back to Home", on_click=lambda: go_home())
    st.divider()
    game["run"]()


def go_home():
    st.session_state.active_game = None


# -----------------------
# 🚀 APP ENTRY
# -----------------------
if st.session_state.active_game is None:
    home_page()
else:
    game_page(st.session_state.active_game)
