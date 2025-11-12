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

# Tricky triangle strategy steps:
# 1) This strategy can be successful if the Bot has already taken a center [4]
# 2) After [4] need to find a free one from the four angle cells [0],[2],[6],[8]
# 3) Find TRIANGLEs which are related to [4][0] OR [4][2] OR [4][6] OR [4][8]
# 4) Take the first free angle cell related to one of the TRIANGLEs
# 5) Last step is already provided by existing logic.

TRICKY_TRIANGLE_COMBINATIONS = [
    (0, 4, 6),  # Need to check if is free: 2,3,8 | Winning lines for this triangle: 048 OR 246 OR 036
    (0, 4, 2),  # Need to check if is free: 1,6,8 | Winning lines for this triangle: 048 OR 246 OR 012
    (2, 4, 8),  # Need to check if is free: 0,5,6 | Winning lines for this triangle: 048 OR 246 OR 258
    (6, 4, 8),  # Need to check if is free: 0,2,7 | Winning lines for this triangle: 048 OR 246 OR 678
]


# TODO:[1]:
#  Manual and automated testing strategies:
#  Cases:
#  1) Bot in the center
#  2) User in the center
#  3) Need to test how smart the bot is in its quest to win.
#  4) Need to test how smart the bot is to prevent the user from winning.
#  5) Need to test how smart the bot is to balance between 3 and 4.

class BotStrategyMixin:
    # Must be used just for a Bot.
    def find_potentially_winning_step(self):
        # The best is to take the center of the board first for Bot.
        # OR
        # Tricky triangle strategy, step 1.
        if self.board[4] is None:
            print("BOT STEP: 1")  # debug
            return 4
        # if condition end.

        # TODO:[1]: Fix Priority between "Tricky triangle strategy, step 2." AND "First loop for prevent User's win" :)

        # Done:[1]: Need to implement tricky triangle strategy.

        # Play with that TRICKY_TRIANGLE_COMBINATIONS
        if self.board[4] is self.bot:
            # Tricky triangle strategy, step 2.
            for corner in (0, 2, 6, 8):
                if self.board[corner] is None:
                    print("BOT STEP: 3")  # debug
                    return corner
                # if condition end.
            # for loop end.

            # Tricky triangle strategy, step 3.
            for a, mid, c in TRICKY_TRIANGLE_COMBINATIONS:
                print(f"BOT STEP: a {a}, mid {mid}, c {c}")  # debug
                # гарантуємо, що це правильний трикутник із центром
                if mid != 4:
                    continue
                # if condition end.

                # випадок: бот уже взяв ліву вершину, права вільна
                if self.board[a] is self.bot and self.board[c] is None:
                    print("BOT STEP: 3 (triangle a->c)")  # debug
                    return c
                # if condition end.

                # випадок: бот уже взяв праву вершину, ліва вільна
                if self.board[c] is self.bot and self.board[a] is None:
                    print("BOT STEP: 3 (triangle c->a)")  # debug
                    return a
                # if condition end.
            # for loop end.

            # First loop for prevent User's win
            # Done:[1]: The bot must prevent the user from winning, that is, it must see the user's progress and prevent him.
            for winning_combination in WINNING_COMBINATIONS:
                values = [self.board[index] for index in winning_combination]
                none_count = values.count(None)
                human_symbol_count = values.count(self.human.get())  # for prevent user's win
                #
                if human_symbol_count == 2 and none_count == 1:
                    free_index = values.index(None)
                    print("BOT STEP: 2")  # debug
                    return winning_combination[free_index]
                # if condition end.
            # for loop end.

        # Second loop for smart bot step
        for winning_combination in WINNING_COMBINATIONS:
            values = [self.board[index] for index in winning_combination]
            own_symbol_count = values.count(self.bot)
            none_count = values.count(None)

            if own_symbol_count == 2 and none_count == 1:
                free_index = values.index(None)
                print("BOT STEP: 4.1")  # debug
                return winning_combination[free_index]
            elif own_symbol_count == 1 and none_count == 2:
                free_indices = [winning_combination[i] for i, v in enumerate(values) if v is None]
                print("BOT STEP: 4.2")  # debug
                return random.choice(free_indices)
            elif own_symbol_count == 0 and none_count == 3:
                # Done:[1]: Maybe need to remove 4 from this list because Bot already took that as first condition in this method
                for x in [1, 3, 5, 7]:
                    if x in winning_combination:
                        print("BOT STEP: 4.3")  # debug
                        return x
                    # if condition end.
                # for condition end.
                print("BOT STEP: 4.4")  # debug
                return random.choice(winning_combination)
            # if condition end.
        # for loop end.
        print("BOT STEP: 5")  # debug
        return None
    # Method "find_potentially_winning_step" end.
