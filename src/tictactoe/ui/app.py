# /src/tictactoe/ui/app.py
import random
import tkinter as tk
from tkinter import ttk


# Done:[1]: Render 3x3 grid for buttons.
# Done:[1]: Live User choosing X or 0 before first step in a game.
# Done:[1]: Live User first step in a game to empty square.
# Done:[1]: Bot first step in a game to empty square.
# Done:[1]: How to draw X or 0 in the grid cell ?
# Done:[1]: How to catch event on backend side ?
# TODO:[1]: Set up successful combination list and allways check if game end or not. And show Green message about Winning.
# TODO:[1]: How to make Bot more smart, and add bot symbol 0 or X in the end of any line like XX0 or 00X?
# TODO:[2]: Replace X and 0 with SVG images.
# TODO:[1]: Unit testing for functions and like selenium for the frontend, if it is possible.
# TODO:[1]: ? help icon with instruction how to play this game
# TODO:[1]: Mac OS runner (without installation).
# TODO:[1]: Windows OS runner (without installation).
# TODO:[1]: Ubuntu OS runner (without installation).

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
#
#  Done:[1]: Need build Method which can check if current combination is successful!
#
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


# https://docs.python.org/3.12/library/tkinter.html
# Window generator here.
class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window settings
        # Widget title
        self.title("Tic Tac Toe Game")
        self.geometry("570x680")  # window size (width x height)
        self.resizable(False, False)  # disable resizing (for now)

        # --- State ---
        self.size = 3  # grid size
        # self.board = [None, None, None, None, None, None, None, None, None]
        # Indexes:   [0,    1,    2,    3,    4,    5,    6,    7,    8]
        self.board = [None] * (self.size * self.size)  # [None|"X"|"O"]
        # default value is "", in our case "X"
        self.human = tk.StringVar(value="X")  # Choosing a person before the start
        self.bot = "O"  # will update at startup
        self.current = "X"  # who walks now
        self.started = False  # whether they pressed Start


        # Label Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        # Create text and put it in the window
        label = ttk.Label(self, text="Tic Tac Toe Game", font=("TkDefaultFont", 16))
        # Geometry manager Pack
        # pady - like css Padding vertical distance.
        label.pack(pady=8)  # at the top

        # --- Choice panel X/O + Start ---
        # Frame Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        choice = ttk.Frame(self, padding=(8, 0))
        # Geometry manager Pack
        choice.pack()

        # Label Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        ttk.Label(choice, text="Play as:").grid(row=0, column=0, padx=4)
        ttk.Radiobutton(choice, text="X", variable=self.human, value="X").grid(row=0, column=1, padx=4)
        ttk.Radiobutton(choice, text="O", variable=self.human, value="O").grid(row=0, column=2, padx=4)

        # Game start button
        # Button Widget
        self.start_btn = ttk.Button(choice, text="Start", command=self.on_start)
        self.start_btn.grid(row=0, column=3, padx=8)

        # Game status bar:
        self.status_var = tk.StringVar(value="Select X or O and press Start")
        # Label Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        ttk.Label(choice, textvariable=self.status_var).grid(row=0, column=4, padx=8)

        # Container for the grid
        # Frame Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        table = ttk.Frame(self, padding=8)
        # Geometry manager Pack
        table.pack(expand=True, fill="both")

        # Grid doc is here  https://tkdocs.com/tutorial/grid.html#sizing
        # Uniform cells
        for index in range(self.size):
            # Doc https://www.tcl-lang.org/man/tcl8.6/TkCmd/grid.htm#M24 #grid rowconfigure
            table.grid_rowconfigure(index, weight=1, uniform="grid")
            # Doc https://www.tcl-lang.org/man/tcl8.6/TkCmd/grid.htm#M24 #grid columnconfigure
            table.grid_columnconfigure(index, weight=1, uniform="grid")
        # for loop end.

        # Create 3×3 buttons
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
            # for loop end.
        # for loop end.

        # --- Reset ---
        # Frame Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        bottom = ttk.Frame(self, padding=(8, 0))
        # Geometry manager Pack
        bottom.pack(pady=6)
        # on_reset method triggering.
        ttk.Button(bottom, text="Reset", command=self.on_reset).pack()

    # Method "__init__" end.

    # --- Helpers ---
    # Convert to one-dimensional list? return index 0-8
    def idx(self, row, col):
        return row * self.size + col

    # Method "idx" end.

    # Game board appearance update
    def render(self):
        # Update the text/status of the buttons according to the board
        for row in range(self.size):
            for col in range(self.size):
                index = self.idx(row, col)
                txt = self.board[index] or ""
                self.cells[(row, col)].config(text=txt, state=("disabled" if txt else "normal"))
            # for loop end.
        # for loop end.

    # Method "render" end.

    # --- Events ---
    # Start action, changing game board state
    def on_start(self):
        # Exit from method if already started
        if self.started:
            return
        # if condition end.

        # Game started status
        self.started = True

        if self.human.get() == "X":
            self.bot = "O"
        else:
            self.bot = "X"

        self.current = "X"
        # Game status bar update.
        self.status_var.set(f"You: {self.human.get()}  |  Bot: {self.bot}  |  Turn: {self.current}")

        # If the person has chosen "O", the bot walks first
        if self.human.get() == "O":
            self.bot_move()
        # if condition end.

        # Change game board state
        self.render()

    # Method "on_start" end.

    def on_cell_click(self, row, col):
        print(f"CLICKED: row={row}, col={col}")  # debug
        print(f"BOARD before move: {self.board}")  # debug

        # First you need to start
        if not self.started:
            return
        # if condition end.

        # Skip if cell is already busy
        index = self.idx(row, col)
        if self.board[index] is not None:
            return
        # if condition end.

        # Allow a person's move only when it is his turn
        if self.current != self.human.get():
            return
        # if condition end.

        self.board[index] = self.human.get()
        print(f"BOARD after move: {self.board}")  #debug

        self.current = self.bot
        # Game status bar update.
        self.status_var.set(f"You: {self.human.get()}  |  Bot: {self.bot}  |  Turn: {self.current}")
        # Change game board state
        self.render()

        # Check winning combination
        winner = self.check_winner()
        if winner:
            print(f"winner: {winner}")  # debug
            # Stop game if someone winning
            self.end_game(winner)
            return
        # if condition end.

        # the simplest bot immediately responds
        self.after(150, self.bot_move)

    # Method "on_cell_click" end.

    # Bot step
    def bot_move(self):
        # If the game hasn't started or it's not the bot's turn now, we don't do anything
        if not self.started or self.current != self.bot:
            return
        # if condition end.

        # TODO:[1]: More smart step here, analyze potentially winning steps
        # # Find the first free cell.
        # for index, cell in enumerate(self.board):
        #     if cell is None:
        #         self.board[index] = self.bot
        #
        #         break
        #     # if condition end.
        # # for loop end.

        free_index = self.find_potentially_winning_step()
        self.board[free_index] = self.bot

        self.current = self.human.get()
        # Game status bar update.
        self.status_var.set(f"You: {self.human.get()}  |  Bot: {self.bot}  |  Turn: {self.current}")
        # Change game board state
        self.render()

        # Check winning combination For Bot.
        winner = self.check_winner()
        if winner:
            print(f"winner: {winner}")  # debug
            self.end_game(winner)
            return
        # if condition end.

    # Method "bot_move" end.

    # Game board reset for a new game
    def on_reset(self):
        self.board = [None] * (self.size * self.size)
        self.started = False
        self.current = "X"
        self.status_var.set("Select X or O and press Start")

        for btn in self.cells.values():
            btn.config(text="", state="normal")
        # for loop end.

    # Method "on_reset" end.

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

    # Must be used just for Bot.
    # Done:[1]: provide thia method inside bot_move method
    # Done:[1]: maybe remobe a second argument because it possible to get from self.
    # TODO:[1]: The bot must prevent the user from winning, that is, it must see the user's progress and prevent him.
    def find_potentially_winning_step(self):
        # The best is to take the center of the board first for Bot
        if self.board[4] is None:
            return 4

        for winning_combination in WINNING_COMBINATIONS:
            values = [self.board[index] for index in winning_combination]
            symbol_count = values.count(self.bot)
            none_count = values.count(None)

            if symbol_count == 2 and none_count == 1:
                free_index = values.index(None)
                return winning_combination[free_index]
            elif symbol_count == 1 and none_count == 2:
                free_indices = [winning_combination[i] for i, v in enumerate(values) if v is None]
                return random.choice(free_indices)
            elif symbol_count == 0 and none_count == 3:
                # Done:[1]: Maybe need to remove 4 from this list because Bot already took that as first condition in this method
                for x in [1, 3, 5, 7]:
                    if x in winning_combination:
                        return x
                    # if condition end.
                # for condition end.
                return random.choice(winning_combination)
            # if condition end.
        # for loop end.
        # if condition end.
        return None

    # Method "find_potentially_winning_step" end.

    def end_game(self, winner):
        self.started = False

        if self.bot == winner:
            messageSubstring = "Bot"
        else:
            messageSubstring = "User"
        # if condition end.

        # Status bar update
        self.status_var.set(f"!!!  {messageSubstring} WINS!  !!!")

        # Disabling all buttons on the board
        for btn in self.cells.values():
            btn.config(state="disabled")
    # Method "end_game" end.
# Class "GameApp" end.
