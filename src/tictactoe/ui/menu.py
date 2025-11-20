# /src/tictactoe/ui/menu.py

########################################################################################################################
#
# Everything related to menu bar.
#
########################################################################################################################
import tkinter as tk
from tkinter import ttk

# Done:[1]: Separate menu to another py file.
def create_menubar(self):
    menubar = tk.Menu(self, tearoff=0, borderwidth=0, activeborderwidth=0)
    # --- Help menu ---
    help_menu = tk.Menu(
        menubar,
        tearoff=0,
        activeborderwidth=0,
        borderwidth=0,
        font=("Segoe UI", 10),
        activebackground="#e6e6e6",
        background="#f8f8f8",
        relief="flat")
    help_menu.add_command(label="How to Play", command=lambda: on_help(self))
    help_menu.add_separator()
    help_menu.add_command(label="About", command=lambda: on_about(self))
    menubar.add_cascade(label="Help", menu=help_menu)

    # Assign a window menu
    self.config(menu=menubar)

    # Shortcut for Help
    self.bind("<F1>", lambda e: on_help(self))

# Method "_create_menubar" end.

def on_help(self):
    def build(top):
        text = tk.Text(
            top,
            wrap="word",
            font=("Segoe UI", 11),
            bg="#fafafa",
            padx=12,
            pady=10,
            relief="flat"
        )
        text.pack(expand=True, fill="both")

        content = (
            "Rules:\n"
            "• Choose X or O and press Start.\n"
            "• Click an empty cell to place your mark.\n"
            "• Get three in a row (row/column/diagonal) to win.\n"
            "• Reset starts a new game.\n\n"
            "Tips:\n"
            "• Center is strong. Corners are valuable.\n"
            "• Block opponent's two-in-a-row."
        )
        text.insert("1.0", content)

        # Title styling
        text.tag_add("section", "1.0", "1.8")
        text.tag_config("section", font=("Segoe UI", 11, "bold"))

        text.tag_add("tips", "7.0", "7.6")
        text.tag_config("tips", font=("Segoe UI", 11, "bold"))

        text.config(state="disabled")

        ttk.Button(top, text="OK", command=top.destroy).pack(pady=8)

    _open_modal_centered(self, "How to Play", 400, 300, build)

def on_about(self):
    def build(top):
        text = tk.Text(
            top,
            wrap="word",
            font=("Segoe UI", 11),
            bg="#fafafa",
            padx=12,
            pady=10,
            relief="flat"
        )
        text.pack(expand=True, fill="both")
        content = (
            "Tic Tac Toe Game\n"
            "Developer: Volodymyr Oliinyk\n"
            "License: MIT\n"
        )
        text.insert("1.0", content)

        # Title styling
        text.tag_add("title", "1.0", "1.end")
        text.tag_config("title", font=("Segoe UI", 11, "bold"))

        text.tag_add("meta", "2.0", "4.end")
        text.tag_config("meta", font=("Segoe UI", 11))

        text.config(state="disabled")

        ttk.Button(top, text="OK", command=top.destroy).pack(pady=8)

    _open_modal_centered(self, "About", 400, 300, build)

# Method "on_about" end.

def _open_modal_centered(self, title: str, width: int, height: int, build_body_fn):
    top = tk.Toplevel(self)
    top.withdraw()
    top.title(title)

    dialog_width = width
    dialog_height = height
    root_x = self.winfo_x()
    root_y = self.winfo_y()
    root_w = self.winfo_width()
    root_h = self.winfo_height()
    position_x = int(root_x + (root_w / 2) - (dialog_width / 2))
    position_y = int(root_y + (root_h / 2) - (dialog_height / 2))
    top.geometry(f"{dialog_width}x{dialog_height}+{position_x}+{position_y}")

    top.resizable(False, False)
    top.transient(self)
    top.deiconify()
    top.grab_set()

    build_body_fn(top)

    top.protocol("WM_DELETE_WINDOW", top.destroy)

    return top
# Method "_open_modal_centered" end.
