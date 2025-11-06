import streamlit as st
import random
import io
import pandas as pd

def run():
    # --- Default Word Lists ---
    DEFAULT_OBJECT_PRONOUNS = ['Her', 'Him', 'Them']
    DEFAULT_POSSESIVE_PRONOUNS = ['Her', 'His', 'Their']
    DEFAULT_PERSONAL_PRONOUNS = ['She', 'He', 'They']
    DEFAULT_STATES = ['California', 'Texas', 'Florida', 'New York', 'Pennsylvania',
                    'Illinois', 'Ohio', 'Georgia', 'North Carolina', 'Michigan']
    DEFAULT_NOUNS = ['Athlete', 'Clown', 'Shovel', 'Paleo Diet', 'Doctor', 'Parent',
                    'Cat', 'Dog', 'Chicken', 'Robot', 'Video Game', 'Avocado',
                    'Plastic Straw','Serial Killer', 'Telephone Psychic']
    DEFAULT_PLACES = ['House', 'Attic', 'Bank Deposit Box', 'School', 'Basement',
                    'Workplace', 'Donut Shop', 'Apocalypse Bunker']
    DEFAULT_WHEN = ['Soon', 'This Year', 'Later Today', 'RIGHT NOW', 'Next Week']

    # --- Streamlit Sidebar: Custom Word Lists ---
    st.sidebar.header("⚙️ Customize Word Lists")

    def load_word_list(default_list, label):
        uploaded_file = st.sidebar.file_uploader(f"Upload CSV for {label}", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file, header=None)
            return df[0].dropna().tolist()
        else:
            # Editable text area
            text_area = st.sidebar.text_area(f"Edit {label}", value=", ".join(default_list))
            return [x.strip() for x in text_area.split(",") if x.strip()]

    OBJECT_PRONOUNS = load_word_list(DEFAULT_OBJECT_PRONOUNS, "Object Pronouns")
    POSSESIVE_PRONOUNS = load_word_list(DEFAULT_POSSESIVE_PRONOUNS, "Possessive Pronouns")
    PERSONAL_PRONOUNS = load_word_list(DEFAULT_PERSONAL_PRONOUNS, "Personal Pronouns")
    STATES = load_word_list(DEFAULT_STATES, "States")
    NOUNS = load_word_list(DEFAULT_NOUNS, "Nouns")
    PLACES = load_word_list(DEFAULT_PLACES, "Places")
    WHEN = load_word_list(DEFAULT_WHEN, "When")

    # --- Headline Functions ---
    def generateAreMillennialsKillingHeadline():
        noun = random.choice(NOUNS)
        return f"Are Millennials Killing the {noun} Industry?"

    def generateWhatYouDontKnowHeadline():
        noun = random.choice(NOUNS)
        pluralNoun = random.choice(NOUNS) + "s"
        when = random.choice(WHEN)
        return f"Without This {noun}, {pluralNoun} Could Kill You {when}"

    def generateBigCompaniesHateHerHeadline():
        pronoun = random.choice(OBJECT_PRONOUNS)
        state = random.choice(STATES)
        noun1 = random.choice(NOUNS)
        noun2 = random.choice(NOUNS)
        return f"Big Companies Hate {pronoun}! See How This {state} {noun1} Invented a Cheaper {noun2}"

    def generateYouWontBelieveHeadline():
        state = random.choice(STATES)
        noun = random.choice(NOUNS)
        pronoun = random.choice(POSSESIVE_PRONOUNS)
        place = random.choice(PLACES)
        return f"You Won't Believe What This {state} {noun} Found in {pronoun} {place}"

    def generateDontWantYouToKnowHeadline():
        pluralNoun1 = random.choice(NOUNS) + "s"
        pluralNoun2 = random.choice(NOUNS) + "s"
        return f"What {pluralNoun1} Don't Want You To Know About {pluralNoun2}"

    def generateGiftIdeaHeadline():
        number = random.randint(7, 15)
        noun = random.choice(NOUNS)
        state = random.choice(STATES)
        return f"{number} Gift Ideas to Give Your {noun} From {state}"

    def generateReasonsWhyHeadline():
        number1 = random.randint(3, 19)
        pluralNoun = random.choice(NOUNS) + "s"
        number2 = random.randint(1, number1)
        return f"{number1} Reasons Why {pluralNoun} Are More Interesting Than You Think (Number {number2} Will Surprise You!)"

    def generateJobAutomatedHeadline():
        state = random.choice(STATES)
        noun = random.choice(NOUNS)
        i = random.randint(0, 2)
        pronoun1 = POSSESIVE_PRONOUNS[i]
        pronoun2 = PERSONAL_PRONOUNS[i]
        if pronoun1 == 'Their':
            return f"This {state} {noun} Didn't Think Robots Would Take {pronoun1} Job. {pronoun2} Were Wrong."
        else:
            return f"This {state} {noun} Didn't Think Robots Would Take {pronoun1} Job. {pronoun2} Was Wrong."

    # --- Streamlit App ---

    st.title("📰 Clickbait Headline Generator")

    st.markdown("""
    Rules and Usage

    User inputs the number of headlines to generate.
    Using the words/uploaded csv files, headlines are generated
    1. All word lists must contain at least one element, otherwise headline generation may fail.
    2. Uploaded CSV files must have **one word per line** with no header (or a single column header is okay).
    3. Headlines are randomly generated; some may sound silly or outrageous — this is intentional.
    4. Users can regenerate headlines as many times as they like.
    5. Downloaded TXT file contains **all generated headlines** separated by line breaks.

    ---
    Word Lists
    1. OBJECT_PRONOUNS- Inserted into headlines like "Big Companies Hate [OBJECT_PRONOUNS]!"  
    2. POSSESIVE_PRONOUNS- Used in headlines to show possession, e.g., "Found in [POSSESIVE_PRONOUNS] Workplace"
    3. PERSONAL_PRONOUNS- Refers to the subject of a headline in the correct grammatical form, e.g., "They Were Wrong"
    4. STATES- Adds location context to headlines like "This [STATE] Cat Did Something Amazing"
    5. NOUNS- Main subject of headlines, e.g., "Are Millennials Killing the [NOUN] Industry?"
    6. PLACES- Adds location/place detail for headlines, e.g., "Found in [PLACE]"
    7. WHEN- Adds timing context to headlines, e.g., "Could Kill You [WHEN]"
    ---

    """)

    num_headlines = st.number_input("Number of headlines to generate", min_value=1, value=5, step=1)
    generated_headlines = []

    if st.button("Generate Headlines"):
        for _ in range(num_headlines):
            clickbaitType = random.randint(1, 8)
            if clickbaitType == 1:
                headline = generateAreMillennialsKillingHeadline()
            elif clickbaitType == 2:
                headline = generateWhatYouDontKnowHeadline()
            elif clickbaitType == 3:
                headline = generateBigCompaniesHateHerHeadline()
            elif clickbaitType == 4:
                headline = generateYouWontBelieveHeadline()
            elif clickbaitType == 5:
                headline = generateDontWantYouToKnowHeadline()
            elif clickbaitType == 6:
                headline = generateGiftIdeaHeadline()
            elif clickbaitType == 7:
                headline = generateReasonsWhyHeadline()
            elif clickbaitType == 8:
                headline = generateJobAutomatedHeadline()
            generated_headlines.append(headline)
        
        # Display Headlines
        st.markdown("### Generated Headlines")
        for h in generated_headlines:
            st.markdown(f"- {h}")
        
        # --- Download / Copy All ---
        headlines_text = "\n".join(generated_headlines)
        st.download_button(
            label="📥 Download All as TXT",
            data=headlines_text,
            file_name="clickbait_headlines.txt",
            mime="text/plain"
        )
