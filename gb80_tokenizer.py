import re
from gb80_parse_tokens import parse_tokens

tokens = []

def tokenize(line: str) -> list[str]:
    return _tokenize(line)


def _tokenize(line: str) -> list[str]:
    global tokens

    tokens = _parse_program_line(line)
    if tokens[0] == "<fail>":
        tokens = _parse_console_command(line)
    if tokens[0] == "<fail>":
        tokens = [ "<error>" ]
    return tokens


def _parse_program_line(line: str) -> list[str]:
    global tokens

    tokens = []
    match_only = re.match(r'^(\d+)$', line)
    match_with_rest = re.match(r'^(\d+) (.+)$', line)

    if match_only:
        tokens = ["<program_line>", "<line_number>", match_only.group(1)]
    elif match_with_rest:
        tokens = ["<program_line>", "<line_number>", match_with_rest.group(1),
                  "<single_space>", "<remainder_string>", match_with_rest.group(2)]
    else:
        tokens = ["<fail>"]

    tokens.append("<original_line>")
    tokens.append(line)
    return tokens


def _parse_console_command(line: str) -> list[str]:
    return [ "<undefined>" ]