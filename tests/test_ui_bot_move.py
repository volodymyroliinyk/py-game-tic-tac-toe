from tictactoe.ui.app import GameApp
from tictactoe.core.constants import CROSS_SYMBOL, NOUGHT_SYMBOL


# Create a GameApp instance without mainloop,
# hide the window and jam all PNGs to avoid problems with Tk PhotoImage.
def create_app():
    app = GameApp()
    app.withdraw()

    # In tests, interested in logic, not real images.
    app.cross_img_black = ""
    app.nought_img_black = ""
    app.cross_img_green = ""
    app.nought_img_green = ""

    return app


# If the game has not started yet (started == False),
# bot_move should not change the board.
def test_bot_move_does_nothing_if_not_started():
    app = create_app()

    app.started = False
    app.current = app.bot  # even if "bot move"

    before = app.board.copy()
    app.bot_move()
    assert app.board == before


# If it's not the bot's turn right now (current != bot),
# bot_move does nothing.
def test_bot_move_does_nothing_if_not_bots_turn():
    app = create_app()

    app.started = True
    app.human.set(CROSS_SYMBOL)
    app.bot = NOUGHT_SYMBOL
    app.current = app.human.get()  # human move

    before = app.board.copy()
    app.bot_move()
    assert app.board == before


# If find_potentially_winning_step returns an index, the bot must
# make a move to this particular cell, and then pass the move to a person.
def test_bot_move_uses_find_potentially_winning_step_when_available():
    app = create_app()

    app.started = True
    app.human.set(CROSS_SYMBOL)
    app.bot = NOUGHT_SYMBOL
    app.current = app.bot

    # All board is empty
    assert all(v is None for v in app.board)

    # Patching the strategy so that it returns a specific index
    target_index = 5
    app.find_potentially_winning_step = lambda: target_index

    app.bot_move()

    # The bot put its symbol in the target_index
    assert app.board[target_index] == NOUGHT_SYMBOL

    # The move goes to the person
    assert app.current == app.human.get() == CROSS_SYMBOL

    # The game is still in progress (no win/draw), started remains True
    assert app.started is True


# If find_potentially_winning_step returns None,
# The bot should occupy the first free cell from left to right.
def test_bot_move_falls_back_to_first_free_cell_if_no_smart_step():
    app = create_app()

    app.started = True
    app.human.set(CROSS_SYMBOL)
    app.bot = NOUGHT_SYMBOL
    app.current = app.bot

    # Let's take a few cells so that the first free one is not 0
    app.board = [
        CROSS_SYMBOL, NOUGHT_SYMBOL, CROSS_SYMBOL,
        None, None, None,
        None, None, None,
    ]

    # The strategy did not find a smart move
    app.find_potentially_winning_step = lambda: None

    app.bot_move()

    # The first free cell is index 3
    assert app.board[3] == NOUGHT_SYMBOL
    assert app.current == app.human.get() == CROSS_SYMBOL
    assert app.started is True


# If the bot's move creates a 3 in a row, bot_move should:
# - put the bot symbol in the desired cell;
# - call end_game (the game stops);
# - update the status to "Bot WINS" (or with this text inside).
def test_bot_move_winning_step_ends_game():
    app = create_app()

    app.started = True
    app.human.set(NOUGHT_SYMBOL)
    app.bot = CROSS_SYMBOL
    app.current = app.bot

    # State before the winning move:
    # X X .
    # . . .
    # . . .
    app.board = [
        CROSS_SYMBOL, CROSS_SYMBOL, None,
        None, None, None,
        None, None, None,
    ]

    # The strategy returns exactly the winning index 2
    app.find_potentially_winning_step = lambda: 2

    app.bot_move()

    # Making sure the line is complete
    assert app.board[2] == CROSS_SYMBOL

    # Game Over
    assert app.started is False

    status = app.status_var.get()
    assert "Bot WINS" in status

    # All cells are locked
    for btn in app.cells.values():
        assert btn.instate(["disabled"])


# If there is one empty cell left on the board, and the bot occupies it
# without forming a 3 in a row, a draw (TIE) must be recorded.
def test_bot_move_last_free_cell_makes_tie():
    app = create_app()

    app.started = True
    app.human.set(CROSS_SYMBOL)
    app.bot = NOUGHT_SYMBOL
    app.current = app.bot

    # Condition before a draw:
    # X O X
    # X O O
    # O X .
    app.board = [
        CROSS_SYMBOL, NOUGHT_SYMBOL, CROSS_SYMBOL,
        CROSS_SYMBOL, NOUGHT_SYMBOL, NOUGHT_SYMBOL,
        NOUGHT_SYMBOL, CROSS_SYMBOL, None,
    ]

    # Let the strategy not offer a "smart" move (None),
    # The bot will use Fallback and occupy the last cell (index 8).
    app.find_potentially_winning_step = lambda: None

    app.bot_move()

    # Cell 8 must be occupied by the bot
    assert app.board[8] == NOUGHT_SYMBOL

    # End of the game
    assert app.started is False

    status = app.status_var.get()
    assert "TIE" in status or "Tie" in status
