import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Pattern Carpet",
    layout="centered"
)

# ------------------ APP ------------------
def run():
    st.title("🧵 Pattern Carpet")
    st.caption("Create, preview, and export repeating ASCII carpets")

    st.markdown("""
    ### 🎮 How it works
    - Enter a **base pattern**
    - Choose repeats and background color
    - Click **Apply Changes** to update the carpet
    - Download as **text or image**
    """)

    # ------------------ SESSION STATE INIT ------------------
    if "applied_pattern" not in st.session_state:
        st.session_state.applied_pattern = "_ \\ \\ \\_/ __\n \\ \\ \\___/ _\n\\ \\ \\_____/"
        st.session_state.applied_x = 6
        st.session_state.applied_y = 4
        st.session_state.applied_bg = "#000000"

    # ------------------ INPUT CONTROLS ------------------
    pattern_input = st.text_area(
        "Enter base pattern:",
        value=st.session_state.applied_pattern,
        height=150
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        x_repeat = st.slider("Horizontal Repeat", 1, 12, st.session_state.applied_x)
    with col2:
        y_repeat = st.slider("Vertical Repeat", 1, 12, st.session_state.applied_y)
    with col3:
        bg_color = st.color_picker("Background Color", st.session_state.applied_bg)

    # ------------------ APPLY BUTTON ------------------
    if st.button("✅ Apply Changes"):
        st.session_state.applied_pattern = pattern_input
        st.session_state.applied_x = x_repeat
        st.session_state.applied_y = y_repeat
        st.session_state.applied_bg = bg_color

    # ------------------ BUILD OUTPUT FROM APPLIED STATE ------------------
    base_lines = st.session_state.applied_pattern.splitlines()

    output_lines = []
    for _ in range(st.session_state.applied_y):
        for line in base_lines:
            output_lines.append(line * st.session_state.applied_x)

    carpet_text = "\n".join(output_lines)

    # ------------------ DISPLAY ------------------
    st.markdown("### 🖨 Carpet Preview")

    st.markdown(
        f"""
        <div style="
            background:{st.session_state.applied_bg};
            padding:16px;
            border-radius:6px;
            overflow-x:auto;
        ">
            <pre style="
                margin:0;
                font-family:monospace;
                font-size:14px;
                color:#ffffff;
            ">{carpet_text}</pre>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------ DOWNLOAD AS TEXT ------------------
    st.download_button(
        label="⬇ Download as Text (.txt)",
        data=carpet_text,
        file_name="pattern_carpet.txt",
        mime="text/plain"
    )

    # ------------------ DOWNLOAD AS IMAGE ------------------
    img_bytes = generate_image(
        carpet_text,
        bg_color=st.session_state.applied_bg
    )

    st.download_button(
        label="🖼 Download as Image (.png)",
        data=img_bytes,
        file_name="pattern_carpet.png",
        mime="image/png"
    )


# ------------------ IMAGE GENERATION ------------------
def generate_image(text, bg_color):
    lines = text.splitlines()
    font_size = 16
    padding = 20

    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Measure text
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    max_width = max(draw.textlength(line, font=font) for line in lines)
    line_height = font_size + 4

    img_width = int(max_width) + padding * 2
    img_height = line_height * len(lines) + padding * 2

    img = Image.new("RGB", (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    y = padding
    for line in lines:
        draw.text((padding, y), line, fill="white", font=font)
        y += line_height

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


# ------------------ RUN ------------------
if __name__ == "__main__":
    run()
