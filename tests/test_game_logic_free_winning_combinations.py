from tictactoe.core.game_logic import GameLogicMixin
from tictactoe.core.constants import CROSS_SYMBOL, NOUGHT_SYMBOL, WINNING_COMBINATIONS


class DummyGame(GameLogicMixin):
    def __init__(self, board):
        self.size = 3
        self.board = board


def test_get_free_winning_combinations_empty_board():
    board = [None] * 9
    game = DummyGame(board)

    combinations_x = game.get_free_winning_combinations(CROSS_SYMBOL)

    # Must return all combinations
    assert len(combinations_x) == len(WINNING_COMBINATIONS)
    # The order does not change (3 None everywhere)
    assert combinations_x == WINNING_COMBINATIONS


def test_get_free_winning_combinations_filters_opponent_lines():
    # Let's arrange O so that it occupies one payline (e.g. (0,1,2))
    board = [
        NOUGHT_SYMBOL, NOUGHT_SYMBOL, None,
        None, None, None,
        None, None, None,
    ]
    game = DummyGame(board)

    combinations_x = game.get_free_winning_combinations(CROSS_SYMBOL)

    # Lines containing O should not be the result of
    assert (0, 1, 2) not in combinations_x

    # Other lines where there is no O should remain
    # For example, (3,4,5) is empty – it should be
    assert (3, 4, 5) in combinations_x


def test_get_free_winning_combinations_sorted_by_none_count():
    # Let's try to make different degrees of occupancy for X
    board = [
        CROSS_SYMBOL, CROSS_SYMBOL, None,  # (0,1,2) – 1 None
        CROSS_SYMBOL, None, None,  # (3,4,5) – 2 None
        None, None, None,  # (6,7,8) – 3 None
    ]
    game = DummyGame(board)

    combinations_x = game.get_free_winning_combinations(CROSS_SYMBOL)

    # Let's restore the number of None for each combination
    none_counts = []
    for a, b, c in combinations_x:
        cells = [board[a], board[b], board[c]]
        none_counts.append(cells.count(None))

    # The number of None must not be decreasing (0,1,2,3,...)
    assert none_counts == sorted(none_counts)


def test_get_free_winning_combinations_for_nought():
    board = [
        CROSS_SYMBOL, CROSS_SYMBOL, None,
        None, NOUGHT_SYMBOL, None,
        None, None, None,
    ]
    game = DummyGame(board)

    combinations_o = game.get_free_winning_combinations(NOUGHT_SYMBOL)

    # Lines with X should be eliminated for O, e.g. (0,1,2)
    assert (0, 1, 2) not in combinations_o

    # Lines where there is no X must be available for O.
    # For example, (2,5,8) - there is only None.
    assert (2, 5, 8) in combinations_o
