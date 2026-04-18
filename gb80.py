from gb80_terminal import Main, TextDisplay
from gb80_tokenizer import tokenize
from gb80_parse_tokens import parse_tokens


_state = {"mode": "dev"}


def handle_init(self) -> None:
    display = self.query_one(TextDisplay)
    display.update_lines(["WELCOME TO GB80", ""])


def handle_new_line(self, line: str) -> None:
    display = self.query_one(TextDisplay)
    tokens = tokenize(line)

    if _state["mode"] == "dev":
        for token in tokens:
            display.append_line(token)


Main.on_init = handle_init
Main.on_new_line = handle_new_line

if __name__ == "__main__":
    Main().run()
