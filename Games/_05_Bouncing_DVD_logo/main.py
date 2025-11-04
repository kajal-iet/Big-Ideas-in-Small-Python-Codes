import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random, time

def run():
    st.title("💿 Bouncing DVD Logo (Streamlit Edition)")
    st.markdown("A modern web version of the classic screensaver!")

    # --- Layout ---
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.subheader("⚙️ Controls")
        num_logos = st.slider("Number of logos", 1, 10, 3)
        logo_text = st.text_input("Logo text", "DVD")
        speed = st.slider("Speed", 1, 20, 8)
        trail = st.checkbox("Enable trailing effect", True)
        random_colors = st.checkbox("Random colors", True)
        start = st.button("▶️ Start Animation", use_container_width=True)

    with right:
        st.subheader("🎞️ Animation Preview")
        frame_placeholder = st.empty()

    # --- Initialize screen size and settings ---
    WIDTH, HEIGHT = 600, 400
    LOGO_SIZE = 70
    FPS = 30

    # --- Utility Functions ---
    def random_color():
        return tuple(random.randint(80, 255) for _ in range(3))

    def init_logos():
        logos = []
        for _ in range(num_logos):
            logos.append({
                "x": random.randint(0, WIDTH - LOGO_SIZE),
                "y": random.randint(0, HEIGHT - LOGO_SIZE),
                "dx": random.choice([-1, 1]),
                "dy": random.choice([-1, 1]),
                "color": random_color(),
            })
        return logos

    # --- Initialize Session State ---
    if "trail_img" not in st.session_state:
        st.session_state.trail_img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))

    if "corner_hits" not in st.session_state:
        st.session_state.corner_hits = 0

    logos = init_logos()

    # --- Animation loop ---
    if start:
        while True:
            if trail:
                # use previous frame for fading effect
                img = st.session_state.trail_img.copy()
                fade = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 40))
                img = Image.alpha_composite(img, fade)
            else:
                img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))

            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            corner_hit = False

            for logo in logos:
                # Move logo
                logo["x"] += logo["dx"] * speed
                logo["y"] += logo["dy"] * speed

                hit_x = hit_y = False

                # Bounce off walls
                if logo["x"] <= 0 or logo["x"] + LOGO_SIZE >= WIDTH:
                    logo["dx"] *= -1
                    logo["color"] = random_color() if random_colors else logo["color"]
                    hit_x = True
                if logo["y"] <= 0 or logo["y"] + LOGO_SIZE >= HEIGHT:
                    logo["dy"] *= -1
                    logo["color"] = random_color() if random_colors else logo["color"]
                    hit_y = True

                # Corner hit detection
                if hit_x and hit_y:
                    corner_hit = True
                    logo["color"] = (255, 255, 255)  # flash white briefly

                # Draw logo
                draw.rounded_rectangle(
                    [logo["x"], logo["y"], logo["x"] + LOGO_SIZE, logo["y"] + LOGO_SIZE],
                    radius=10, fill=logo["color"]
                )

                # Center the logo text
                bbox = draw.textbbox((0, 0), logo_text, font=font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text(
                    (logo["x"] + (LOGO_SIZE - w) // 2, logo["y"] + (LOGO_SIZE - h) // 2),
                    logo_text, fill="black", font=font
                )

            # Update corner hit counter
            if corner_hit:
                st.session_state.corner_hits += 1

            # Draw the counter text in top-left corner
            counter_text = f"💥 Corner Hits: {st.session_state.corner_hits}"
            draw.text((10, 10), counter_text, fill=(255, 255, 255), font=font)

            # Save trail frame if enabled
            if trail:
                st.session_state.trail_img = img

            # Display frame
            frame_placeholder.image(img.convert("RGB"))
            time.sleep(1 / FPS)
