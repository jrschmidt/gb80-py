from textual.app import App, ComposeResult
from textual.widgets import Static, Footer
from textual.binding import Binding


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


class Main(App):
    CSS = """
    TextDisplay {
        height: 1fr;
        border: solid green;
        padding: 1 2;
        color: green;
        text-style: bold;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "QUIT"),
        Binding("r", "action_one", "ACTION ONE"),
    ]

    def compose(self) -> ComposeResult:
        yield TextDisplay()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(TextDisplay).update_lines(["WELCOME", "PRESS R TO DO SOMETHING", "PRESS Q TO QUIT"])

    def action_action_one(self) -> None:
        display = self.query_one(TextDisplay)
        display.update_lines(["YOU PRESSED R!", "STATE UPDATED."])


if __name__ == "__main__":
    Main().run()
