# /src/tictactoe/core/game_logic.py

from ..core.constants import WINNING_COMBINATIONS
from ..core.constants import CROSS_SYMBOL
from ..core.constants import NOUGHT_SYMBOL
from ..core.constants import TRICKY_TRIANGLE_COMBINATIONS_BIG
from ..core.constants import TRIANGLE_TO_LINES_BIG
from ..core.constants import TRICKY_TRIANGLE_COMBINATIONS_SMALL
from ..core.constants import TRIANGLE_TO_LINES_SMALL
from ..core.constants import TRICKY_TRIANGLE_COMBINATIONS_CORNER
from ..core.constants import TRIANGLE_TO_LINES_CORNER

class GameLogicMixin:
    # Convert to one-dimensional list? return index 0-8.
    def idx(self, row, col):
        return row * self.size + col
    # Method "idx" end.

    # Checking current board state if contains winning combination.
    def check_winner(self):
        # Checking each combination and compair with cells.
        for winning_combination in WINNING_COMBINATIONS:
            cell1 = self.board[winning_combination[0]]
            cell2 = self.board[winning_combination[1]]
            cell3 = self.board[winning_combination[2]]

            # All cells must be the same and not equal None.
            if cell1 is not None and cell1 == cell2 and cell1 == cell3:
                return cell1  # Returns Player or Bot symbol.
            # Condition "if" end.
        # Loop "for" end.

        return None
    # Method "check_winner" end.

    # Getting free winning combinations from WINNING_COMBINATIONS for X or for O.
    def get_free_winning_combinations(self, symbol):
        if symbol == CROSS_SYMBOL:
            opponent = NOUGHT_SYMBOL
        else:
            opponent = CROSS_SYMBOL
        # Condition "if" end.

        free_lines = []

        for winning_combination in WINNING_COMBINATIONS:
            a, b, c = winning_combination
            tri_cells = [self.board[a], self.board[b], self.board[c]]

            # If there is an opponent in a line, the line is busy.
            if opponent in tri_cells:
                continue
            # Condition "if" end.

            free_lines.append((winning_combination, tri_cells))
        # Loop "for" end.

        # Sorting, combinations with a less None on the start.
        free_lines.sort(key=lambda item: item[1].count(None))

        # Return only combinations, without tri_cells.
        return [combination for combination, _ in free_lines]
    #  Method "get_free_winning_combinations" end.

    def get_free_tricky_triangles_common(self, symbol, tricky_triangle_combinations, triangle_to_lines):
        if symbol == CROSS_SYMBOL:
            opponent = NOUGHT_SYMBOL
        else:
            opponent = CROSS_SYMBOL
        # Condition "if" end.

        # Take all free winning lines for symbol.
        free_lines = set(self.get_free_winning_combinations(symbol))

        valid_triangles = []

        for triangle in tricky_triangle_combinations:
            a, mid, c = triangle
            tri_cells = [self.board[a], self.board[mid], self.board[c]]

            # If there is an opponent in a triangle, the triangle is busy.
            if opponent in tri_cells:
                continue
            # Condition "if" end.

            # Check all its related lines.
            related_lines = triangle_to_lines.get(triangle, [])

            # All three lines must be free.
            if all(line in free_lines for line in related_lines):
                valid_triangles.append(triangle)
            # Condition "if" end.
        # Loop "for" end.

        return valid_triangles

    #  Method "get_free_tricky_triangles_big" end.

    # Returns all triangles that can still be used to create a fork:
    # - there are no opponent pieces in the triangle
    # - all related paylines are also free (do not contain an opponent).
