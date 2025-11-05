import streamlit as st
import time
import os

# Your original bitmap (you can replace this with your actual one)
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
    st.title("🗺️ Bitmap Message — Text Art Generator")

    st.markdown("""
    Turn plain text into **ASCII-style pixel art** using a bitmap pattern! 🖋️  

    **How it works:**  
    - Enter a custom message.  
    - Each `#` in the bitmap gets replaced with a character from your text.  
    - Spaces stay empty, so you get a cool text-based visual output.  

    💡 Try with words like *HELLO WORLD*, *PYTHON*, or your name to see your message appear as ASCII art!
    """)
    st.divider()


    # Inputs
    message = st.text_input("Enter your message:")
    color = st.color_picker("Pick your display color:", "#00FFAA")
    speed_choice = st.radio(
        "Select printing speed:",
        ["🐢 Slow", "🐇 Fast", "⚡ Instant"],
        horizontal=True
    )

    if message and st.button("Generate Message"):
        st.markdown("---")
        output_placeholder = st.empty()
        final_output = ""

        # Set delay based on speed
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
            # Show progress gradually
            if delay > 0:
                output_placeholder.markdown(f"<pre style='color:{color}'>{final_output}</pre>", unsafe_allow_html=True)
                time.sleep(delay)

        # Final full output
        output_placeholder.markdown(f"<pre style='color:{color}'>{final_output}</pre>", unsafe_allow_html=True)

        # Save output to file
        os.makedirs("outputs", exist_ok=True)
        file_path = os.path.join("outputs", "bitmap_output.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_output)
        
        st.success(f"✅ Output saved to `{file_path}`")
        st.download_button("⬇️ Download Output", final_output, "bitmap_output.txt", "text/plain")

