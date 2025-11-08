import streamlit as st
import streamlit.components.v1 as components

def run(height=800):
    """Matrix Rain with Streamlit UI mode switch."""

    # ✅ Mode selection
    mode = st.selectbox("Choose Rain Mode:", ["Straight", "Wave"])

    wave_flag = "true" if mode == "Wave" else "false"

    MATRIX_HTML = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            overflow: hidden;
            background: black;
        }}
    </style>
    </head>

    <body>
    <canvas id="matrix"></canvas>

    <script>
    const canvas = document.getElementById("matrix");
    const ctx = canvas.getContext("2d");

    function resize() {{
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }}
    resize();
    window.onresize = resize;

    const letters = "01";
    const fontSize = 18;
    let columns = Math.floor(canvas.width / fontSize);
    let drops = Array(columns).fill(1);

    // ✅ Get mode from Streamlit
    const waveMode = {wave_flag};

    // ✅ Wave parameters
    const waveAmplitude = 12;
    const waveSpeed = 0.035;

    function draw() {{
        ctx.fillStyle = "rgba(0,0,0,0.06)";
        ctx.fillRect(0,0,canvas.width,canvas.height);

        ctx.fillStyle = "#0F0";
        ctx.font = fontSize + "px monospace";

        drops.forEach((y, i) => {{
            const char = letters[Math.floor(Math.random() * letters.length)];

            let x = i * fontSize;

            // ✅ Apply wave only if enabled
            if (waveMode) {{
                x += Math.sin((Date.now() * waveSpeed) + (i * 0.5)) * waveAmplitude;
            }}

            ctx.fillText(char, x, y * fontSize);

            if (y * fontSize > canvas.height && Math.random() > 0.975) {{
                drops[i] = 0;
            }}

            drops[i]++;
        }});
    }}

    setInterval(draw, 50);
    </script>

    </body>
    </html>
    """

    components.html(MATRIX_HTML, height=height, width="100%")
