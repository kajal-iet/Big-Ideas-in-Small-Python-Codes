import streamlit as st

# ----------------------------
EMPTY_SPACE = '.'
PLAYER_X = 'X'
PLAYER_O = 'O'
BOARD_WIDTH = 7
BOARD_HEIGHT = 6


def getNewBoard():
    board = {}
    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT):
            board[(c, r)] = EMPTY_SPACE
    return board


def dropTile(board, columnIndex):
    for rowIndex in range(BOARD_HEIGHT - 1, -1, -1):
        if board[(columnIndex, rowIndex)] == EMPTY_SPACE:
            return (columnIndex, rowIndex)
    return None


def isFull(board):
    return not any(board[pos] == EMPTY_SPACE for pos in board)


def isWinner(playerTile, board):
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT):
            if board[(c, r)] == board[(c+1, r)] == board[(c+2, r)] == board[(c+3, r)] == playerTile:
                return True

    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT - 3):
            if board[(c, r)] == board[(c, r+1)] == board[(c, r+2)] == board[(c, r+3)] == playerTile:
                return True

    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT - 3):
            if board[(c, r)] == board[(c+1, r+1)] == board[(c+2, r+2)] == board[(c+3, r+3)] == playerTile:
                return True
            if board[(c+3, r)] == board[(c+2, r+1)] == board[(c+1, r+2)] == board[(c, r+3)] == playerTile:
                return True

    return False


# ----------------------------
# UI symbol mapping
def tile_visual(tile):
    if tile == PLAYER_X:
        return "🔴"
    if tile == PLAYER_O:
        return "🟡"
    return "⚪"


# ----------------------------
def renderBoard(board):
    for r in range(BOARD_HEIGHT):
        cols = st.columns(BOARD_WIDTH)
        for c in range(BOARD_WIDTH):
            with cols[c]:
                st.markdown(
                    f"<h2 style='text-align:center'>{tile_visual(board[(c,r)])}</h2>",
                    unsafe_allow_html=True
                )


# ----------------------------
def run():

    st.title("Connect 4 🟡🔴 (Streamlit Edition)")

    if "board" not in st.session_state:
        st.session_state.board = getNewBoard()

    if "player" not in st.session_state:
        st.session_state.player = PLAYER_X

    # store last selected column safely
    if "selected_col" not in st.session_state:
        st.session_state.selected_col = 0      

    st.write("Current Turn:", "🔴" if st.session_state.player == PLAYER_X else "🟡")

    renderBoard(st.session_state.board)

    # update only on select
    new_col = st.selectbox("Choose a column:", list(range(BOARD_WIDTH)), index=st.session_state.selected_col)
    st.session_state.selected_col = new_col   # <<< FIX


    if st.button("Drop"):
        col = st.session_state.selected_col

        pos = dropTile(st.session_state.board, col)

        if pos:
            st.session_state.board[pos] = st.session_state.player

            if isWinner(st.session_state.player, st.session_state.board):
                st.session_state.last_winner = st.session_state.player
                st.rerun()

            if isFull(st.session_state.board):
                st.session_state.tie = True
                st.rerun()

            st.session_state.player = (
                PLAYER_O if st.session_state.player == PLAYER_X
                else PLAYER_X
            )

        st.rerun()



if __name__ == "__main__":
    run()
