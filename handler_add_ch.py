# TEST THE append_character() METHOD

from textual.events import Key

magic_line = ""

def on_key(app, event: Key) -> None:
  global magic_line

  display = app.query_one("TextDisplay")

  # First, append a line at end of text, so there is something to
  # append characters to, if it is not there already.
  if len(magic_line) == 0:
    magic_line = "This is my magic line: "
    display.append_line(magic_line)

  display.append_character(event.key)
