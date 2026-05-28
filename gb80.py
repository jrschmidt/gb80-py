from gb80_terminal import Main, TextDisplay
from gb80_tokenizer import tokenize
from gb80_line_builder import build_line_object
from gb80_line_objects import add_program_line
from gb80_command_runner import execute_console_command, is_waiting_for_input, resume_with_input
from gb80_devtools import DEV_COMMANDS, _dev_state


def handle_init(self) -> None:
    self.on_mode_changed("basic")


def handle_mode_changed(self, mode: str) -> None:
    display = self.query_one(TextDisplay)
    if mode == "basic":
        _dev_state["show_tokens"] = False
        display.update_lines([
            "WELCOME TO GRANDPA BASIC 1980",
            "1980 STYLE BASIC LANGUAGE EMULATOR",
            ""
        ])
    else:
        display.update_lines([
            "--- Grandpa BASIC 1980 ---",
            "Entering DEV mode ...",
            ""
        ])


def handle_new_line(self, line: str) -> None:
    display = self.query_one(TextDisplay)

    if is_waiting_for_input():
        resume_with_input(line)
        return

    if display._dev_mode:
        for cmd_key, cmd_fn in DEV_COMMANDS.items():
            if line == cmd_key or line.startswith(cmd_key + " "):
                arg = line[len(cmd_key):].strip()
                for output_line in cmd_fn(arg):
                    display.output_text(output_line)
                return

    tokens = tokenize(line)

    if display._dev_mode and _dev_state["show_tokens"]:
        for token in tokens:
            display.output_text(token)

    if tokens[0] == "<error>":
        display.output_text("SYNTAX ERROR")
        return

    if tokens[0] == "<parse_complete>":
        if tokens[1] == "<program_line>":
            line_object = build_line_object(tokens)
            add_program_line(int(tokens[3]), line_object)
        elif tokens[1] == "<console_command>":
            execute_console_command(tokens, display.output_text)


Main.on_init = handle_init
Main.on_new_line = handle_new_line
Main.on_mode_changed = handle_mode_changed

if __name__ == "__main__":
    Main().run()
