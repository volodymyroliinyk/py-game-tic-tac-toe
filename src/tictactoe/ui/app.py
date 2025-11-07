# /src/tictactoe/ui/app.py
import tkinter as tk
from tkinter import ttk


# Done:[1]: Render 3x3 grid for buttons.
# TODO:[1]: Live User choosing X or 0 before first step in a game.
# TODO:[1]: Live User first step in a game to empty square.
# TODO:[1]: Bot first step in a game to empty square.
# TODO:[1]: How to draw X or 0 in the grid cell ?
# TODO:[1]: How to catch event on backend side ?

# https://docs.python.org/3.12/library/tkinter.html
# Window generator here.
class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Tic Tac Toe Game")
        self.geometry("600x600")  # window size (width x height)
        self.resizable(False, False)  # disable resizing (for now)

        # Label Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        # Create text and put it in the window
        label = ttk.Label(self, text="Tic Tac Toe Game", font=("TkDefaultFont", 16))
        label.pack(pady=8)  # at the top

        # Frame Widget doc is here https://docs.python.org/3.12/library/tkinter.ttk.html
        # Container for the grid
        table = ttk.Frame(self, padding=8)
        table.pack(expand=True, fill="both")

        # Grid doc is here  https://tkdocs.com/tutorial/grid.html#sizing
        # Uniform cells
        for i in range(3):
            # Doc https://www.tcl-lang.org/man/tcl8.6/TkCmd/grid.htm#M24 #grid rowconfigure
            table.grid_rowconfigure(i, weight=1, uniform="grid")
            # Doc https://www.tcl-lang.org/man/tcl8.6/TkCmd/grid.htm#M24 #grid columnconfigure
            table.grid_columnconfigure(i, weight=1, uniform="grid")

        # Create 3×3 buttons
        cells = {}
        for row in range(3):
            for col in range(3):
                # Button Widget doc is here https://tkdocs.com/pyref/ttk_button.html
                btn = ttk.Button(table, text="", width=4)

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
                cells[(row, col)] = btn
