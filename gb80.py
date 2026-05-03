from gb80_terminal import Main, TextDisplay, DevTextDisplay
from gb80_tokenizer import tokenize
from gb80_line_builder import build_line_object
from gb80_line_objects import add_program_line, delete_program_line


_state = {"mode": "dev"}

if _state.get("mode") == "dev":
    Main.DISPLAY_CLASS = DevTextDisplay


def handle_init(self) -> None:
    display = self.query_one(TextDisplay)
    display.update_lines(["WELCOME TO GB80", ""])


def handle_new_line(self, line: str) -> None:
    display = self.query_one(TextDisplay)
    tokens = tokenize(line)
    line_object = build_line_object(tokens)

    if tokens[0] == "<parse_complete>":
        if tokens[1] == "<program_line>":
            add_program_line(int(tokens[3]), line_object)
        elif tokens[1] == "<console_command>" and tokens[2] == "<delete_program_line>":
            delete_program_line(int(tokens[4]))

    if _state["mode"] == "dev":
        for token in tokens:
            display.append_line(token)


Main.on_init = handle_init
Main.on_new_line = handle_new_line

if __name__ == "__main__":
    Main().run()
