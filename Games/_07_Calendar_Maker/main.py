import streamlit as st
import datetime
import json
import os

# --- CONSTANTS ---
DAYS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December')

NOTES_FILE = "calendar_notes.json"

# --- Load or create notes storage ---
if os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "r") as f:
        notes_data = json.load(f)
else:
    notes_data = {}


def CalendarMaker(year, month, notes_data):
    today = datetime.date.today()
    calText = f"### {MONTHS[month - 1]} {year}\n\n"
    calText += '| Sun | Mon | Tue | Wed | Thu | Fri | Sat |\n'
    calText += '|-----|-----|-----|-----|-----|-----|-----|\n'

    # Start from Sunday before or on the 1st of the month
    currentDate = datetime.date(year, month, 1)
    while currentDate.weekday() != 6:  # 6 = Sunday
        currentDate -= datetime.timedelta(days=1)

    # Determine the last date to draw (Saturday of the last week that includes month-end)
    next_month = month + 1 if month < 12 else 1
    next_month_year = year if month < 12 else year + 1
    end_of_month = datetime.date(next_month_year, next_month, 1) - datetime.timedelta(days=1)
    last_display_date = end_of_month + datetime.timedelta(days=(5 - end_of_month.weekday()) % 7 + 1)

    while currentDate <= last_display_date:
        week_row = []
        for _ in range(7):
            cell_date = currentDate
            date_key = str(cell_date)

            # Out-of-month days in gray
            if cell_date.month != month:
                day_str = f"<span style='color:#aaa'>{cell_date.day}</span>"
                note_display = ""
            else:
                # Highlight today
                if cell_date == today:
                    day_str = (
                        f"<span style='background:#2563eb;color:white;"
                        f"padding:2px 6px;border-radius:6px;font-weight:bold;'>"
                        f"[{cell_date.day}]</span>"
                    )
                else:
                    day_str = f"**{cell_date.day}**"

                # Add note if exists
                note_display = f"<br><sub>{notes_data.get(date_key, '')}</sub>" if date_key in notes_data else ""

            week_row.append(f"{day_str}{note_display}")
            currentDate += datetime.timedelta(days=1)

        calText += '| ' + ' | '.join(week_row) + ' |\n'

    return calText


def run():
    st.set_page_config(
    page_title="Responsive App",
    layout="centered",
    initial_sidebar_state="collapsed"
    )
    st.title("📅 Smart Calendar with Notes")

    st.markdown("""
    Create and customize your own **monthly calendar** with ease!  

    ✨ Features:
    - Choose **any month and year**
    - Add custom **events, notes, or holidays**
    - Download or display your calendar in a clean layout
    - Fully resets when restarted for a fresh start each time  

    🧭 Perfect for quick planning, journaling, or just keeping things organized.
    """)

    # User input for month and year
    year = st.number_input("Enter year:", min_value=1, max_value=9999, value=datetime.date.today().year)
    month = st.selectbox("Select month:", list(range(1, 13)), format_func=lambda x: MONTHS[x - 1])

    # Automatically draw calendar after user input
    st.markdown(CalendarMaker(year, month, notes_data), unsafe_allow_html=True)

    st.divider()
    st.subheader("✏️ Add or Edit Notes")

    # Pick a date within the chosen month
    note_date = st.date_input("Select date:", datetime.date(year, month, 1))
    note_text = st.text_area("Your note:", value=notes_data.get(str(note_date), ""))

    if st.button("💾 Save Note"):
        notes_data[str(note_date)] = note_text.strip()
        with open(NOTES_FILE, "w") as f:
            json.dump(notes_data, f, indent=2)
        st.success(f"Note saved for {note_date.strftime('%B %d, %Y')}!")

        # Refresh displayed calendar
        st.rerun()


if __name__ == "__main__":
    run()
