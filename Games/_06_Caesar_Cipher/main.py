# Games/_XX_CaesarCipher/main.py
import streamlit as st

try:
    import pyperclip
except Exception:
    pyperclip = None

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def caesar_translate(message: str, key: int, mode: str) -> str:
    """Encrypt or decrypt message using Caesar cipher (A-Z only)."""
    message = message.upper()
    translated = ''
    for symbol in message:
        if symbol in SYMBOLS:
            num = SYMBOLS.find(symbol)
            if mode == 'encrypt':
                num = num + key
            else:  # decrypt
                num = num - key

            if num >= len(SYMBOLS):
                num = num - len(SYMBOLS)
            elif num < 0:
                num = num + len(SYMBOLS)

            translated += SYMBOLS[num]
        else:
            translated += symbol
    return translated

def run():
    st.title("🔐 Caesar Cipher (Encrypt / Decrypt / Hacker)")

    st.markdown("""
    The **Caesar Cipher** is one of the oldest and simplest encryption techniques —  
    each letter in your message is shifted by a secret key 🔑.  

    🧩 Modes:
    - **Encrypt**: Encode your message with a chosen key  
    - **Decrypt**: Decode it if you know the key  
    - **Hack Mode**: Forgot the key? Let the Caesar Hacker try **all possible shifts** automatically!  

    💡 Great for learning basic cryptography, substitution ciphers, and brute-force logic.
    """)

    # Choose mode
    mode = st.radio("Mode", ["Encrypt", "Decrypt"], index=0, key="caesar_mode")

    # Common message input (we show context-sensitive helper texts)
    if mode == "Encrypt":
        st.info("Encrypt mode: enter a key (0–25) and a message to encrypt. Hacker is not available when encrypting.")
        key = st.slider("Key (shift amount)", 0, len(SYMBOLS)-1, 3, key="encrypt_key")
        message = st.text_area("Message to encrypt", value="", key="encrypt_message", placeholder="Type the message to encrypt (letters only will be shifted).")
        if st.button("🔒 Encrypt", key="encrypt_btn"):
            if not message:
                st.warning("Enter a message to encrypt.")
            else:
                result = caesar_translate(message, key, "encrypt")
                st.success("Encrypted text:")
                st.text_area("Encrypted output", value=result, height=120, key="encrypt_output")
                # Try to copy to clipboard (server-side). If pyperclip unavailable, prompt user to select text.
                if pyperclip:
                    try:
                        pyperclip.copy(result)
                        st.info("Encrypted text copied to clipboard (server-side). If this didn't work for you, select and copy from the box above.")
                    except Exception:
                        st.info("Couldn't copy to clipboard automatically. Please select and copy the encrypted text above.")
                else:
                    st.info("Tip: select and copy the encrypted text above (pyperclip not installed on server).")

    else:  # Decrypt
        st.info("Decrypt mode: either enter the key (if you remember it) or choose HACK to try all possible keys.")
        decrypt_choice = st.radio("Decrypt option", ["Enter key", "HACK (brute-force)"], index=0, key="decrypt_choice")

        if decrypt_choice == "Enter key":
            key = st.slider("Key (0–25)", 0, len(SYMBOLS)-1, 3, key="decrypt_key")
            message = st.text_area("Encrypted message to decrypt", value="", key="decrypt_message")
            if st.button("🔓 Decrypt", key="decrypt_btn"):
                if not message:
                    st.warning("Enter the encrypted message to decrypt.")
                else:
                    result = caesar_translate(message, key, "decrypt")
                    st.success(f"Decrypted with key {key}:")
                    st.text_area("Decrypted output", value=result, height=120, key="decrypt_output")
                    if pyperclip:
                        try:
                            pyperclip.copy(result)
                            st.info("Decrypted text copied to clipboard (server-side). If this didn't work for you, select and copy from the box above.")
                        except Exception:
                            st.info("Couldn't copy to clipboard automatically. Please select and copy the decrypted text above.")
                    else:
                        st.info("Tip: select and copy the decrypted text above (pyperclip not installed on server).")

        else:  # HACK (brute-force)
            st.write("HACK mode: enter the encrypted message and click **Run Hacker**. The app will show every key candidate (Key #0..#25).")
            hack_message = st.text_area("Encrypted message to hack", value="", key="hack_message")
            if st.button("🛠️ Run Hacker (brute-force)", key="run_hacker_btn"):
                if not hack_message:
                    st.warning("Please provide the encrypted message to hack.")
                else:
                    candidates = []
                    st.write("### Hacker results (Key # : Decrypted candidate)")
                    for key_trial in range(len(SYMBOLS)):
                        translated = caesar_translate(hack_message, key_trial, "decrypt")
                        candidates.append((key_trial, translated))
                        # show as expandable so UI doesn't get long
                        with st.expander(f"Key #{key_trial}", expanded=False):
                            st.write(translated)
                            # allow selecting this candidate to copy/display
                            if st.button(f"Select Key #{key_trial}", key=f"select_{key_trial}"):
                                # set selected output into a text area below
                                st.session_state.setdefault("selected_decryption", {"key": key_trial, "text": translated})
                                st.success(f"Selected Key #{key_trial} — decrypted text stored below.")
                                # attempt to copy
                                if pyperclip:
                                    try:
                                        pyperclip.copy(translated)
                                        st.info("Selected decrypted text copied to clipboard (server-side).")
                                    except Exception:
                                        st.info("Couldn't copy to clipboard automatically.")
                                st.experimental_rerun()

                    # After listing, if user previously selected one, show it
                    if "selected_decryption" in st.session_state:
                        sel = st.session_state["selected_decryption"]
                        st.write("---")
                        st.write(f"### Previously selected Key #{sel['key']}")
                        st.text_area("Selected decrypted text", value=sel["text"], height=140, key="selected_output")
                        st.info("You can copy the selected text above. (pyperclip may not work for client clipboard.)")

    st.write("---")
    st.caption("Caesar Cipher UI — preserves original logic. Letters outside A–Z are left unchanged.")
