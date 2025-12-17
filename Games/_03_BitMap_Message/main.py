import streamlit as st
import time
import os

# ---------------- BITMAP (UNCHANGED) ----------------
bitmap = """
....................................................................
   *************   ***     ***   *************   *************
   *************   ***     ***   *************   *************
   ***             ***     ***   ***             ***          
   ***             ***     ***   ***             ***          
   *************   ***********   *************   *************
   *************   ***********   *************   *************
            ***   ***     ***             ***   ***     ***
            ***   ***     ***             ***   ***     ***
   *************   ***     ***   *************   *************
   *************   ***     ***   *************   *************
....................................................................
"""

def run():

    # ---------------- UI STYLES (ONLY UI) ----------------
    st.markdown("""
    <style>
    .bm-container {
        max-width: 650px;
        margin: auto;
        padding: 10px;
    }
    .bm-card {
        border: 1px solid #e6e6e6;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
        background: #ffffff;
    }
    input[type="text"] {
        font-size: 18px !important;
    }
    button {
        width: 100%;
        border-radius: 14px;
        font-size: 16px;
        padding: 8px 0;
    }
    .output-box {
        max-height: 320px;
        overflow-x: auto;
        overflow-y: auto;
        border-radius: 12px;
        padding: 12px;
        background: #111;
        margin-top: 10px;
    }
    pre {
        font-size: 13px;
        line-height: 1.2;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="bm-container">', unsafe_allow_html=True)

    # ---------------- TITLE ----------------
    st.title("🗺️ Bitmap Message — Text Art Generator")

    st.markdown("""
    Turn your text into **ASCII-style pixel art** using a bitmap pattern ✨  

    **How it works**
    - Characters replace pixels in the bitmap  
    - Spaces remain empty  
    - Your message loops automatically  
    """)

    # ---------------- INPUT CARD ----------------
    st.markdown('<div class="bm-card">', unsafe_allow_html=True)

    message = st.text_input("✍️ Enter your message")
    color = st.color_picker("🎨 Pick display color", "#00FFAA")

    speed_choice = st.radio(
        "⚡ Printing speed",
        ["🐢 Slow", "🐇 Fast", "⚡ Instant"],
        horizontal=True
    )

    generate = st.button("▶ Generate Message")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- OUTPUT ----------------
    if message and generate:

        output_placeholder = st.empty()
        final_output = ""

        delay = 0.1 if speed_choice == "🐢 Slow" else 0.03 if speed_choice == "🐇 Fast" else 0
        message_index = 0

        for line in bitmap.splitlines():
            output_line = ""
            for c in line:
                if c == " ":
                    output_line += " "
                else:
                    output_line += message[message_index % len(message)]
                    message_index += 1

            final_output += output_line + "\n"

            if delay > 0:
                output_placeholder.markdown(
                    f"""
                    <div class="output-box">
                        <pre style="color:{color};">{final_output}</pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                time.sleep(delay)

        # Final output
        output_placeholder.markdown(
            f"""
            <div class="output-box">
                <pre style="color:{color};">{final_output}</pre>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------- SAVE + DOWNLOAD ----------------
        os.makedirs("outputs", exist_ok=True)
        file_path = os.path.join("outputs", "bitmap_output.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_output)

        st.success("✅ Output generated successfully!")
        st.download_button(
            "⬇️ Download Output",
            final_output,
            "bitmap_output.txt",
            "text/plain"
        )

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    run()
