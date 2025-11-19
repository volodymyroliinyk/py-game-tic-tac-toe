# /src/tictactoe/core/bot_strategy.py

########################################################################################################################
#
#
#
########################################################################################################################

# Smart Bot
# How to find free cell just around first one?
# How to find how to find 3rd cell if two nearest already don ?
# How to fut third X or 0 between two first?

# How to predict the next step, second and third steps?
#  012 0?? ?1? ??2 ..? ?.? .?. ?.? ?.. .?.
#  345 ??. .?. .?? ??5 .?? .?. ??. 3?? ?4?
#  678 ?.? .?. ?.? ..? ??8 ?7? 6?? ?.. .?.

# The easiest way to check if each winning combination have combination like:
# None, X, None
# X, None, None
# None, None, X
#
# None, 0, None
# 0, None, None
# None, None, 0

# Need build Method which can check in an array of three elements that it has contains:
# 1) all three elements are None and stop and output it,
# 2) one X|0 and two other elements None, in any sequence stop at the first combination and output it,
# 3) two X|0 and one None element, in any sequence stop on it and output it.


import random
from ..core.constants import CORNERS
from ..core.constants import TRICKY_TRIANGLE_COMBINATIONS_BIG
from ..core.constants import TRIANGLE_TO_LINES_BIG
from ..core.constants import TRICKY_TRIANGLE_COMBINATIONS_SMALL
from ..core.constants import TRIANGLE_TO_LINES_SMALL
from ..core.constants import TRICKY_TRIANGLE_COMBINATIONS_CORNER
from ..core.constants import TRIANGLE_TO_LINES_CORNER



class BotStrategyMixin:
    # Must be used just for a Bot.
    def find_potentially_winning_step(self):
        bot_can_win = False
        user_can_win = False
        bot_free_index = None
        user_free_index = None

        # The best is to take the center of the board first for Bot.
        # OR
        # Tricky triangle strategy, step 1.
        if self.board[4] is None:
            print("BOT STEP: 1")  # debug
            return 4
        # Condition "if" end.

        bot_free_winning_combinations = self.get_free_winning_combinations(self.bot)
        # print(f"bot_free_winning_combinations: {bot_free_winning_combinations}")
        user_free_winning_combinations = self.get_free_winning_combinations(self.human.get())
        bot_free_tricky_triangles_big = self.get_free_tricky_triangles_common(self.bot,
                                                                              TRICKY_TRIANGLE_COMBINATIONS_BIG,
                                                                              TRIANGLE_TO_LINES_BIG)
        bot_free_tricky_triangles_small = self.get_free_tricky_triangles_common(self.bot,
                                                                                TRICKY_TRIANGLE_COMBINATIONS_SMALL,
                                                                                TRIANGLE_TO_LINES_SMALL)
        bot_free_tricky_triangles_corner = self.get_free_tricky_triangles_common(self.bot,
                                                                                 TRICKY_TRIANGLE_COMBINATIONS_CORNER,
                                                                                 TRIANGLE_TO_LINES_CORNER)
        # print(f"bot_free_tricky_triangles_corner: {bot_free_tricky_triangles_corner}")
        bot_free_tricky_triangles_merged = bot_free_tricky_triangles_big + bot_free_tricky_triangles_small
        # print(f"bot_free_tricky_triangles_merged: {bot_free_tricky_triangles_merged}")

        # First loop for prevent User's win.
        for winning_combination in user_free_winning_combinations:
            values = [self.board[index] for index in winning_combination]
            none_count = values.count(None)
            user_symbol_count = values.count(self.human.get())  # For prevent user's win.

            if user_symbol_count == 2 and none_count == 1:
                free_index = values.index(None)
                user_can_win = True
                user_free_index = winning_combination[free_index]
                print("BOT STEP: 2")  # debug
                break
            # Condition "if" end.
        # Loop "for" end.

        # Play with that TRICKY_TRIANGLE_COMBINATIONS_...
        if self.board[4] is self.bot:
            # Tricky triangle strategy, step 3.
            for a, mid, c in bot_free_tricky_triangles_merged:
                # Ensure that it is a regular triangle centered on.
                if mid != 4:
                    continue
                # Condition "if" end.

                # The bot has already taken the right vertex, the left is free.
                if self.board[c] is self.bot and self.board[a] is None:
                    print("BOT TRIANGLE: 3 (triangle c->a)")  # debug
                    bot_free_index = a
                    break
                # Condition "if" end.

                # The bot has already taken the left vertex, the right one is free.
                if self.board[a] is self.bot and self.board[c] is None:
                    print("BOT TRIANGLE: 3 (triangle a->c)")  # debug
                    bot_free_index = c
                    break
                # Condition "if" end.
            # Loop "for" end.
        elif self.board[4] is not self.bot:
            for a, mid, c in bot_free_tricky_triangles_corner:
                tri_indices = (a, mid, c)
                tri_cells = [self.board[a], self.board[mid], self.board[c]]
                bot_count = tri_cells.count(self.bot)
                none_positions = [i for i, v in enumerate(tri_cells) if v is None]

                # print(f"BOT CORNER TRIANGLE a:{a}-{self.board[a]}, mid:{mid}-{self.board[mid]}, c:{c}-{self.board[c]}")  # debug

                if bot_count == 0 and len(none_positions) == 3:
                    # Give priority to the global angles that are part of this triangle.
                    for corner in CORNERS:
                        if corner in (a, c) and self.board[corner] is None:
                            bot_free_index = corner
                            print(f"BOT CORNER TRIANGLE: take empty-corner start {bot_free_index}")
                            break
                        # Condition "if" end.
                    # Loop "for" end.

                    # If we were able to choose an angle - we get out of the loop by triangles.
                    if bot_free_index is not None:
                        break
                    # Condition "if" end.

                    # If for some reason there are no angles (theoretically unlikely) - we take a.
                    bot_free_index = a
                    print(f"BOT CORNER TRIANGLE: take any from empty triangle {bot_free_index}")
                    break
                # The bot already occupies 2 cells in a triangle - we take the third.
                elif bot_count == 2 and len(none_positions) == 1:
                    idx = none_positions[0]
                    bot_free_index = tri_indices[idx]
                    print(f"BOT CORNER TRIANGLE: finish triangle at {bot_free_index}")  # debug
                    break
                # Bot takes 1 cell, 2 empty.
                elif bot_count == 1 and len(none_positions) == 2:
                    # If the mid is free, it is best to take it.
                    if self.board[mid] is None:
                        bot_free_index = mid
                        print(f"BOT CORNER TRIANGLE: take mid {mid}")  # debug
                        break
                    # If mid is not free (theoretically it shouldn't be, but just in case).
                    else:
                        # Take any free angle (a or c).
                        for pos in none_positions:
                            candidate = tri_indices[pos]
                            if candidate in (a, c) and self.board[candidate] is None:
                                bot_free_index = candidate
                                print(f"BOT CORNER TRIANGLE: take corner {bot_free_index}")  # debug
                                break
                            # Condition "if" end.
                        # Loop "for" end.

                        # If we find an angle, we proceed from the cycle of triangles.
                        if bot_free_index is not None:
                            break
                        # Condition "if" end.
                    # Condition "if" end.
                # Condition "if" end.
            # Loop "for" end.
            # print(f"BOT CORNER TRIANGLE: bot_free_index {bot_free_index}")  # debug

        # Loop for smart bot step.
        for winning_combination in bot_free_winning_combinations:
            values = [self.board[index] for index in winning_combination]
            bot_symbol_count = values.count(self.bot)
            none_count = values.count(None)

            if bot_symbol_count == 2 and none_count == 1:
                free_index = values.index(None)
                bot_can_win = True
                bot_free_index = winning_combination[free_index]
                print("BOT STEP: 4.1")  # debug
                break
                # return winning_combination[free_index]
            elif bot_symbol_count == 1 and none_count == 2:
                free_indices = [winning_combination[i] for i, v in enumerate(values) if v is None]
                print("BOT STEP: 4.2")  # debug
                bot_free_index = random.choice(free_indices)
                break
            # Condition "if" end.
        # Loop "for" end.

        if bot_can_win == True and user_can_win == True:
            print(f"FINAL CASE 1: bot_free_index: {bot_free_index}")
            return bot_free_index
        elif bot_can_win == True and user_can_win == False:
            print(f"FINAL CASE 2: bot_free_index: {bot_free_index}")
            return bot_free_index
        elif bot_can_win == False and user_can_win == True:
            print(f"FINAL CASE 3: user_free_index: {user_free_index}")
            return user_free_index
        elif bot_can_win == False and user_can_win == False:
            print(f"FINAL CASE 4: bot_free_index: {bot_free_index}")
            return bot_free_index
        # Condition "if" end.

        return None
    # Method "find_potentially_winning_step" end.
