from tictactoe.core.game_logic import GameLogicMixin


# Simple stub for idx testing:
# Set the size and board so that the method can work.
class DummyGame(GameLogicMixin):
    def __init__(self, size=3):
        self.size = size
        self.board = [None] * (size * size)


# (0,0) on a 3x3 board must correspond to the index 0.
def test_idx_top_left():
    game = DummyGame(size=3)
    assert game.idx(0, 0) == 0


# Check the entire top line:
#   (0,0) -> 0
#   (0,1) -> 1
#   (0,2) -> 2
def test_idx_top_row():
    game = DummyGame(size=3)
    assert game.idx(0, 0) == 0
    assert game.idx(0, 1) == 1
    assert game.idx(0, 2) == 2


# For the middle row (row = 1) on a 3x3 board:
#   (1,0) -> 3
#   (1,1) -> 4
#   (1,2) -> 5
# Formula: row * size + col.
def test_idx_middle_row():
    game = DummyGame(size=3)
    assert game.idx(1, 0) == 3
    assert game.idx(1, 1) == 4
    assert game.idx(1, 2) == 5


# (2, 0) -> 6
# (2, 1) -> 7
# (2, 2) -> 8
def test_idx_bottom_row():
    game = DummyGame(size=3)
    assert game.idx(2, 0) == 6
    assert game.idx(2, 1) == 7
    assert game.idx(2, 2) == 8


# For a 3x3 board, all pairs (row,col) 0..2×0..2
# should give unique indices of 0..8 without spaces.
def test_idx_all_cells_unique_for_3x3():
    game = DummyGame(size=3)
    indices = set()

    for row in range(3):
        for col in range(3):
            indices.add(game.idx(row, col))

    # Having all indices from 0 to 8
    assert indices == set(range(9))


# Although it is a 3x3 game now, the idx method itself is universal.
# Let's check that for size=4 everything works according to the same formula.
def test_idx_works_for_other_size_4x4():
    game = DummyGame(size=4)

    # Checking multiple points
    assert game.idx(0, 0) == 0  # first cell
    assert game.idx(0, 3) == 3  # top right corner
    assert game.idx(1, 0) == 4  # the beginning of the second line
    assert game.idx(2, 2) == 10  # middle board 4x4
    assert game.idx(3, 3) == 15  # last cell
