import streamlit as st
import streamlit.components.v1 as components

def run(height=650, message="HELLO WORLD"):

    # ✅ Streamlit mode switcher
    st.title()
    st.markdown(
      """  Displays a scrolling ASCII art double-helix similar to the original terminal animation.
    Includes Normal Mode, Secret Message Reveal, and Download Log options.

    # How to Use
    1. Choose a mode:
    Normal DNA — classic nucleotide animation
    Reveal Hidden Message — DNA reveals a secret message over time
    2. Watch the helix scroll smoothly on screen.
    3. Click Download DNA Log to save the full animation as a text file.
    4.Customize your hidden message via the input settings.""")
    mode = st.selectbox(
        "DNA Mode:",
        ["Normal DNA", "Reveal Hidden Message"]
    )

    reveal_flag = "true" if mode == "Reveal Hidden Message" else "false"

    DNA_HTML = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            background: black;
            color: #00FFAA;
            font-family: monospace;
            font-size: 18px;
        }}
        #dna {{
            white-space: pre;
        }}
        #downloadBtn {{
            background: #00FFAA;
            color: black;
            padding: 8px 14px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 9999;
        }}
    </style>
    </head>

    <body>

    <button id="downloadBtn">📥 Download DNA Log</button>
    <div id="dna"></div>

    <script>
    const dnaDiv = document.getElementById("dna");
    const logData = [];

    const rows = [
        "         ##",
        "        #{{}}-{{}}#",
        "       #{{}}---{{}}#",
        "      #{{}}-----{{}}#",
        "     #{{}}------{{}}#",
        "    #{{}}------{{}}#",
        "    #{{}}-----{{}}#",
        "     #{{}}---{{}}#",
        "     #{{}}-{{}}#",
        "      ##",
        "     #{{}}-{{}}#",
        "     #{{}}---{{}}#",
        "    #{{}}-----{{}}#",
        "    #{{}}------{{}}#",
        "     #{{}}------{{}}#",
        "      #{{}}-----{{}}#",
        "       #{{}}---{{}}#",
        "        #{{}}-{{}}#"
    ];

    const pairs = [
        ["A","T"],
        ["T","A"],
        ["C","G"],
        ["G","C"]
    ];

    const hiddenMessage = "{message}";
    let index = 0;
    let msgIndex = 0;
    let frameCounter = 0;

    // ✅ Mode flag from Python
    const revealMode = {reveal_flag};

    function frame() {{
        let r = rows[index];

        if (r.includes("{{}}")) {{

            if (revealMode && frameCounter % 25 === 0) {{
                // ✅ Hidden message reveal mode
                let char = hiddenMessage[msgIndex % hiddenMessage.length];
                r = r.replace("{{}}", char).replace("{{}}", char);
                msgIndex++;
            }}
            else {{
                // ✅ Normal DNA
                let pair = pairs[Math.floor(Math.random()*pairs.length)];
                r = r.replace("{{}}", pair[0]).replace("{{}}", pair[1]);
            }}
        }}

        dnaDiv.innerText += r + "\\n";
        logData.push(r);

        window.scrollTo(0, document.body.scrollHeight);

        frameCounter++;
        index = (index + 1) % rows.length;
    }}

    setInterval(frame, 150);

    // ✅ Working Download Button
    document.getElementById("downloadBtn").onclick = function() {{
        const blob = new Blob([logData.join("\\n")], {{type: "text/plain"}});
        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "dna_animation.txt";
        a.click();

        URL.revokeObjectURL(url);
    }};
    </script>

    </body>
    </html>
    """

    components.html(DNA_HTML, height=height, width="100%", scrolling=True)
