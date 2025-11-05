## Caesar Cipher 

A simple Streamlit UI for the classic Caesar cipher (encrypt / decrypt) with a built-in HACK (brute-force) mode for decrypting when the key is unknown.
This preserves the original command-line logic (Al Sweigart’s examples) while exposing a friendly web interface.

## Features

Encrypt text using a user-chosen key (0–25).

Decrypt text using a user-chosen key.

HACK (brute-force): when you forget the key, try all 26 possible keys and inspect each candidate result.

Contextual UI: only shows options relevant to the current mode (Encrypt or Decrypt).

Copy result to clipboard on the server (if pyperclip is available); otherwise, you can select & copy from the text area.

Preserves non-A–Z characters (spaces, punctuation) unchanged — only A–Z letters are shifted (exactly like the original script).