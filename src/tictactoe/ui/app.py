# /src/tictactoe/ui/app.py
import tkinter as tk
from tkinter import ttk


# Window generator here.
class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe Game")
        self.geometry("600x600")  # розмір вікна (ширина x висота)
        self.resizable(False, False)  # вимкнути ресайз (поки що)

        # Створюємо текст і кладемо у вікно
        label = ttk.Label(self, text="Tic Tac Toe Game", font=("TkDefaultFont", 16))
        label.pack(expand=True)  # по центру
