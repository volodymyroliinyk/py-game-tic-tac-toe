from tictactoe.ui.app import GameApp
from tictactoe.core.constants import CROSS_SYMBOL, NOUGHT_SYMBOL


# It's just a stub for TTC. Button:
#  - supports config(...)
#  - supports cget(...)
#  - supports instate([...])
class DummyButton:
    def __init__(self):
        self._options = {
            "text": "",
            "image": "",
            "state": "normal",
        }

    def config(self, **kwargs):
        self._options.update(kwargs)

    def cget(self, name):
        return self._options.get(name, "")

    def instate(self, states):
        # states: e.g. ["disabled"] or ["!disabled"].
        flag = states[0]
        current_state = self._options.get("state", "normal")
        if flag.startswith("!"):
            # "!disabled" -> true if state != "disabled"
            wanted = flag[1:]
            return current_state != wanted
        else:
            # "disabled" -> true if state == "disabled"
            return current_state == flag


def create_app():
    app = GameApp()
    app.withdraw()

    # Replace all real buttons with DummyButton,
    # so that render() does not call the real Tk and PhotoImage.
    new_cells = {}
    for key in app.cells.keys():
        new_cells[key] = DummyButton()
    app.cells = new_cells

    return app


# Returns (text, has_image, state_str),
# where has_image = True if image is set (not an empty string),
# and state_str is "disabled" or "normal" (via instate()).
def extract_btn_state(btn):
    text = btn.cget("text")
    img_name = btn.cget("image")
    has_image = bool(img_name)
    state_str = "disabled" if btn.instate(["disabled"]) else "normal"
    return text, has_image, state_str


def test_render_empty_board():
    app = create_app()

    app.board = [None] * 9
    app.render()

    for btn in app.cells.values():
        text, has_image, state = extract_btn_state(btn)
        assert text == ""
        assert has_image is False
        assert state == "normal"


def test_render_all_crosses():
    app = create_app()

    app.board = [CROSS_SYMBOL] * 9
    app.render()

    for btn in app.cells.values():
        text, has_image, state = extract_btn_state(btn)
        assert text == ""
        # For X there is an "image"
        assert has_image is True
        assert state == "disabled"


def test_render_all_noughts():
    app = create_app()

    app.board = [NOUGHT_SYMBOL] * 9
    app.render()

    for btn in app.cells.values():
        text, has_image, state = extract_btn_state(btn)
        assert text == ""
        # For O there is an "image"
        assert has_image is True
        assert state == "disabled"


def test_render_mixed_board():
    app = create_app()

    # X . O
    # . X .
    # O . X
    app.board = [
        CROSS_SYMBOL, None, NOUGHT_SYMBOL,
        None, CROSS_SYMBOL, None,
        NOUGHT_SYMBOL, None, CROSS_SYMBOL,
    ]

    app.render()

    # Expectations by indices:
    # index -> (has_image, state_str)
    expected = {
        0: (True, "disabled"),  # X
        1: (False, "normal"),  # None
        2: (True, "disabled"),  # O
        3: (False, "normal"),  # None
        4: (True, "disabled"),  # X
        5: (False, "normal"),  # None
        6: (True, "disabled"),  # O
        7: (False, "normal"),  # None
        8: (True, "disabled"),  # X
    }

    size = app.size
    for row in range(size):
        for col in range(size):
            idx = row * size + col
            btn = app.cells[(row, col)]
            text, has_image, state = extract_btn_state(btn)

            exp_has_image, exp_state = expected[idx]

            assert text == ""
            assert has_image is exp_has_image
            assert state == exp_state
