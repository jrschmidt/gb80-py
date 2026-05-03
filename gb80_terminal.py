from textual.app import App, ComposeResult
from textual.widgets import Static, Footer
from textual.binding import Binding
from textual.containers import Center, Middle

MAX_LINES = 24
MAX_COLS = 80


class TextDisplay(Static):
    def __init__(self):
        super().__init__("")
        self.lines: list[str] = []

    def update_lines(self, lines: list[str]) -> None:
        if len(lines) > MAX_LINES or any(len(line) > MAX_COLS for line in lines):
            raise ValueError("Lines in lines[] buffer exceeds maximum.")
        self.lines = lines
        rendered = [line.upper() for line in lines]
        if rendered:
            rendered[-1] += "[blink underline] [/]"
        self.update("\n".join(rendered))

    def append_line(self, line: str) -> None:
        lines = self.lines[1:] if len(self.lines) >= MAX_LINES else self.lines
        self.update_lines(lines + [line])

    def append_character(self, char: str) -> None:
        if self.lines and len(self.lines[-1]) >= MAX_COLS:
            raise ValueError("Lines in lines[] buffer exceeds maximum.")
        if self.lines:
            self.update_lines(self.lines[:-1] + [self.lines[-1] + char])
        else:
            self.update_lines([char])


class DevTextDisplay(TextDisplay):
    def update_lines(self, lines: list[str]) -> None:
        if len(lines) > MAX_LINES or any(len(line) > MAX_COLS for line in lines):
            raise ValueError("Lines in lines[] buffer exceeds maximum.")
        self.lines = lines
        rendered = list(lines)
        if rendered:
            rendered[-1] += "[blink underline] [/]"
        self.update("\n".join(rendered))


class Main(App):
    CSS = """
    Screen{
        align: center middle;
    }

    TextDisplay {
        background: black;
        color: green;
        text-style: bold;
        width: 88;  /* So our lines will be 80 characters wide */
        height: 28;  /* So we will show 24 lines of text (24 + 2 padding + 2 border) */
        padding: 1 3;
        border: solid green;
    }

    DevTextDisplay {
        background: black;
        color: white;
        width: 88;
        height: 28;
        padding: 1 3;
        border: solid white;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "QUIT"),
        Binding("ctrl+r", "action_one", "ACTION ONE"),
    ]

    DISPLAY_CLASS: type = TextDisplay

    def compose(self) -> ComposeResult:
        yield self.DISPLAY_CLASS()
        yield Footer()

    def on_init(self) -> None:
        self.query_one(TextDisplay).update_lines([])

    def on_mount(self) -> None:
        self.on_init()

    input_line: str = ""

    def on_new_line(self, line: str) -> None:
        pass

    def on_key(self, event) -> None:
        display = self.query_one(TextDisplay)
        if event.key == "enter":
            self.on_new_line(self.input_line)
            self.input_line = ""
            display.append_line("")
        elif event.key == "backspace":
            if self.input_line:
                display.update_lines(display.lines[:-1] + [display.lines[-1][:-1]])
                self.input_line = self.input_line[:-1]
        elif event.is_printable and len(self.input_line) < MAX_COLS:
            display.append_character(event.character)
            self.input_line += event.character.upper()

    def action_action_one(self) -> None:
        display = self.query_one(TextDisplay)
        display.update_lines(["YOU PRESSED R!", "STATE UPDATED."])
