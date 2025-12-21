import streamlit as st
import time
import os
import random

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

def vary_color(hex_color):
    """Create slight RGB variations for colorful effect"""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = min(255, max(0, r + random.randint(-40, 40)))
    g = min(255, max(0, g + random.randint(-40, 40)))
    b = min(255, max(0, b + random.randint(-40, 40)))

    return f"rgb({r},{g},{b})"


def run():
    st.set_page_config(
    page_title="Responsive App",
    layout="centered",
    initial_sidebar_state="collapsed"
    )
    st.title("🗺️ Bitmap Message — Text Art Generator")

    # ---------- MOBILE + OUTPUT CSS ----------
    st.markdown("""
    <style>
    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .bitmap-output {
        font-family: monospace;
        font-size: 0.75rem;
        line-height: 1.1;
        overflow-x: auto;
        white-space: pre;
        padding: 12px;
        border-radius: 8px;
        background-color: #000;
    }

    @media (max-width: 768px) {
        .bitmap-output {
            font-size: 0.6rem;
        }
        .stButton > button {
            width: 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    Turn plain text into **ASCII-style pixel art** using a bitmap pattern!

    ✨ Each character is rendered with **real color styling**, not a flat block.
    """)
    st.divider()

    # ---------- Inputs ----------
    message = st.text_input("Enter your message:")
    base_color = st.color_picker("Pick your base color:", "#00FFAA")
    speed_choice = st.radio(
        "Select printing speed:",
        ["🐢 Slow", "🐇 Fast", "⚡ Instant"],
        horizontal=True
    )

    if message and st.button("Generate Message", use_container_width=True):
        st.markdown("---")
        output_placeholder = st.empty()

        delay = 0.1 if speed_choice == "🐢 Slow" else 0.03 if speed_choice == "🐇 Fast" else 0

        message_index = 0
        final_html = ""

        for line in bitmap.splitlines():
            line_html = ""
            for c in line:
                if c == "*":
                    ch = message[message_index % len(message)]
                    message_index += 1
                    color = vary_color(base_color)
                    line_html += f"<span style='color:{color}'>{ch}</span>"
                else:
                    line_html += "&nbsp;"
            final_html += line_html + "<br>"

            if delay > 0:
                output_placeholder.markdown(
                    f"<div class='bitmap-output'>{final_html}</div>",
                    unsafe_allow_html=True
                )
                time.sleep(delay)

        # Final render
        output_placeholder.markdown(
            f"<div class='bitmap-output'>{final_html}</div>",
            unsafe_allow_html=True
        )

        # ---------- Save output (plain text version) ----------
        os.makedirs("outputs", exist_ok=True)
        file_path = os.path.join("outputs", "bitmap_output.txt")

        text_only = ""
        idx = 0
        for line in bitmap.splitlines():
            out = ""
            for c in line:
                if c == "*":
                    out += message[idx % len(message)]
                    idx += 1
                else:
                    out += " "
            text_only += out + "\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_only)

        st.success("✅ Output saved successfully")
        st.download_button(
            "⬇️ Download Output",
            text_only,
            "bitmap_output.txt",
            "text/plain",
            use_container_width=True
        )

if __name__ == "__main__":
    run()
