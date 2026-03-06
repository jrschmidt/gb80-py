from textual.app import App, ComposeResult
from textual.widgets import Static, Footer
from textual.binding import Binding
from textual.containers import Center, Middle
from handler import on_key as handle_key


class TextDisplay(Static):
    def __init__(self):
        super().__init__("")
        self.lines: list[str] = []

    def update_lines(self, lines: list[str]) -> None:
        self.lines = lines
        self.update("\n".join(line.upper() for line in self.lines))

    def append_line(self, line: str) -> None:
        self.lines.append(line)
        self.update("\n".join(line.upper() for line in self.lines))

    def append_character(self, char: str) -> None:
        if self.lines:
            self.lines[-1] = self.lines[-1] + char
        else:
            self.lines.append(char)
        self.update("\n".join(line.upper() for line in self.lines))


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
        height: 26;  /* So we will show 24 lines of text */
        padding: 1 3;
        border: solid green;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "QUIT"),
        Binding("ctrl+r", "action_one", "ACTION ONE"),
    ]

    def compose(self) -> ComposeResult:
        yield TextDisplay()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(TextDisplay).update_lines(["WELCOME", "PRESS R TO DO SOMETHING", "PRESS Q TO QUIT"])

    def on_key(self, event) -> None:
        handle_key(self, event)

    def action_action_one(self) -> None:
        display = self.query_one(TextDisplay)
        display.update_lines(["YOU PRESSED R!", "STATE UPDATED."])


if __name__ == "__main__":
    Main().run()
