# /src/tictactoe/ui/app.py

import random
import tkinter as tk
from tkinter import ttk
from .menu import create_menubar
from ..core.bot_strategy import BotStrategyMixin
from ..core.game_logic import GameLogicMixin
from tkinter import PhotoImage
from ..core.constants import (
    CROSS_SYMBOL, NOUGHT_SYMBOL,
    CROSS_IMG_BLACK, NOUGHT_IMG_BLACK,
    CROSS_IMG_GREEN, NOUGHT_IMG_GREEN,
    WINNING_COMBINATIONS
)

# from .core.game_logic import GameLogicMixin
# from .core.bot_strategy import BotStrategyMixin

# Done:[1]: Render 3x3 grid for buttons.
# Done:[1]: Live User choosing X or 0 before first step in a game.
# Done:[1]: Live User first step in a game to empty square.
# Done:[1]: Bot first step in a game to empty square.
# Done:[1]: How to draw X or 0 in the grid cell ?
# Done:[1]: How to catch event on backend side ?
# Done:[1]: Set up successful combination list and allways check if game end or not. And show Green message about Winning.
# Done:[1]: How to make Bot more smart, and add bot symbol 0 or X in the end of any line like XX0 or 00X?
# Done:[1]: No winners mode.
# Done:[1]: Menu About, Help.
# Done:[1]: ? help icon with instruction how to play this game.
# Done:[1]: Game logic separate to sub files.

# TODO:[1]: Unit testing for functions, methods and like selenium for the frontend, if it is possible.
# TODO:[1]: Mac OS runner (without installation).
# Done:[2]: Replace X and 0 with PNG images.
# TODO:[2]: Multilingual support?


# https://docs.python.org/3.12/library/tkinter.html
# Window generator here.
class GameApp(BotStrategyMixin, GameLogicMixin, tk.Tk):
    def __init__(self):
        super().__init__()

        self.cross_img_black = PhotoImage(file=CROSS_IMG_BLACK)
        self.nought_img_black = PhotoImage(file=NOUGHT_IMG_BLACK)
        self.cross_img_green = PhotoImage(file=CROSS_IMG_GREEN)
        self.nought_img_green = PhotoImage(file=NOUGHT_IMG_GREEN)

        # Window settings.
        # Widget title.
        self.title("Tic Tac Toe Game")
        self.geometry("570x680")  # Window size (width x height).
        self.resizable(False, False)  # Disable resizing (for now).

        # --- State ---
        self.size = 3  # Grid size.
        # self.board = [None, None, None, None, None, None, None, None, None]
        # Indexes:   [0,    1,    2,    3,    4,    5,    6,    7,    8]
        self.board = [None] * (self.size * self.size)  # [None|"X"|"O"]
        # default value is "", in our case "X"
        self.human = tk.StringVar(value=CROSS_SYMBOL)  # Choosing a person before the start.
        self.bot = NOUGHT_SYMBOL  # Will update at startup.
        self.current = CROSS_SYMBOL  # Who walks now.
        self.started = False  # Whether they pressed Start.


        # Label Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        # Create text and put it in the window.
        label = ttk.Label(self, text="Tic Tac Toe Game", font=("TkDefaultFont", 16))
        # Geometry manager Pack
        # pady - like css Padding vertical distance.
        label.pack(pady=8)  # at the top

        # --- Choice panel X/O + Start ---
        # Frame Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        choice = ttk.Frame(self, padding=(8, 0))
        # Geometry manager Pack.
        choice.pack()

        # Label Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        ttk.Label(choice, text="Play as:").grid(row=0, column=0, padx=4)
        ttk.Radiobutton(choice, text=CROSS_SYMBOL, variable=self.human, value=CROSS_SYMBOL).grid(row=0, column=1,
                                                                                                 padx=4)
        ttk.Radiobutton(choice, text=NOUGHT_SYMBOL, variable=self.human, value=NOUGHT_SYMBOL).grid(row=0, column=2,
                                                                                                   padx=4)

        # Game start button.
        # Button Widget.
        self.start_btn = ttk.Button(choice, text="Start", command=self.on_start)
        self.start_btn.grid(row=0, column=3, padx=8)

        # Game status bar:
        self.status_var = tk.StringVar(value="Select X or O and press Start")
        # Label Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        ttk.Label(choice, textvariable=self.status_var).grid(row=0, column=4, padx=8)

        # Container for the grid.
        # Frame Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        table = ttk.Frame(self, padding=8)
        # Geometry manager Pack
        table.pack(expand=True, fill="both")

        # Grid doc is here  https://tkdocs.com/tutorial/grid.html#sizing
        # Uniform cells.
        for index in range(self.size):
            # Doc https://www.tcl-lang.org/man/tcl8.6/TkCmd/grid.htm#M24 #grid rowconfigure
            table.grid_rowconfigure(index, weight=1, uniform="grid")
            # Doc https://www.tcl-lang.org/man/tcl8.6/TkCmd/grid.htm#M24 #grid columnconfigure
            table.grid_columnconfigure(index, weight=1, uniform="grid")
        # Loop "for" end.

        # Create 3×3 buttons.
        self.cells = {}
        for row in range(self.size):
            for col in range(self.size):
                # Button Widget doc is here https://tkdocs.com/pyref/ttk_button.html
                #
                btn = ttk.Button(table, text="", width=4, command=lambda r=row, c=col: self.on_cell_click(r, c))

                # Key grid() options for ttk.Button:
                # row: Specifies the row number for the widget (starts from 0).
                # column: Specifies the column number for the widget (starts from 0).
                # rowspan: Specifies how many rows the widget should span.
                # columnspan: Specifies how many columns the widget should span.
                # padx: Adds horizontal padding around the widget.
                # pady: Adds vertical padding around the widget.
                # sticky: Controls how the widget expands within its cell if the cell is larger than the widget.
                #  It takes a string combining compass directions (e.g., "n", "s", "e", "w", "ns", "ew", "nsew").
                btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
                self.cells[(row, col)] = btn
            # Loop "for" end.
        # Loop "for" end.

        # --- Reset ---
        # Frame Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        bottom = ttk.Frame(self, padding=(8, 0))
        # Geometry manager Pack.
        bottom.pack(pady=6)
        # on_reset method triggering.
        ttk.Button(bottom, text="Reset", command=self.on_reset).pack()

        create_menubar(self)

    # Method "__init__" end.

    # --- Helpers ---

    # Game board appearance update.
    def render(self):
        # Update the text/status of the buttons according to the board.
        for row in range(self.size):
            for col in range(self.size):
                index = self.idx(row, col)
                symbol = self.board[index]

                if symbol == CROSS_SYMBOL:
                    img = self.cross_img_black
                elif symbol == NOUGHT_SYMBOL:
                    img = self.nought_img_black
                else:
                    img = ""
                # Condition "if" end.

                self.cells[(row, col)].config(
                    text="",
                    image=img,
                    state=("disabled" if symbol else "normal"),
                )
            # Loop "for" end.
        # Loop "for" end.
    # Method "render" end.

    # --- Events ---
    # Start action, changing game board state.
    def on_start(self):
        # Exit from method if already started.
        if self.started:
            return
        # Condition "if" end.

        # Game started status.
        self.started = True
        print("--------------------------- START ---------------------------")  # debug

        if self.human.get() == CROSS_SYMBOL:
            self.bot = NOUGHT_SYMBOL
        else:
            self.bot = CROSS_SYMBOL

        self.current = CROSS_SYMBOL
        # Game status bar update.
        self.status_var.set(f"You: {self.human.get()}  |  Bot: {self.bot}  |  Turn: {self.current}")

        # If the person has chosen "O", the bot walks first.
        if self.human.get() == NOUGHT_SYMBOL:
            self.bot_move()
        # Condition "if" end.

        # Change game board state.
        self.render()
    # Method "on_start" end.

    def on_cell_click(self, row, col):
        # print(f"CLICKED: row={row}, col={col}")  # debug
        # print(f"BOARD before move: {self.board}")  # debug

        # First you need to start.
        if not self.started:
            return
        # Condition "if" end.

        # Skip if cell is already busy.
        index = self.idx(row, col)
        if self.board[index] is not None:
            return
        # Condition "if" end.

        # Allow a person's move only when it is his turn.
        if self.current != self.human.get():
            return
        # Condition "if" end.

        self.board[index] = self.human.get()
        # print(f"BOARD after move: {self.board}")  #debug

        self.current = self.bot
        # Game status bar update.
        self.status_var.set(f"You: {self.human.get()}  |  Bot: {self.bot}  |  Turn: {self.current}")
        # Change game board state.
        self.render()

        # Done:[1]: Need to cover case if no winners.  winner is None and no empty board cells.
        # Check winning combination.
        winner = self.check_winner()
        empty_cell_count = self.board.count(None)
        if (winner is not None) or (winner is None and empty_cell_count == 0):
            # Stop game if someone winning.
            self.end_game(winner)
            return
        # Condition "if" end.

        # The simplest bot immediately responds.
        self.after(150, self.bot_move)
    # Method "on_cell_click" end.

    # Bot step
    def bot_move(self):
        print("bot_move ------------------------------------------")

        # If the game hasn't started or it's not the bot's turn now, we don't do anything.
        if not self.started or self.current != self.bot:
            return
        # Condition "if" end.

        # Done:[1]: More smart step here, analyze potentially winning steps.
        free_index = self.find_potentially_winning_step()
        # print(f"free_index: {free_index}")
        if free_index is None:
            for index, cell in enumerate(self.board):
                if cell is None:
                    self.board[index] = self.bot
                    break
                # Condition "if" end.
            # Loop "for" end.
        else:
            self.board[free_index] = self.bot
        # Condition "if" end.

        self.current = self.human.get()
        # Game status bar update.
        self.status_var.set(f"You: {self.human.get()}  |  Bot: {self.bot}  |  Turn: {self.current}")
        # Change game board state.
        self.render()

        # Check winning combination For Bot.
        # Done:[1]: Need to cover case if no winners. winner is None and no empty board cells.
        winner = self.check_winner()
        empty_cell_count = self.board.count(None)
        if (winner is not None) or (winner is None and empty_cell_count == 0):
            self.end_game(winner)
            return
        # Condition "if" end.
    # Method "bot_move" end.

    # Game board reset for a new game.
    def on_reset(self):
        self.board = [None] * (self.size * self.size)
        self.started = False
        self.current = CROSS_SYMBOL
        self.bot = NOUGHT_SYMBOL
        self.status_var.set("Select X or O and press Start")

        for btn in self.cells.values():
            btn.config(text="", image="", state="normal")
        # Loop "for" end.

        # Re-enable Start button.
        self.start_btn.config(state="normal")
    # Method "on_reset" end.

    def end_game(self, winner):
        self.started = False
        self.current = CROSS_SYMBOL

        message_substring = ""
        if self.bot == winner:
            message_substring = "Bot WINS"
        elif self.human.get() == winner:
            message_substring = "User WINS"
        elif winner is None:
            message_substring = "TIE"
        # Condition "if" end.

        # Status bar update.
        self.status_var.set(f"!!!  {message_substring}!  !!!")

        # Highlight only the winning line with green PNG.
        if winner in (CROSS_SYMBOL, NOUGHT_SYMBOL):
            winning_line = None

            # Finding a winning combination.
            for winning_combination in WINNING_COMBINATIONS:
                a, b, c = winning_combination
                if (self.board[a] == winner and self.board[b] == winner and self.board[c] == winner):
                    winning_line = winning_combination
                    break
            # Loop "for" end.

            # If you find a winning line, we highlight only it.
            if winning_line is not None:
                for index in winning_line:
                    if winner == CROSS_SYMBOL:
                        img = self.cross_img_green
                    else:
                        img = self.nought_img_green
                    # Condition "if" end.
                    # to find button by row/col.
                    row, col = divmod(index, self.size)
                    self.cells[(row, col)].config(image=img)
                # Loop "for" end.
            # Condition "if" end.
        # Condition "if" end.

        # Disabling all buttons on the board.
        for btn in self.cells.values():
            btn.config(state="disabled")
        # Loop "for" end.

        # Disable Start button.
        self.start_btn.config(state="disabled")
    # Method "end_game" end.

# Class "GameApp" end.
