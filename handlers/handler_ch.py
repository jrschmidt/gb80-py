# Test handler to test the append_character() method.

# Prints whichever character is entered on a new line.


from textual.events import Key


def on_key(app, event: Key) -> None:
    display = app.query_one("TextDisplay")
    display.output_text( f"{event.key}" )
