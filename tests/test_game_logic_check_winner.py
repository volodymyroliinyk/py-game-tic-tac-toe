from tictactoe.core.game_logic import GameLogicMixin
from tictactoe.core.constants import CROSS_SYMBOL, NOUGHT_SYMBOL


class DummyGame(GameLogicMixin):
    def __init__(self, board):
        self.size = 3
        self.board = board


def test_check_winner_x_row():
    # X X X
    # . . .
    # . . .
    board = [
        CROSS_SYMBOL, CROSS_SYMBOL, CROSS_SYMBOL,
        None, None, None,
        None, None, None,
    ]
    game = DummyGame(board)

    assert game.check_winner() == CROSS_SYMBOL


def test_check_winner_o_diagonal():
    # O . .
    # . O .
    # . . O
    board = [
        NOUGHT_SYMBOL, None, None,
        None, NOUGHT_SYMBOL, None,
        None, None, NOUGHT_SYMBOL,
    ]
    game = DummyGame(board)

    assert game.check_winner() == NOUGHT_SYMBOL


def test_check_winner_none_when_no_winner():
    # X O X
    # X O O
    # O X X   (there are no 3 identical in a row anywhere)
    board = [
        "X", "O", "X",
        "X", "O", "O",
        "O", "X", "X",
    ]
    game = DummyGame(board)

    assert game.check_winner() is None


def test_check_winner_none_when_game_not_finished():
    # X O .
    # . X .
    # . . .
    board = [
        "X", "O", None,
        None, "X", None,
        None, None, None,
    ]
    game = DummyGame(board)

    assert game.check_winner() is None
