from tictactoe.core.game_logic import GameLogicMixin
from tictactoe.core.constants import (
    TRICKY_TRIANGLE_COMBINATIONS_BIG, TRIANGLE_TO_LINES_BIG,
    TRICKY_TRIANGLE_COMBINATIONS_SMALL, TRIANGLE_TO_LINES_SMALL,
    TRICKY_TRIANGLE_COMBINATIONS_CORNER, TRIANGLE_TO_LINES_CORNER,
    CROSS_SYMBOL,
    NOUGHT_SYMBOL,
)


class DummyGame(GameLogicMixin):
    def __init__(self, board):
        # 3×3 Board
        self.size = 3
        # list of length 9: [None, "X", "O", ...]
        self.board = board


def test_tricky_big_all_free_on_empty_board():
    game = DummyGame(board=[None] * 9)

    result = game.get_free_tricky_triangles_common(CROSS_SYMBOL, TRICKY_TRIANGLE_COMBINATIONS_BIG,
                                                   TRIANGLE_TO_LINES_BIG)

    # All major triangles must be available
    assert set(result) == set(TRICKY_TRIANGLE_COMBINATIONS_BIG)


def test_tricky_big_exclude_if_opponent_in_triangle():
    # O put the 6th triangle at the vertex (0,4,6)
    board = [None] * 9
    board[4] = CROSS_SYMBOL  # our symbol
    board[6] = NOUGHT_SYMBOL  # Oponent

    game = DummyGame(board)

    result = game.get_free_tricky_triangles_common(CROSS_SYMBOL, TRICKY_TRIANGLE_COMBINATIONS_BIG,
                                                   TRIANGLE_TO_LINES_BIG)

    assert (0, 4, 6) not in result


def test_tricky_big_exclude_if_related_line_blocked():
    # X in the center, O at 8 - line (0,4,8) is blocked
    board = [None] * 9
    board[4] = CROSS_SYMBOL  # our symbol
    board[8] = NOUGHT_SYMBOL  # opponent blocks the line (0,4,8)

    game = DummyGame(board)

    result = game.get_free_tricky_triangles_common(CROSS_SYMBOL, TRICKY_TRIANGLE_COMBINATIONS_BIG,
                                                   TRIANGLE_TO_LINES_BIG)

    # triangle (0,4,6) must be excluded because one connected line is no longer free
    assert (0, 4, 6) not in result


def test_tricky_big_mixed_valid_and_invalid():
    board = [None] * 9
    board[4] = CROSS_SYMBOL  # our symbol in the center
    board[1] = NOUGHT_SYMBOL  # opponent blocks the line (0,1,2)

    game = DummyGame(board)

    result = game.get_free_tricky_triangles_common(CROSS_SYMBOL, TRICKY_TRIANGLE_COMBINATIONS_BIG,
                                                   TRIANGLE_TO_LINES_BIG)

    # (0,4,2) should be excluded
    assert (0, 4, 2) not in result
    # But some other triangle (e.g. (2,4,8)) may still be in the list
    assert (2, 4, 8) in TRICKY_TRIANGLE_COMBINATIONS_BIG


def test_tricky_big_for_nought_symbol():
    # Mirrored: Now play O
    board = [None] * 9
    board[4] = NOUGHT_SYMBOL  # our symbol
    # opponent X is not standing anywhere yet

    game = DummyGame(board)

    result = game.get_free_tricky_triangles_common(NOUGHT_SYMBOL, TRICKY_TRIANGLE_COMBINATIONS_BIG,
                                                   TRIANGLE_TO_LINES_BIG)

    assert set(result) == set(TRICKY_TRIANGLE_COMBINATIONS_BIG)


#################################################################################################################

def test_tricky_small_all_free_on_empty_board():
    board = [None] * 9
    game = DummyGame(board)

    result = game.get_free_tricky_triangles_common(
        CROSS_SYMBOL,
        TRICKY_TRIANGLE_COMBINATIONS_SMALL,
        TRIANGLE_TO_LINES_SMALL,
    )

    # On a blank board, all small triangles must be available
    assert set(result) == set(TRICKY_TRIANGLE_COMBINATIONS_SMALL)


# Board:
#   0 1 2
#   3 4 5
#   6 7 8
#
# X in the center (4), O on 1 and 7.
# Expectations (calculate according to real logic):
#
# free_lines for X: (3,4,5), (0,3,6), (2,5,8), (0,4,8), (2,4,6)
#
# Checking each small-triangle shows that the free:
#   (2, 4, 5), (8, 4, 5), (6, 4, 3), (0, 4, 3)
def test_tricky_small_mixed_valid_and_invalid():
    board = [None] * 9
    board[4] = CROSS_SYMBOL  # our symbol in the center
    board[1] = NOUGHT_SYMBOL  # Oponent
    board[7] = NOUGHT_SYMBOL  # Oponent
    game = DummyGame(board)

    result = game.get_free_tricky_triangles_common(
        CROSS_SYMBOL,
        TRICKY_TRIANGLE_COMBINATIONS_SMALL,
        TRIANGLE_TO_LINES_SMALL,
    )

    expected = {
        (2, 4, 5),
        (8, 4, 5),
        (6, 4, 3),
        (0, 4, 3),
    }

    assert set(result) == expected

    # Optional Invariant: No opponent's piece should be in any triangle
    opponent = NOUGHT_SYMBOL
    for a, mid, c in result:
        tri_cells = [board[a], board[mid], board[c]]
        assert opponent not in tri_cells


# Script for O:
#
#   X . .
#   . O .
#   . . .
#
# - opponent X is in cell 0;
# - no small triangle containing 0 should be in the result;
# - triangle (2,4,5) must be valid;
# - no resulting triangle should contain X nor at the vertices themselves,
# no on the support lines.
def test_tricky_small_for_nought_symbol():
    board = [None] * 9
    board[4] = NOUGHT_SYMBOL  # our O symbol
    board[0] = CROSS_SYMBOL  # opponent X
    game = DummyGame(board)

    result = game.get_free_tricky_triangles_common(
        NOUGHT_SYMBOL,
        TRICKY_TRIANGLE_COMBINATIONS_SMALL,
        TRIANGLE_TO_LINES_SMALL,
    )

    # 1) specific positive expectation: (2,4,5) should be the result
    assert (2, 4, 5) in result

    # 2) triangles containing cell 0 (where X stands) should not appear
    assert (0, 4, 1) not in result
    assert (0, 4, 3) not in result

    # 3) invariant: no triangle has an X at the vertices
    opponent = CROSS_SYMBOL
    for a, mid, c in result:
        tri_cells = [board[a], board[mid], board[c]]
        assert opponent not in tri_cells

        # 4) invariant: no support line of a triangle contains an X
        for line in TRIANGLE_TO_LINES_SMALL.get((a, mid, c), []):
            vals = [board[i] for i in line]
            assert opponent not in vals


###############################################################################################################

def test_tricky_corner_all_free_on_empty_board():
    game = DummyGame(board=[None] * 9)

    result = game.get_free_tricky_triangles_common(
        CROSS_SYMBOL,
        TRICKY_TRIANGLE_COMBINATIONS_CORNER,
        TRIANGLE_TO_LINES_CORNER,
    )

    # All corner triangles must be available on a blank board
    assert set(result) == set(TRICKY_TRIANGLE_COMBINATIONS_CORNER)


def test_tricky_corner_exclude_if_opponent_in_triangle():
    # Let's take the triangle (0, 6, 7) and put the opponent at one of the vertices (6)
    board = [None] * 9
    board[6] = NOUGHT_SYMBOL  # opponent for X

    game = DummyGame(board)

    result = game.get_free_tricky_triangles_common(
        CROSS_SYMBOL,
        TRICKY_TRIANGLE_COMBINATIONS_CORNER,
        TRIANGLE_TO_LINES_CORNER,
    )

    # Any triangle containing 6 must be excluded (check specifically (0,6,7))
    assert (0, 6, 7) not in result


def test_tricky_corner_exclude_if_related_line_blocked():
    # For the triangle (0, 6, 7), the lines are connected: (0,3,6) and (6,7,8)
    # Block the line (0,3,6) by the opponent in cell 3
    board = [None] * 9
    board[3] = NOUGHT_SYMBOL  # opponent for X

    game = DummyGame(board)

    result = game.get_free_tricky_triangles_common(
        CROSS_SYMBOL,
        TRICKY_TRIANGLE_COMBINATIONS_CORNER,
        TRIANGLE_TO_LINES_CORNER,
    )

    # There is no opponent in the triangle itself (0,6,7), but one of the connected lines is not free
    assert (0, 6, 7) not in result


def test_tricky_corner_mixed_valid_and_invalid():
    # The opponent stands in 3, as in the previous test
    # => triangle (0,6,7) must be invalid (across the line (0,3,6))
    # but the triangle (2,8,7) can still be valid,
    # because its lines: (2,5,8) and (6,7,8) do not contain cell 3.
    board = [None] * 9
    board[3] = NOUGHT_SYMBOL  # opponent for X

    game = DummyGame(board)

    result = game.get_free_tricky_triangles_common(
        CROSS_SYMBOL,
        TRICKY_TRIANGLE_COMBINATIONS_CORNER,
        TRIANGLE_TO_LINES_CORNER,
    )

    assert (0, 6, 7) not in result
    assert (2, 8, 7) in result


def test_tricky_corner_for_nought_symbol():
    # Now play O, only our symbol is on the board (in the center, which is not included in any corner triangle)
    board = [None] * 9
    board[4] = NOUGHT_SYMBOL  # our symbol, but the center is not included in the corner triangles

    game = DummyGame(board)

    result = game.get_free_tricky_triangles_common(
        NOUGHT_SYMBOL,
        TRICKY_TRIANGLE_COMBINATIONS_CORNER,
        TRIANGLE_TO_LINES_CORNER,
    )

    # Since neither triangles nor connected lines have an opponent X,
    # All corner triangles must be available.
    assert set(result) == set(TRICKY_TRIANGLE_COMBINATIONS_CORNER)
