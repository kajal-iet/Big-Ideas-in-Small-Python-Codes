import streamlit as st

EMPTY_SPACE = '.'
PLAYER_X = 'X'
PLAYER_O = 'O'
BOARD_WIDTH = 7
BOARD_HEIGHT = 6


def getNewBoard():
    return {(c, r): EMPTY_SPACE for c in range(BOARD_WIDTH) for r in range(BOARD_HEIGHT)}


def dropTile(board, col):
    for r in range(BOARD_HEIGHT-1, -1, -1):
        if board[(col, r)] == EMPTY_SPACE:
            return (col, r)
    return None


def tile_visual(t):
    return "🔴" if t == PLAYER_X else "🟡" if t == PLAYER_O else "⚪"


def isWinner(t, b):
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT):
            if b[(c, r)] == b[(c+1, r)] == b[(c+2, r)] == b[(c+3, r)] == t:
                return True

    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT-3):
            if b[(c, r)] == b[(c, r+1)] == b[(c, r+2)] == b[(c, r+3)] == t:
                return True

    for c in range(BOARD_WIDTH-3):
        for r in range(BOARD_HEIGHT-3):
            if b[(c, r)] == b[(c+1, r+1)] == b[(c+2, r+2)] == b[(c+3, r+3)] == t:
                return True
            if b[(c+3, r)] == b[(c+2, r+1)] == b[(c+1, r+2)] == b[(c, r+3)] == t:
                return True

    return False


def render_board(board):
    for r in range(BOARD_HEIGHT):
        cols = st.columns(BOARD_WIDTH)
        for c in range(BOARD_WIDTH):
            with cols[c]:
                st.markdown(
                    f"<h2 style='text-align:center'>{tile_visual(board[(c,r)])}</h2>",
                    unsafe_allow_html=True
                )


def reset_game():
    st.session_state.board = getNewBoard()
    st.session_state.player = PLAYER_X
    st.session_state.winner = None


def run():
    st.set_page_config(
    page_title="Responsive App",
    layout="centered",
    initial_sidebar_state="collapsed"
    )

    st.title("Connect 4 🔴🟡")
    st.markdown(
        """

    - The board has **7 columns × 6 rows**.
    - Two players take turns:
    - 🔴 Player X
    - 🟡 Player O
    - On your turn:
    - Choose a **column (0–6)**
    - Click **Drop** to place your disc
    - The disc falls to the **lowest empty space** in the column.
    - First player to connect **4 discs in a row** wins:
    - Horizontally
    - Vertically
    - Diagonally
    - Click **Restart Game** to start over.
    """
    )

    if "board" not in st.session_state:
        reset_game()

    board = st.session_state.board
    player = st.session_state.player
    winner = st.session_state.winner

    render_board(board)

    if winner:
        st.success(f"Winner: {winner}")
        if st.button("Restart"):
            reset_game()
        return

    col = st.number_input("Column (0-6):", min_value=0, max_value=6, step=1)

    def on_drop():
        pos = dropTile(board, col)
        if pos:
            board[pos] = player
            if isWinner(player, board):
                st.session_state.winner = player
            else:
                st.session_state.player = PLAYER_O if player == PLAYER_X else PLAYER_X

    st.button("Drop", on_click=on_drop)

    st.button("Restart Game", on_click=reset_game)



if __name__ == "__main__":
    run()
