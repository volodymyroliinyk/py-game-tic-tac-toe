from tictactoe.ui.app import GameApp
from tictactoe.core.constants import CROSS_SYMBOL, NOUGHT_SYMBOL


# Create a GameApp instance without mainloop,
# hide the window and jam the green PNGs to avoid problems with Tk PhotoImage.
def create_app():
    app = GameApp()
    app.withdraw()

    # In tests, interested in logic, not real images.
    app.cross_img_black = ""
    app.nought_img_black = ""
    app.cross_img_green = ""
    app.nought_img_green = ""

    return app


# If the game has not yet started (started == False),
# clicking on a cell should not change the board.
def test_on_cell_click_ignored_if_not_started():
    app = create_app()

    app.started = False
    before = app.board.copy()

    app.on_cell_click(0, 0)

    assert app.board == before


# If the cell is already occupied, the click does not change anything.
def test_on_cell_click_ignored_if_cell_not_empty():
    app = create_app()

    app.started = True
    app.human.set(CROSS_SYMBOL)
    app.bot = NOUGHT_SYMBOL
    app.current = CROSS_SYMBOL

    # Let's take a cell (0,0)
    idx = 0
    app.board[idx] = CROSS_SYMBOL
    app.cells[(0, 0)].config(text="X")

    before = app.board.copy()

    app.on_cell_click(0, 0)

    # The board has not changed
    assert app.board == before


# If the game has started and the cell is free, then after clicking
# in the board, the player symbol appears on the corresponding index.
def test_on_cell_click_places_human_symbol_on_empty_cell():
    app = create_app()

    app.started = True
    app.human.set(CROSS_SYMBOL)
    app.bot = NOUGHT_SYMBOL
    app.current = CROSS_SYMBOL

    # Before clicking, the entire board is empty
    assert all(v is None for v in app.board)

    app.on_cell_click(0, 0)

    idx = 0
    assert app.board[idx] == CROSS_SYMBOL
    # The button has drawn a symbol (either text or image) – minimally check the text
    assert app.cells[(0, 0)].cget("text") in ("X", CROSS_SYMBOL, "")


# If a user's click creates a 3 in a row, the game must end:
#   - started == False
# - all cells disabled
# - Start also disabled
# - the status contains "User WINS" or "wins"
def test_on_cell_click_winning_move_ends_game_and_disables_board():
    app = create_app()

    app.started = True
    app.human.set(CROSS_SYMBOL)
    app.bot = NOUGHT_SYMBOL
    app.current = CROSS_SYMBOL

    # Let's prepare the situation:
    # X X .
    # . . .
    # . . .
    # Clicking on (0.2) should give X a victory.
    app.board = [
        CROSS_SYMBOL, CROSS_SYMBOL, None,
        None, None, None,
        None, None, None,
    ]
    # synchronize the text on the buttons with the board
    app.cells[(0, 0)].config(text="X")
    app.cells[(0, 1)].config(text="X")

    # A move that should be victorious
    app.on_cell_click(0, 2)

    # The game must be completed
    assert app.started is False

    status = app.status_var.get()
    assert "WINS" in status or "wins" in status

    # All cells are locked
    for btn in app.cells.values():
        assert btn.instate(["disabled"])

    # The Start button is also blocked
    assert app.start_btn.instate(["disabled"])
