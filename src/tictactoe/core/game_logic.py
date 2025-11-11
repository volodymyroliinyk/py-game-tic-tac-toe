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

WINNING_COMBINATIONS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


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
