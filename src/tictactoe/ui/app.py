# /src/tictactoe/ui/app.py
import tkinter as tk
from tkinter import ttk


# Done:[1]: Render 3x3 grid for buttons.
# Done:[1]: Live User choosing X or 0 before first step in a game.
# Done:[1]: Live User first step in a game to empty square.
# Done:[1]: Bot first step in a game to empty square.
# Done:[1]: How to draw X or 0 in the grid cell ?
# Done:[1]: How to catch event on backend side ?
# TODO:[1]: Set up successful combination list and allways check if game ends or not. And showGreen message about Winning.
# TODO:[1]: How to make Bot more smart, and add bot symbol 0 or X in the end of any line like XX0 or 00X?
# TODO:[2]: Replace X and 0 with SVG images.

# https://docs.python.org/3.12/library/tkinter.html
# Window generator here.
class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window settings
        # Widget title
        self.title("Tic Tac Toe Game")
        self.geometry("600x600")  # window size (width x height)
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

        # --- Reset ---
        # Frame Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        bottom = ttk.Frame(self, padding=(8, 0))
        # Geometry manager Pack
        bottom.pack(pady=6)
        # on_reset method triggering.
        ttk.Button(bottom, text="Reset", command=self.on_reset).pack()

    # Method "__init__" ends.

    # --- Helpers ---
    # Convert to one-dimensional list? return index 0-8
    def idx(self, row, col):
        return row * self.size + col

    # Method "idx" ends.

    # Game board appearance update
    def render(self):
        # Update the text/status of the buttons according to the board
        for row in range(self.size):
            for col in range(self.size):
                index = self.idx(row, col)
                txt = self.board[index] or ""
                self.cells[(row, col)].config(text=txt, state=("disabled" if txt else "normal"))

    # Method "render" ends.

    # --- Events ---
    # Start action, changing game board state
    def on_start(self):
        # Exit from method if already started
        if self.started:
            return

        # Game started status
        self.started = True
        self.bot = "O" if self.human.get() == "X" else "X"
        self.current = "X"
        # Game status bar update.
        self.status_var.set(f"You: {self.human.get()}  |  Bot: {self.bot}  |  Turn: {self.current}")

        # If the person has chosen "O", the bot walks first
        if self.human.get() == "O":
            self.bot_move()
        # Change game board state
        self.render()

    # Method "on_start" ends.

    def on_cell_click(self, row, col):
        if not self.started:
            return  # first you need to start

        index = self.idx(row, col)
        if self.board[index] is not None:
            return

        # Allow a person's move only when it is his turn
        if self.current != self.human.get():
            return

        self.board[index] = self.human.get()
        self.current = self.bot
        # Game status bar update.
        self.status_var.set(f"You: {self.human.get()}  |  Bot: {self.bot}  |  Turn: {self.current}")
        # Change game board state
        self.render()

        # TODO:[1]: Check winning combination
        # TODO:[1]: Show winner User OR Bot
        # TODO:[1]: Stop game if someone winning
        # the simplest bot immediately responds
        self.after(150, self.bot_move)

    # Method "on_cell_click" ends.

    # Bot step
    def bot_move(self):
        # If the game hasn't started or it's not the bot's turn now, we don't do anything
        if not self.started or self.current != self.bot:
            return

        # TODO:[1]: More smart step here, analyze potentially winning steps
        # Find the first free cell
        for i, cell in enumerate(self.board):
            if cell is None:
                self.board[i] = self.bot
                break

        self.current = self.human.get()
        # Game status bar update.
        self.status_var.set(f"You: {self.human.get()}  |  Bot: {self.bot}  |  Turn: {self.current}")
        # Change game board state
        self.render()
    # Method "bot_move" ends.

    # Game board reset for a new game
    def on_reset(self):
        self.board = [None] * (self.size * self.size)
        self.started = False
        self.current = "X"
        self.status_var.set("Select X or O and press Start")

        for btn in self.cells.values():
            btn.config(text="", state="normal")
    # Method "on_reset" ends.

    # Winning combinations for X
    # XXX 000 000 X00 0X0 00X X00 00X
    # 000 XXX 000 X00 0X0 00X 0X0 0X0
    # 000 000 XXX X00 0X0 00X 00X X00

    # Winning combinations for 0
    # 000 XXX XXX 0XX X0X XX0 0XX XX0
    # XXX 000 XXX 0XX X0X XX0 X0X X0X
    # XXX XXX 000 0XX X0X XX0 XX0 0XX

    # Indexes
    # 0 1 2
    # 3 4 5
    # 6 7 8

    # Winning combinations for indexes
    # 012, 345, 678, 036, 147, 258, 048, 246
    #
    #  TODO:[1]: Need build Method which can check if current combination is successfull!
    #


# Class "GameApp" ends.
