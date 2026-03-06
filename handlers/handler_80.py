# Test handler to check dimensions of the terminal display.

# Display should be 24 lines, 80 characters wide.

# This prints 21 80-character lines, because currently the app
    # prints 3 test lines when it initializes.


from textual.events import Key


def on_key(app, event: Key) -> None:
    display = app.query_one("TextDisplay")
    for _ in range(21):
        display.append_line( "1234567[1]1234567[2]1234567[3]1234567[4]1234567[5]1234567[6]1234567[7]1234567[8]" )
