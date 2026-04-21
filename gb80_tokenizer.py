import re
from gb80_parse_tokens import parse_tokens


def tokenize(line: str) -> list[str]:
    return _tokenize(line)


# Lines that are input on the terminal are parsed into tokens. A valid line entered
# in an interactive BASIC terminal will generally be either a program line or a
# console command. A program line will start with a line number. A console command
# will usually be one simple word like LIST or RUN.
# 
# "<fail>" vs "<error>":
# If an entered line does not match whatever a particular method is looking for, it
# will return with a "<fail>" token, which will signal that we will look for the next
# match. If there is a fatal mistake in the input line, it will return with an "<error>"
# token, and attempts to parse it further will stop.
# If an input line does not successfully match any valid construct, and returns with
# "<fail>" for all attempted matches, then it will return with an "<error>" token. An
# "<error>" token should result in the terminal displaying a "SYNTAX ERROR" message.
def _tokenize(line: str) -> list[str]:

    tokens = _parse_program_line(line)
    if tokens[0] == "<fail>":
        tokens = _parse_console_command(line)
    if tokens[0] == "<fail>":
        tokens = [ "<error>" ]
    return tokens


# A program line will begin with a line number, an integer between 1 and the maximum
# line number allowed by your BASIC implementation. When a program line is entered,
# if there is already a program line with the same line number, the new entry will
# replace the old program line. To erase a line instead of replacing it, enter a line
# consisting of the line number with nothing following.
def _parse_program_line(line: str) -> list[str]:


    # First, check to see that the input line matches the general format that any
    # valid program line will have.
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

    # Now, traverse the individual types of program lines
    for parser in parsers:
        if (tokens[0] == "<fail>") or (tokens[0] == "<error>"):
            break
        tokens = parser(tokens)

    tokens.append("<original_line>")
    tokens.append(line)
    return tokens


def _parse_remark(tokens: list[str]) -> list[str]:
    return tokens



# If an entered line does not have a line number, this method will check if it is a
# valid console command line. A line that matches a valid command will be parsed with
# the appropriate tokens. Currently, we are not implementing parameters for any commands,
# so any valid command will consist of just a single keyword.
def _parse_console_command(line: str) -> list[str]:

    tokens = []
    if line == "CLEAR" :
        tokens = ["<console_command>", "<clear>"]
    elif line == "LIST" :
        tokens = ["<console_command>", "<list>"]
    elif line == "RUN" :
        tokens = ["<console_command>", "<run>"]
    else:
        tokens = ["<fail>"]

    tokens.append("<original_line>")
    tokens.append(line)
    return tokens
