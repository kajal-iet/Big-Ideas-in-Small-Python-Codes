import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random, time

def run():
    st.title("💿 Bouncing DVD Logo — Retro Animation")

    # ---------- MOBILE RESPONSIVE CSS (UI ONLY) ----------
    st.markdown("""
    <style>
    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    @media (max-width: 768px) {
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }

        .stButton > button {
            width: 100%;
            margin-bottom: 0.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    Relive the nostalgia! Watch the classic **DVD logo** bounce around the screen.  
    If you’re lucky, you might see it hit the corner perfectly 😎  

    **How it works:**  
    - The logo moves diagonally and bounces off the edges.  
    - You can tweak speed, color, or number of logos for extra fun.  
    - Try spotting the “corner hit” moment — that’s the jackpot! 💥  
    """)
    st.divider()

    # ---------- Layout ----------
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

    # ---------- RESPONSIVE CANVAS SIZE ----------
    # Desktop default, mobile-safe scaling
    container_width = st.session_state.get("container_width", 600)
    WIDTH = min(600, container_width)
    HEIGHT = int(WIDTH * 0.66)

    LOGO_SIZE = int(WIDTH * 0.12)
    FPS = 30

    # ---------- Utility Functions ----------
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

    # ---------- Session State ----------
    if "trail_img" not in st.session_state or st.session_state.trail_img.size != (WIDTH, HEIGHT):
        st.session_state.trail_img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))

    if "corner_hits" not in st.session_state:
        st.session_state.corner_hits = 0

    logos = init_logos()

    # ---------- Animation Loop ----------
    if start:
        while True:
            if trail:
                img = st.session_state.trail_img.copy()
                fade = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 40))
                img = Image.alpha_composite(img, fade)
            else:
                img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))

            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            corner_hit = False

            for logo in logos:
                logo["x"] += logo["dx"] * speed
                logo["y"] += logo["dy"] * speed

                hit_x = hit_y = False

                if logo["x"] <= 0 or logo["x"] + LOGO_SIZE >= WIDTH:
                    logo["dx"] *= -1
                    logo["color"] = random_color() if random_colors else logo["color"]
                    hit_x = True

                if logo["y"] <= 0 or logo["y"] + LOGO_SIZE >= HEIGHT:
                    logo["dy"] *= -1
                    logo["color"] = random_color() if random_colors else logo["color"]
                    hit_y = True

                if hit_x and hit_y:
                    corner_hit = True
                    logo["color"] = (255, 255, 255)

                draw.rounded_rectangle(
                    [logo["x"], logo["y"], logo["x"] + LOGO_SIZE, logo["y"] + LOGO_SIZE],
                    radius=10,
                    fill=logo["color"]
                )

                bbox = draw.textbbox((0, 0), logo_text, font=font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text(
                    (logo["x"] + (LOGO_SIZE - w) // 2,
                     logo["y"] + (LOGO_SIZE - h) // 2),
                    logo_text,
                    fill="black",
                    font=font
                )

            if corner_hit:
                st.session_state.corner_hits += 1

            draw.text(
                (10, 10),
                f"💥 Corner Hits: {st.session_state.corner_hits}",
                fill=(255, 255, 255),
                font=font
            )

            if trail:
                st.session_state.trail_img = img

            frame_placeholder.image(img.convert("RGB"), use_container_width=True)
            time.sleep(1 / FPS)
