# /src/tictactoe/core/game_logic.py

# Winning combinations for X
# XXX 000 000 X00 0X0 00X X00 00X
# 000 XXX 000 X00 0X0 00X 0X0 0X0
# 000 000 XXX X00 0X0 00X 00X X00

# Winning combinations for 0
# 000 XXX XXX 0XX X0X XX0 0XX XX0
# XXX 000 XXX 0XX X0X XX0 X0X X0X
# XXX XXX 000 0XX X0X XX0 XX0 0XX

# Indexes
#  0 1 2
#  3 4 5
#  6 7 8

# Winning combinations for indexes
# 012, 345, 678, 036, 147, 258, 048, 246

from ..core.constants import WINNING_COMBINATIONS
from ..core.constants import CROSS_SYMBOL
from ..core.constants import NOUGHT_SYMBOL
from ..core.constants import TRICKY_TRIANGLE_COMBINATIONS_BIG
from ..core.constants import TRICKY_TRIANGLE_COMBINATIONS_SMALL

class GameLogicMixin:
    # Convert to one-dimensional list? return index 0-8
    def idx(self, row, col):
        return row * self.size + col

    # Method "idx" end.

    # Checking current board state if contains winning combination
    def check_winner(self):
        # Checking each combination and compair with cells
        for winning_combination in WINNING_COMBINATIONS:
            cell1 = self.board[winning_combination[0]]
            cell2 = self.board[winning_combination[1]]
            cell3 = self.board[winning_combination[2]]

            # All cells must be the same and not equal None
            if cell1 is not None and cell1 == cell2 and cell1 == cell3:
                return cell1  # returns Player or Bot symbol
            # if condition end.
        # for loop end.

        return None
    # Method "check_winner" end.

    # Getting free winning combinations from WINNING_COMBINATIONS for X or for O
    def get_free_winning_combinations(self, symbol):
        if symbol == CROSS_SYMBOL:
            opponent = NOUGHT_SYMBOL
        else:
            opponent = CROSS_SYMBOL

        free_lines = []

        for winning_combination in WINNING_COMBINATIONS:
            a, b, c = winning_combination
            tri_cells = [self.board[a], self.board[b], self.board[c]]

            # 1) If there is an opponent in a line, the line is busy
            if opponent in tri_cells:
                continue

            free_lines.append(winning_combination)

        return free_lines

    # Returns all triangles that can still be used to create a fork:
    # - there are no opponent pieces in the triangle
    # - all related paylines are also free (do not contain an opponent)
    def get_free_tricky_triangles_big(self, symbol):

        if symbol == CROSS_SYMBOL:
            opponent = NOUGHT_SYMBOL
        else:
            opponent = CROSS_SYMBOL

        # 1) Take all free winning lines for symbol
        free_lines = set(self.get_free_winning_combinations(symbol))

        # 2) Map: Each triangle -> associated paylines
        TRIANGLE_TO_LINES = {
            (0, 4, 6): [(0, 4, 8), (2, 4, 6), (0, 3, 6)],
            (0, 4, 2): [(0, 4, 8), (2, 4, 6), (0, 1, 2)],
            (2, 4, 8): [(0, 4, 8), (2, 4, 6), (2, 5, 8)],
            (6, 4, 8): [(0, 4, 8), (2, 4, 6), (6, 7, 8)],
        }

        valid_triangles = []

        for triangle in TRICKY_TRIANGLE_COMBINATIONS_BIG:
            a, mid, c = triangle
            tri_cells = [self.board[a], self.board[mid], self.board[c]]

            # 1) If there is an opponent in a triangle, the triangle is busy
            if opponent in tri_cells:
                continue

            # 2) Check all its related lines
            related_lines = TRIANGLE_TO_LINES.get(triangle, [])

            # all lines must be free
            if all(line in free_lines for line in related_lines):
                valid_triangles.append(triangle)

        return valid_triangles

    def get_free_tricky_triangles_small(self, symbol):
        if symbol == CROSS_SYMBOL:
            opponent = NOUGHT_SYMBOL
        else:
            opponent = CROSS_SYMBOL

        # take all free paylines as a set
        free_lines = set(self.get_free_winning_combinations(symbol))

        # map triangle → only 2 matching paylines
        TRIANGLE_TO_LINES_2 = {
            (0, 4, 1): [(0, 1, 2), (0, 4, 8)],
            (2, 4, 1): [(0, 1, 2), (2, 4, 6)],
            (2, 4, 5): [(2, 5, 8), (0, 4, 2)],
            (8, 4, 5): [(2, 5, 8), (0, 4, 8)],
            (7, 4, 8): [(6, 7, 8), (0, 4, 8)],
            (7, 4, 6): [(6, 7, 8), (2, 4, 6)],
            (6, 4, 3): [(3, 4, 5), (0, 3, 6)],
            (0, 4, 3): [(3, 4, 5), (0, 3, 6)],
        }

        valid_triangles = []

        for triangle in TRICKY_TRIANGLE_COMBINATIONS_SMALL:
            a, mid, c = triangle
            tri_cells = [self.board[a], self.board[mid], self.board[c]]

            # if there is an opponent in the triangle itself - he is busy
            if opponent in tri_cells:
                continue

            # Take a list of related lines
            related_lines = TRIANGLE_TO_LINES_2.get(triangle, [])

            # These two lines must be "alive"
            if all(line in free_lines for line in related_lines):
                valid_triangles.append(triangle)

        return valid_triangles
