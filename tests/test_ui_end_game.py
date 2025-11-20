#
# Run all tests: `PYTHONPATH=src pytest -q`
#
from tictactoe.ui.app import GameApp
from tictactoe.core.constants import CROSS_SYMBOL, NOUGHT_SYMBOL


# Create a GameApp instance without mainloop and hide the window.
# Additionally, jam real PhotoImages to avoid problems
# with Tk images in the test environment.
def create_app():
    app = GameApp()
    app.withdraw()

    # In the tests, interested in logic, not real PNGs,
    # Therefore, replace green images with "empty" values.
    app.cross_img_green = ""
    app.nought_img_green = ""

    return app


# The user plays X, wins with the top line (0,1,2).
#
# Expecting:
# - status contains "User WINS"
# - all cells and the Start button are locked
def test_end_game_user_wins_disables_board_and_sets_status():
    app = create_app()

    # User = X, bot = O
    app.human.set(CROSS_SYMBOL)
    app.bot = NOUGHT_SYMBOL

    # X X X
    # . . .
    # . . .
    app.board = [
        CROSS_SYMBOL, CROSS_SYMBOL, CROSS_SYMBOL,
        None, None, None,
        None, None, None,
    ]

    app.end_game(CROSS_SYMBOL)

    status = app.status_var.get()
    assert "User WINS" in status

    # All cells are locked
    for btn in app.cells.values():
        assert btn.instate(["disabled"])

    # Start should also be blocked
    assert app.start_btn.instate(["disabled"])

    # Logical state of the game
    assert app.started is False
    assert app.current == CROSS_SYMBOL


# The bot wins (e.g. X as a bot, O as a user).
#
# Checking:
# - status contains "Bot WINS"
# - all cells and Start-locked
def test_end_game_bot_wins_sets_correct_status_and_disables():
    app = create_app()

    # User = O, Bot = X
    app.human.set(NOUGHT_SYMBOL)
    app.bot = CROSS_SYMBOL

    # X X X
    # . . .
    # . . .
    app.board = [
        CROSS_SYMBOL, CROSS_SYMBOL, CROSS_SYMBOL,
        None, None, None,
        None, None, None,
    ]

    app.end_game(CROSS_SYMBOL)

    status = app.status_var.get()
    assert "Bot WINS" in status

    # All cells are locked
    for btn in app.cells.values():
        assert btn.instate(["disabled"])

    # Start is also blocked
    assert app.start_btn.instate(["disabled"])

    # Game stopped
    assert app.started is False
    assert app.current == CROSS_SYMBOL


# Draw: winner=None, the field is filled, but without 3 in a row.
#
# Expecting:
# - status contains "TIE"
# - all buttons are locked
def test_end_game_tie_sets_tie_status_and_disables():
    app = create_app()

    # Some state of a draw without a winner
    # X O X
    # X O O
    # O X X
    app.board = [
        CROSS_SYMBOL, NOUGHT_SYMBOL, CROSS_SYMBOL,
        CROSS_SYMBOL, NOUGHT_SYMBOL, NOUGHT_SYMBOL,
        NOUGHT_SYMBOL, CROSS_SYMBOL, CROSS_SYMBOL,
    ]

    app.end_game(None)

    status = app.status_var.get()
    assert "TIE" in status

    # All cells are locked
    for btn in app.cells.values():
        assert btn.instate(["disabled"])

    # Start is also blocked
    assert app.start_btn.instate(["disabled"])

    # Game stopped
    assert app.started is False
    assert app.current == CROSS_SYMBOL
