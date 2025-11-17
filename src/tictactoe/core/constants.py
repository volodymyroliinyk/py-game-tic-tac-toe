# /src/tictactoe/core/constants.py

# TODO:[2]: use images instead of symbols.
CROSS_SYMBOL = "X"
NOUGHT_SYMBOL = "O"

# TODO:[2]: need to find normal images.
# Regular images.
CROSS_IMG_BLACK = "assets/images/CROSS_BLACK.png"
NOUGHT_IMG_BLACK = "assets/images/NOUGHT_BLACK.png"

# Winning images.
CROSS_IMG_GREEN = "assets/images/CROSS_GREEN.png"
NOUGHT_IMG_GREEN = "assets/images/NOUGHT_GREEN.png"

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


# CORNER in (0, 2, 6, 8)
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

# CORNER in (0, 2, 6, 8)
# Especial combination which can help to winn 100%. Big triangles.
TRICKY_TRIANGLE_COMBINATIONS_BIG = [
    # Big.
    # Important! corner cell always first with index 0.
    # Important! board center cell always second with index 1.
    (0, 4, 6),  # Need to check if is free: 2,3,8 | Winning lines for this triangle: 048 OR 246 OR 036
    (0, 4, 2),  # Need to check if is free: 1,6,8 | Winning lines for this triangle: 048 OR 246 OR 012
    (2, 4, 8),  # Need to check if is free: 0,5,6 | Winning lines for this triangle: 048 OR 246 OR 258
    (6, 4, 8),  # Need to check if is free: 0,2,7 | Winning lines for this triangle: 048 OR 246 OR 678
]

TRIANGLE_TO_LINES_BIG = {
    (0, 4, 6): [(0, 4, 8), (2, 4, 6), (0, 3, 6)],
    (0, 4, 2): [(0, 4, 8), (2, 4, 6), (0, 1, 2)],
    (2, 4, 8): [(0, 4, 8), (2, 4, 6), (2, 5, 8)],
    (6, 4, 8): [(0, 4, 8), (2, 4, 6), (6, 7, 8)],
}

# CORNER in (0, 2, 6, 8)
# Especial combination which can help to winn 100%, but triangle is another one. Small triangles.
TRICKY_TRIANGLE_COMBINATIONS_SMALL = [
    # Small.
    # Important! corner cell always first with index 0.
    # Important! board center cell always second with index 1.
    (0, 4, 1),
    (2, 4, 1),
    (2, 4, 5),
    (8, 4, 5),
    (8, 4, 7),
    (6, 4, 7),
    (6, 4, 3),
    (0, 4, 3),
]

TRIANGLE_TO_LINES_SMALL = {
    (0, 4, 1): [(0, 1, 2), (0, 4, 8)],
    (2, 4, 1): [(0, 1, 2), (2, 4, 6)],
    (2, 4, 5): [(2, 5, 8), (0, 4, 2)],
    (8, 4, 5): [(2, 5, 8), (0, 4, 8)],
    (7, 4, 8): [(6, 7, 8), (0, 4, 8)],
    (7, 4, 6): [(6, 7, 8), (2, 4, 6)],
    (6, 4, 3): [(3, 4, 5), (0, 3, 6)],
    (0, 4, 3): [(3, 4, 5), (0, 3, 6)],
}

# TODO:[1] I found one more TRICKY_TRIANGLE_COMBINATIONS, need to implement for bot strategies, but if bot not occupied board center, bot can win!
# example
# 1:O 2:X X
# 3:O 1:X
# 2:O 2:O 3:X
