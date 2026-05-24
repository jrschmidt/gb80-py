# Test handler to test the append_character() method.

# Adds each character typed to the last line.

# Prints a sample line `magic_line` the first time `on_key()`
# is called so there is something to append to.


from textual.events import Key

magic_line = ""

def on_key(app, event: Key) -> None:
  global magic_line

  display = app.query_one("TextDisplay")

  # First, append a line at end of text, so there is something to
  # append characters to, if it is not there already.
  if len(magic_line) == 0:
    magic_line = "This is my magic line: "
    display.output_text(magic_line)

  display.append_character(event.key)
