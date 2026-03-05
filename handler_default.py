from textual.events import Key


def on_key(app, event: Key) -> None:
    display = app.query_one("TextDisplay")
    display.append_line(event.key.upper())
