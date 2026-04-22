import re
from gb80_parse_tokens import parse_tokens


def tokenize(line: str) -> list[str]:
    return _tokenize(line)


# Lines that are input on the terminal are parsed into tokens. A valid line entered
# in an interactive BASIC terminal will generally be either a program line or a
# console command. A program line will start with a line number. A console command
# will usually be one simple word like LIST or RUN.
# 
# "<no_match>" vs "<error>":
# If an entered line does not match whatever a particular method is looking for, it
# will return with a "<no_match>" token, which will signal that we will look for the next
# match. If there is a fatal mistake in the input line, it will return with an "<error>"
# token, and attempts to parse it further will stop.
# If an input line does not successfully match any valid construct, and returns with
# "<no_match>" for all attempted matches, then it will return with an "<error>" token. An
# "<error>" token should result in the terminal displaying a "SYNTAX ERROR" message.
def _tokenize(line: str) -> list[str]:

    tokens = _parse_console_command(line)
    if tokens[0] == "<no_match>":
        tokens = _parse_program_line(line)
    if tokens[0] != "<parse_complete>":
        tokens = [ "<error>" ]
    return tokens


# A program line will begin with a line number, an integer between 1 and the maximum
# line number allowed by your BASIC implementation. When a program line is entered,
# if there is already a program line with the same line number, the new entry will
# replace the old program line. To erase a line instead of replacing it, enter a line
# consisting of the line number with nothing following.
def _parse_program_line(line: str) -> list[str]:

    # A list of subsidiary parse methods that we will cycle through looking for a match.
    _parsers = [
        _parse_remark
    ]

    # First, check to see that the input line matches the general format that any
    # valid program line will have.
    match_only = re.match(r'^(\d+)$', line)
    match_with_rest = re.match(r'^(\d+) (.+)$', line)

    # If an input line is an integer string with nothing following, that means the user
    # wishes to remove any program line with this number. So, this is actually a console
    # command, with the line number as a parameter.
    if match_only:
        tokens = [
            "<parse_complete>",
            "<console_command>",
            "<delete_program_line>",
            "<line_number>",
            match_only.group(1)
            ]

    # This condition will match anything that starts with a line number, followed with
    # something else.
    elif match_with_rest:
        tokens = [
            "<no_match>",
            "<program_line>",
            "<line_number>",
            match_with_rest.group(1),
            "<single_space>",
            "<remainder_string>",
            match_with_rest.group(2)
        ]

    else:
        tokens = ["<error>"]

    # Now, cycle through the individual parsers for different types of BASIC program lines.
    for parser in _parsers:
        if (tokens[0] == "<error>") or (tokens[0] == "<parse_complete>") :
            break
        if tokens[5] != "<remainder_string>":
            tokens = [ "<error>" ]
            break
        remainder_string = tokens[6]
        tokens = parser(tokens, remainder_string)

    if tokens[0] != "<parse_complete>" :
        tokens = [ "<error>" ]

    tokens.append("<original_line>")
    tokens.append(line)
    return tokens


def _parse_remark(tokens: list[str], remainder_string: str) -> list[str]:
    if remainder_string.startswith("REM "):
        del tokens[-2:]
        tokens[0] = "<parse_complete>"
        tokens.append("<remark>")
    return tokens


# If an entered line does not have a line number, this method will check if it is a
# valid console command line. A line that matches a valid command will be parsed with
# the appropriate tokens. Currently, we are not implementing parameters any of these
# commands, so any valid command will consist of just a single keyword.
def _parse_console_command(line: str) -> list[str]:

    tokens = []
    if line == "CLEAR" :
        tokens = ["<parse_complete>", "<console_command>", "<clear>"]
    elif line == "LIST" :
        tokens = ["<parse_complete>", "<console_command>", "<list>"]
    elif line == "RUN" :
        tokens = ["<parse_complete>", "<console_command>", "<run>"]
    else:
        tokens = ["<no_match>"]

    return tokens
