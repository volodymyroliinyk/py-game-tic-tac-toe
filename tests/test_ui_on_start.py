from tictactoe.ui.app import GameApp
from tictactoe.core.constants import CROSS_SYMBOL, NOUGHT_SYMBOL


# Create a GameApp instance without mainloop,
# hide the window and jam all PNGs to avoid problems with Tk PhotoImage.
def create_app():
    app = GameApp()
    app.withdraw()

    # In tests, interested in logic, not real images.
    # To prevent render()/end_game/on_start from crashing on image "pyimageXX doesn't exist",
    # Replace all sprites with "empty" values.
    app.cross_img_black = ""
    app.nought_img_black = ""
    app.cross_img_green = ""
    app.nought_img_green = ""

    return app


# When the user has chosen X and the bot = O:
#
# - the game enters the started state == True;
# - current must be X (human move);
# - Start remains active (on_start does not block it);
# - the bot does not make the first move (the center remains None).
def test_on_start_with_human_cross_starts_game_and_does_not_move_bot():
    app = create_app()

    # Initialize the "pure" state
    app.on_reset()

    app.human.set(CROSS_SYMBOL)
    app.bot = NOUGHT_SYMBOL

    # Before the start, the board is empty
    assert all(v is None for v in app.board)

    app.on_start()

    # The game has started
    assert app.started is True

    # The current player is a person with X
    assert app.human.get() == CROSS_SYMBOL
    assert app.current == CROSS_SYMBOL
    assert app.bot == NOUGHT_SYMBOL

    # on_start in your implementation does NOT block Start
    assert app.start_btn.instate(["!disabled"])

    # The bot should not make the first move – the center is still empty
    assert app.board[4] is None


# When the user has chosen O and the bot = X:
#
# - the game enters the started state == True;
# - on_start immediately causes bot_move() (not through after);
# - the bot makes the first move to the center (index 4);
# - the current player after the bot's turn is a person (O);
# - Start remains active (on_start does not block it).
def test_on_start_with_human_nought_bot_moves_first_to_center():
    app = create_app()

    # Clean state
    app.on_reset()

    app.human.set(NOUGHT_SYMBOL)
    app.bot = CROSS_SYMBOL

    # Before the start, the board is empty
    assert all(v is None for v in app.board)

    app.on_start()

    # The game has started
    assert app.started is True

    # on_start in your code calls bot_move() directly:
    # if self.human.get() == NOUGHT_SYMBOL: self.bot_move()
    # so the center should be occupied by the bot (X)
    assert app.board[4] == CROSS_SYMBOL

    # Then the turn goes to the person (O)
    assert app.current == NOUGHT_SYMBOL
    assert app.human.get() == NOUGHT_SYMBOL
    assert app.bot == CROSS_SYMBOL

    # Start is NOT blocked on_start
    assert app.start_btn.instate(["!disabled"])
