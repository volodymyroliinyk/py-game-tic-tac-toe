#
# Run all tests: `PYTHONPATH=src pytest -q`
#
from tictactoe.ui.app import GameApp
from tictactoe.core.constants import CROSS_SYMBOL, NOUGHT_SYMBOL


# Create a GameApp instance without launching mainloop.
# Call withdraw() so that the window does not blink during tests.
def create_app():
    app = GameApp()
    app.withdraw()
    return app


# on_reset must:
# - reset self.board (all None)
# - set started = False
# - set current = CROSS_SYMBOL
# - set bot = NOUGHT_SYMBOL
def test_on_reset_clears_board_and_flags():
    app = create_app()

    # Simulate the state in the middle of the game
    app.board[0] = CROSS_SYMBOL
    app.board[4] = NOUGHT_SYMBOL
    app.started = True
    app.current = NOUGHT_SYMBOL
    app.bot = CROSS_SYMBOL

    app.on_reset()

    # 1) Plank Cleared
    assert app.board == [None] * (app.size * app.size)

    # 2) Flags
    assert app.started is False
    assert app.current == CROSS_SYMBOL
    assert app.bot == NOUGHT_SYMBOL


# on_reset should put all cells in the state:
#   - text == ""
#   - state != "disabled"
def test_on_reset_resets_buttons_state_and_content():
    app = create_app()

    # Simulate: all buttons are pressed/locked
    for (row, col), btn in app.cells.items():
        btn.config(text="X", state="disabled")

    app.on_reset()

    for btn in app.cells.values():
        # Purification Text
        assert btn.cget("text") == ""
        # button not in disabled state
        assert btn.instate(["!disabled"])


# After on_reset:
# - Start button must be active again (not disabled)
# - status resets to the original text
def test_on_reset_enables_start_button_and_updates_status():
    app = create_app()

    # Simulate that the game has been launched and Start is blocked
    app.start_btn.config(state="disabled")
    app.status_var.set("Some old status")

    app.on_reset()

    # Start is active again
    assert app.start_btn.instate(["!disabled"])

    # Status - something like "Select X or O and press Start"
    status = app.status_var.get()
    assert "Start" in status or "start" in status or "Select" in status
