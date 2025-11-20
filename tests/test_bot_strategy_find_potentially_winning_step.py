#
# Run all tests: `PYTHONPATH=src pytest -q`
#
from tictactoe.core.bot_strategy import BotStrategyMixin
from tictactoe.core.game_logic import GameLogicMixin
from tictactoe.core.constants import CROSS_SYMBOL, NOUGHT_SYMBOL, CORNERS


# A simple stub for human.get() is simple.
class DummyHuman:
    def __init__(self, symbol):
        self._symbol = symbol

    def get(self):
        return self._symbol


# Minimum class for testing find_potentially_winning_step
# without Tkinter. Provides:
#   - self.size
#   - self.board
#   - self.human.get()
#   - self.bot
class DummyBotGame(GameLogicMixin, BotStrategyMixin):
    def __init__(self, board, human_symbol, bot_symbol):
        self.size = 3
        self.board = board
        self.human = DummyHuman(human_symbol)
        self.bot = bot_symbol


# If the center is free, the bot's first priority is to take cell 4.
def test_bot_takes_center_if_free():
    board = [None] * 9
    game = DummyBotGame(board, human_symbol=CROSS_SYMBOL, bot_symbol=NOUGHT_SYMBOL)

    move = game.find_potentially_winning_step()

    assert move == 4


# User (X) has 2 in a row and one free cell.
# The bot (O) must block this line.
#   X X .
#   . O .
#   . . .
def test_bot_blocks_immediate_user_win_row():
    board = [
        CROSS_SYMBOL, CROSS_SYMBOL, None,
        None, NOUGHT_SYMBOL, None,
        None, None, None,
    ]
    game = DummyBotGame(board, human_symbol=CROSS_SYMBOL, bot_symbol=NOUGHT_SYMBOL)

    move = game.find_potentially_winning_step()

    # The bot must put O at position 2 to lock (0,1,2).
    assert move == 2


# A situation where both the user and the bot have 2 in a line, but
# The bot must prioritize its own victory.
#
#   X X .
#   O O .
#   . . .
#
# For the bot (O), a winning move to position 5 (line 3,4,5).
# For user (X), the threatening string is 0,1,2 (position 2).
# Expecting the bot to choose 5, not 2.
def test_bot_prefers_own_win_over_block():
    board = [
        CROSS_SYMBOL, CROSS_SYMBOL, None,
        NOUGHT_SYMBOL, NOUGHT_SYMBOL, None,
        None, None, None,
    ]
    game = DummyBotGame(board, human_symbol=CROSS_SYMBOL, bot_symbol=NOUGHT_SYMBOL)

    move = game.find_potentially_winning_step()

    assert move == 5


# If the user does not have an immediate threat, and the bot has 2 in the line,
# The bot must make a winning move.
#
#   . . .
#   O O .
#   . . .
def test_bot_wins_when_possible_and_user_not_threatening():
    board = [
        None, None, None,
        NOUGHT_SYMBOL, NOUGHT_SYMBOL, None,
        None, None, None,
    ]
    game = DummyBotGame(board, human_symbol=CROSS_SYMBOL, bot_symbol=NOUGHT_SYMBOL)

    move = game.find_potentially_winning_step()

    # Bot's winning move to position 5 (line 3,4,5)
    assert move == 5


# When there is no immediate victory for either the bot or the user,
# method should return the index of the free cell.
# Do not test a specific strategy (triangles/random),
# invariant only: the move is correct.
#
#   X O X
#   O X .
#   . . O
def test_bot_returns_some_free_cell_when_no_forced_moves():
    board = [
        CROSS_SYMBOL, NOUGHT_SYMBOL, CROSS_SYMBOL,
        NOUGHT_SYMBOL, CROSS_SYMBOL, None,
        None, None, NOUGHT_SYMBOL,
    ]
    game = DummyBotGame(board, human_symbol=CROSS_SYMBOL, bot_symbol=NOUGHT_SYMBOL)

    move = game.find_potentially_winning_step()

    # move must be either None (if the implementation decides to return None on the filled board),
    # or an index within [0..8] per free cell.
    assert move is None or (0 <= move < 9 and board[move] is None)


# Blocking a user threat by column:
#   X . .
#   X O .
#   . . .
# (line 0,3,6 — X X _)
def test_bot_blocks_immediate_user_win_column():
    board = [
        CROSS_SYMBOL, None, None,
        CROSS_SYMBOL, NOUGHT_SYMBOL, None,
        None, None, None,
    ]
    game = DummyBotGame(board, human_symbol=CROSS_SYMBOL, bot_symbol=NOUGHT_SYMBOL)

    move = game.find_potentially_winning_step()

    # The bot must block the combination (0,3,6), i.e. put in 6
    assert move == 6


# Diagonally blocking a user threat:
#   X . .
#   . X O
#   . . .
# (diagonal 0,4,8 — X X _)
def test_bot_blocks_immediate_user_win_diagonal():
    board = [
        CROSS_SYMBOL, None, None,
        None, CROSS_SYMBOL, NOUGHT_SYMBOL,
        None, None, None,
    ]
    game = DummyBotGame(board, human_symbol=CROSS_SYMBOL, bot_symbol=NOUGHT_SYMBOL)

    move = game.find_potentially_winning_step()

    # The bot must block the diagonal (0,4,8), i.e. put in 8
    assert move == 8


# Bot victory by column:
#   . O .
#   . O X
#   X . .
#
# The bot (O) has two in column 1 (1,4,_), must be completed in 7.
def test_bot_wins_on_column_when_possible():
    board = [
        None, NOUGHT_SYMBOL, None,
        None, NOUGHT_SYMBOL, CROSS_SYMBOL,
        CROSS_SYMBOL, None, None,
    ]
    game = DummyBotGame(board, human_symbol=CROSS_SYMBOL, bot_symbol=NOUGHT_SYMBOL)

    move = game.find_potentially_winning_step()

    assert move == 7


# Bot victory diagonally:
#   O X .
#   X O .
#   . . .
#
# The bot (O) has two on a diagonal of 0,4,_ – you need to win with a move of 8.
def test_bot_wins_on_diagonal_when_possible():
    board = [
        NOUGHT_SYMBOL, CROSS_SYMBOL, None,
        CROSS_SYMBOL, NOUGHT_SYMBOL, None,
        None, None, None,
    ]
    game = DummyBotGame(board, human_symbol=CROSS_SYMBOL, bot_symbol=NOUGHT_SYMBOL)

    move = game.find_potentially_winning_step()

    assert move == 8


# ======================================================================
# НОВІ ТЕСТИ: corner-triangular strategies (TRICKY_TRIANGLE_COMBINATIONS_CORNER)
# ======================================================================

# Case: the center is occupied by the user, the bot has not yet walked.
#
#   . . .
#   . X .
#   . . .
#
# The triangle algorithm should choose one of the angles (0,2,6,8) rather than the edge.
def test_bot_corner_triangle_when_center_taken_by_user_picks_corner():
    board = [
        None, None, None,
        None, CROSS_SYMBOL, None,
        None, None, None,
    ]
    game = DummyBotGame(board, human_symbol=CROSS_SYMBOL, bot_symbol=NOUGHT_SYMBOL)

    move = game.find_potentially_winning_step()

    # Must be one of the corners and empty
    assert move in CORNERS
    assert board[move] is None


# Case: the center and one corner are already occupied by the user, the bot has not yet walked.
#
#   X . .
#   . X .
#   . . .
#
# The corner-strategy should still return some free angle (with CORNERS),
# and not a rib.
def test_bot_corner_triangle_when_center_and_one_corner_taken_by_user_picks_other_corner():
    board = [
        CROSS_SYMBOL, None, None,
        None, CROSS_SYMBOL, None,
        None, None, None,
    ]
    game = DummyBotGame(board, human_symbol=CROSS_SYMBOL, bot_symbol=NOUGHT_SYMBOL)

    move = game.find_potentially_winning_step()

    # The angle that is already occupied by the user is 0; We expect another free angle.
    assert move in CORNERS
    assert board[move] is None
    # additionally make sure that the bot has not selected the already occupied 0
    assert move != 0
