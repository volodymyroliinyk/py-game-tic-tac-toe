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

# Tricky triangle strategy
#  012 0.? 0?2 ?.2 ?.?
#  345 ?4. .4. .4? .4.
#  678 6.? ?.? ?.8 6?8

# Tricky triangle strategy steps:
# 1) This strategy can be successful if the Bot has already taken a center [4]
# 2) After [4] need to find a free one from the four angle cells [0],[2],[6],[8]
# 3) Find TRIANGLEs which are related to [4][0] OR [4][2] OR [4][6] OR [4][8]
# 4) Take the first free angle cell related to one of the TRIANGLEs
# 5) Last step is already provided by existing logic.

# TODO:[1]:
#  Manual and automated testing strategies:
#  Cases:
#  1) Bot in the center [Issue with preventing user winning]
#  2) User in the center [Issue with preventing user winning]
#  3) Need to test how smart the bot is in its quest to win.
#  4) Need to test how smart the bot is to prevent the user from winning.
#  5) Need to test how smart the bot is to balance between 3 and 4.


class BotStrategyMixin:
    # Must be used just for a Bot.
    def find_potentially_winning_step(self):
        bot_can_win = False
        user_can_win = False
        bot_free_index = None
        user_free_index = None
        bot_free_winning_combinations = self.get_free_winning_combinations(self.bot)
        print(f"bot_free_winning_combinations: {bot_free_winning_combinations}")
        user_free_winning_combinations = self.get_free_winning_combinations(self.human.get())
        bot_free_tricky_triangles_big = self.get_free_tricky_triangles_big(self.bot)
        bot_free_tricky_triangles_small = self.get_free_tricky_triangles_small(self.bot)
        bot_free_tricky_triangles_merged = bot_free_tricky_triangles_big + bot_free_tricky_triangles_small
        print(f"bot_free_tricky_triangles_merged: {bot_free_tricky_triangles_merged}")
        # The best is to take the center of the board first for Bot.
        # OR
        # Tricky triangle strategy, step 1.
        if self.board[4] is None:
            print("BOT STEP: 1")  # debug
            return 4
        # if condition end.

        # TODO:[1]: Fix Priority between "Tricky triangle strategy, step 2." AND "First loop for prevent User's win" :)

        # First loop for prevent User's win
        # Done:[1]: The bot must prevent the user from winning, that is, it must see the user's progress and prevent him.
        for winning_combination in user_free_winning_combinations:
            values = [self.board[index] for index in winning_combination]
            none_count = values.count(None)
            user_symbol_count = values.count(self.human.get())  # for prevent user's win
            #
            if user_symbol_count == 2 and none_count == 1:
                free_index = values.index(None)
                user_can_win = True
                user_free_index = winning_combination[free_index]
                print("BOT STEP: 2")  # debug
                return winning_combination[free_index]
            # if condition end.
        # for loop end.

        # Play with that TRICKY_TRIANGLE_COMBINATIONS_...
        if self.board[4] is self.bot:
            # # Tricky triangle strategy, step 2.
            # for corner in (0, 2, 6, 8):
            #     if self.board[corner] is None:
            #         print("BOT STEP: 3")  # debug
            #         return corner
            #     # if condition end.
            # # for loop end.

            # Tricky triangle strategy, step 3.
            for a, mid, c in bot_free_tricky_triangles_merged:
                # ensure that it is a regular triangle centered on
                if mid != 4:
                    continue
                # if condition end.

                # case: the bot has already taken the right vertex, the left is free
                if self.board[c] is self.bot and self.board[a] is None:
                    print("BOT STEP: 3 (triangle c->a)")  # debug
                    return a
                # if condition end.

                # case: the bot has already taken the left vertex, the right one is free
                if self.board[a] is self.bot and self.board[c] is None:
                    print("BOT STEP: 3 (triangle a->c)")  # debug
                    return c
                # if condition end.


            # for loop end.

        # Весь цей цикл про аналіз кожної ліннії по черзі та прийнятя рішення на льоту,
        #  а потрібно проаналізувати кілька ліній і прийняти рішення на основі ліній Юзера і Бота,
        #  щоб пріоритет перемогти запрацював.
        # ENG:
        # This whole cycle is about analyzing each line in turn and making decisions on the fly,
        # and you need to analyze several lines and make a decision based on the lines of the User and Bot,
        # for the priority to win to work.

        # Стратегія пріоритету:
        # 1) Проходимось по всіх переможних комбінаціях.
        # 2) Збираємо дані для перемоги бота
        # 3) Збираємо дані для перемоги юзера
        # 4) після проходженя всіх комбінацій лише наступним кроком робимо вибір перемогти чи перешколити,
        #    на основі зібраних даних.
        # 5) Робити лише один ретурн з цього методу
        # ENG:
        # Priority Strategy:
        # 1) Let's go through all the winning combinations.
        # 2) Collecting data for the bot to win
        # 3) Collect data for the user's victory
        # 4) after passing all the combinations, only the next step is to make a choice to win or re-train,
        #    based on the data collected.
        # 5) Make only one return from this method

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
                return winning_combination[free_index]
            elif bot_symbol_count == 1 and none_count == 2:
                free_indices = [winning_combination[i] for i, v in enumerate(values) if v is None]
                print("BOT STEP: 4.2")  # debug
                bot_free_index = random.choice(free_indices)
                return random.choice(free_indices)
            # This part is too much.
            # elif bot_symbol_count == 0 and none_count == 3:
            #     # Done:[1]: Maybe need to remove 4 from this list because Bot already took that as first condition in this method
            #     for x in [1, 3, 5, 7]:
            #         if x in winning_combination:
            #             print("BOT STEP: 4.3")  # debug
            #             return x
            #         # if condition end.
            #     # for condition end.
            #     print("BOT STEP: 4.4")  # debug
            #     return random.choice(winning_combination)
            # if condition end.
        # for loop end.
        print("BOT STEP: 5")  # debug
        return None
    # Method "find_potentially_winning_step" end.
