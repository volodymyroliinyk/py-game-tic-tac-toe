# TODO:[1]: use images instead of symbols.
CROSS_SYMBOL = "X"
NOUGHT_SYMBOL = "O"

# Just all possible winning combinations.
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

# Especial combination which can help to winn 100%.
TRICKY_TRIANGLE_COMBINATIONS = [
    (0, 4, 6),  # Need to check if is free: 2,3,8 | Winning lines for this triangle: 048 OR 246 OR 036
    (0, 4, 2),  # Need to check if is free: 1,6,8 | Winning lines for this triangle: 048 OR 246 OR 012
    (2, 4, 8),  # Need to check if is free: 0,5,6 | Winning lines for this triangle: 048 OR 246 OR 258
    (6, 4, 8),  # Need to check if is free: 0,2,7 | Winning lines for this triangle: 048 OR 246 OR 678
]
