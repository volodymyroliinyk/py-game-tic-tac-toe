# /src/tictactoe/core/bot_strategy.py

########################################################################################################################
#
#
#
########################################################################################################################

# Smart Bot
# How to find free cell just around first one?
# How to find how to find 3rd cell if two nearest already don ?
# How to fut third X or 0 between two first

# How to predict the next step, second and third steps?
#  012 0?? ?1? ??2 ..? ?.? .?. ?.? ?.. .?.
#  345 ??. .?. .?? ??5 .?? .?. ??. 3?? ?4?
#  678 ?.? .?. ?.? ..? ??8 ?7? 6?? ?.. .?.

# The easiest way to check if each winning combination have combination like
# None, X, None
# X, None, None
# None, None, X
#
# None, 0, None
# 0, None, None
# None, None, 0

# Need build Method which can check in an array of three elements that it has contains:
# 1) all three elements are None and stop and output it.
# 2) one X|0 and two other elements None, in any sequence stop at the first combination and output it
# 3) two X|0 and one None element, in any sequence stop on it and output it


import random
from .game_logic import WINNING_COMBINATIONS

# Tricky triangle strategy
#  012 0.? 0?2 ?.2 ?.?
#  345 ?4. .4. .4? .4.
#  678 6.? ?.? ?.8 6?8

# WINNING_COMBINATIONS = [
#     (0, 1, 2),
#     (3, 4, 5),
#     (6, 7, 8),
#     (0, 3, 6),
#     (1, 4, 7),
#     (2, 5, 8),
#     (0, 4, 8),
#     (2, 4, 6),
# ]

TRICKY_TRIANGLE_COMBINATIONS = [
    (0, 4, 6),  # Need to check if is free: 2,3,8 | Winning lines for this triangle: 048 OR 246 OR 036
    (0, 4, 2),  # Need to check if is free: 1,6,8 | Winning lines for this triangle: 048 OR 246 OR 042
    (2, 4, 8),  # Need to check if is free: 0,5,6 | Winning lines for this triangle: 048 OR 246 OR 258
    (6, 4, 8),  # Need to check if is free: 0,2,7 | Winning lines for this triangle: 048 OR 246 OR 678
]


class BotStrategyMixin:
    # Must be used just for a Bot.
    def find_potentially_winning_step(self):
        # The best is to take the center of the board first for Bot
        if self.board[4] is None:
            return 4
        # if condition end.

        # First loop for prevent User's win
        # Done:[1]: The bot must prevent the user from winning, that is, it must see the user's progress and prevent him.
        for winning_combination in WINNING_COMBINATIONS:
            values = [self.board[index] for index in winning_combination]
            none_count = values.count(None)
            human_symbol_count = values.count(self.human.get())  # for prevent user's win
            #
            if human_symbol_count == 2 and none_count == 1:
                free_index = values.index(None)
                return winning_combination[free_index]
            # if condition end.
        # for loop end.

        # TODO:[1]: Need to implement tricky triangle strategy.
        # Play with that TRICKY_TRIANGLE_COMBINATIONS

        # Second loop for smart bot step
        for winning_combination in WINNING_COMBINATIONS:
            values = [self.board[index] for index in winning_combination]
            own_symbol_count = values.count(self.bot)
            none_count = values.count(None)

            if own_symbol_count == 2 and none_count == 1:
                free_index = values.index(None)
                return winning_combination[free_index]
            elif own_symbol_count == 1 and none_count == 2:
                free_indices = [winning_combination[i] for i, v in enumerate(values) if v is None]
                return random.choice(free_indices)
            elif own_symbol_count == 0 and none_count == 3:
                # Done:[1]: Maybe need to remove 4 from this list because Bot already took that as first condition in this method
                for x in [1, 3, 5, 7]:
                    if x in winning_combination:
                        return x
                    # if condition end.
                # for condition end.

                return random.choice(winning_combination)
            # if condition end.
        # for loop end.

        return None
    # Method "find_potentially_winning_step" end.
