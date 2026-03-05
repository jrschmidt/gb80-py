from textual.events import Key


def on_key(app, event: Key) -> None:
    display = app.query_one("TextDisplay")
    for _ in range(21):
        display.append_line( "1234567[1]1234567[2]1234567[3]1234567[4]1234567[5]1234567[6]1234567[7]1234567[8]" )
