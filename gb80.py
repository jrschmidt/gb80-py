from textual.events import Key
from constants import MAX_LINES, MAX_COLS
from gb80_terminal import Main


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


if __name__ == "__main__":
    Main().run()
