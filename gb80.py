from textual.events import Key
from gb80_terminal import Main, TextDisplay


_state = {"mode": "idle"}


def handle_keypress(app, event: Key) -> None:
    if _state["mode"] == "idle":
        _dummy_1(app, event)
    elif _state["mode"] == "active":
        _dummy_2(app, event)
    else:
        _dummy_3(app, event)


def _dummy_1(app, event: Key) -> None:
    display = app.query_one("TextDisplay")
    display.append_line(f"DUMMY 1: {event.key.upper()}")


def _dummy_2(app, event: Key) -> None:
    display = app.query_one("TextDisplay")
    display.append_line(f"DUMMY 2: {event.key.upper()}")


def _dummy_3(app, event: Key) -> None:
    display = app.query_one("TextDisplay")
    display.append_line(f"DUMMY 3: {event.key.upper()}")


def on_key(app, event: Key) -> None:
    display = app.query_one("TextDisplay")
    display.append_line( f"YOU PRESSED {event.key.upper()}" )


def handle_new_line(self, line: str) -> None:
    display = self.query_one(TextDisplay)
    display.append_line("GB80.PY IS RESPONDING TO THE FOLLOWING INPUT:")
    display.append_line(line)


Main.on_new_line = handle_new_line

if __name__ == "__main__":
    Main().run()
