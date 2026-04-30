import re
from gb80_parse_tokens import parse_tokens
from gb80_constants import MAX_LINE_NUMBER


def tokenize(line: str) -> list[str]:
    return _tokenize(line)


# Lines that are input on the terminal are parsed into tokens. A valid line entered
# in an interactive BASIC terminal will generally be either a program line or a
# console command. A program line will start with a line number. A console command
# will usually be one simple word like LIST or RUN.
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
# 
# Note that these functions only parse the input into a list of "tokens". Forming
# actual program line objects, or other actions, are performed afterwards in another
# part of the codebase.


# --------   Program Line "Primary" Parser   --------
# Parses a program line into tokens, with the help of "primary", "subsidiary" and
# "utility" parsers.

def _parse_program_line(line: str) -> list[str]:

    # A list of subsidiary parse methods that we will cycle through looking for a match.
    _parsers = [
        _parse_remark,
        _parse_numeric_assignment,
        _parse_string_assignment,
        _parse_goto,
        _parse_if_then,
        _parse_gosub,
        _parse_return,
        _parse_print,
        _parse_input,
        _parse_end
    ]


    # Check for a valid line number followed by nothing else.
    # If an input line is an integer string with nothing following, that means the user
    # wishes to remove any program line with this number. So, this is actually a console
    # command, with the line number as a parameter.
    match_only = re.match(r'^(\d+)$', line)

    if match_only:
        number_test = _parse_line_number(match_only.group(1))
        if number_test == "<error>":
            tokens = ["<error>"]

        else:
            tokens = [
                "<parse_complete>",
                "<console_command>",
                "<delete_program_line>",
                "<line_number_ref>",
                match_only.group(1)
                ]

    # Check for a valid line number followed by nothing else.
    # This condition will match anything that starts with a line number, followed with
    # something else.
    if not match_only:
        match_with_rest = re.match(r'^(\d+) (.+)$', line)
        if match_with_rest:
            number_test = _parse_line_number(match_with_rest.group(1))
            if number_test == "<error>":
                tokens = ["<error>"]

            else:
                tokens = [
                    "<no_match>",
                    "<program_line>",
                    "<line_number>",
                    match_with_rest.group(1),
                    "<single_space>",
                    "<remainder_string>",
                    match_with_rest.group(2)
                ]

    if not (match_only or match_with_rest):
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

    if (tokens[0] == "<parse_complete>") and (tokens[1] == "<program_line>") :
        tokens.append("<original_line>")
        tokens.append(line)

    if tokens[0] != "<parse_complete>" :
        tokens = [ "<error>" ]

    return tokens


# --------   "Subsidiary" Parsers for Program Lines   --------
# These are the parser methods that _parse_program_line() cycles through, trying to match
# the input line with different types of BASIC program lines. When a match is found, the
# method returns the appropriate tokens. If no match is found for that individual program
# line type, the list of tokens is returned unaltered so it can be passed to the next parsing
# method. Numeric, string, or boolean expressions, as well as sequences of digits for line
# number references, are inserted between the tokens as strings, to be parsed by additional
# "utility" parsing methods.


# Parse a BASIC REM statement. Comments are called "remarks" in BASIC.
# Example:
# 100 REM THIS IS A REMARK
# 110 REM
# 120 REM THIS IS ANOTHER REMARK
# A REM statement can consist of just a line number followed by "REM",
# with nothing after it, in order to insert a blank line as white space.
def _parse_remark(tokens: list[str], remainder_string: str) -> list[str]:
    if (remainder_string.startswith("REM ")) or (remainder_string == "REM") :
        del tokens[-3:]
        tokens[0] = "<parse_complete>"
        tokens.append("<remark>")
    return tokens


# Parse a numeric assignment statement
# Example:
# 220 X=100
# 275 W=A+B+C
# 350 H=(E1+E2)/V7
def _parse_numeric_assignment(tokens: list[str], remainder_string: str) -> list[str]:

    return _parse_assignment(
        tokens,
        remainder_string,
        [1, 2, 3],
        _parse_numeric_variable,
        "<numeric_assignment>",
        "<numeric_expression>"
    )


# Parse a string assignment statement
# Example:
# 640 F$="FAILURE"
# 710 N$=N1$+N2$
# 880 P5$="THE ACCOUNT NUMBER IS "+A1$
def _parse_string_assignment(tokens: list[str], remainder_string: str) -> list[str]:

    return _parse_assignment(
        tokens,
        remainder_string,
        [2, 3, 4],
        _parse_string_variable,
        "<string_assignment>",
        "<string_expression>"
    )


def _parse_assignment(tokens: list[str], remainder_string: str, eq_positions: list[int],
                      var_parser, assignment_token: str, expression_token: str) -> list[str]:
    eq_pos = None
    for pos in eq_positions:
        if len(remainder_string) > pos and remainder_string[pos] == '=':
            eq_pos = pos
            break
    if eq_pos is None:
        return tokens

    before_eq = remainder_string[:eq_pos]
    after_eq = remainder_string[eq_pos + 1:]

    space_idx = before_eq.find(' ')
    var_string = before_eq[:space_idx] if space_idx != -1 else before_eq

    var_result = var_parser(var_string)
    if var_result[0] == "<no_match>":
        return tokens

    if after_eq.startswith('  '):
        return [ "<error>" ]
    expression_string = after_eq[1:] if after_eq.startswith(' ') else after_eq
    if not expression_string or expression_string.isspace():
        return [ "<error>" ]

    del tokens[-3:]
    tokens[0] = "<parse_complete>"
    tokens.append(assignment_token)
    tokens.extend(var_result)
    tokens.append("<equals>")
    if expression_token == '<string_expression>':
        expr_tokens = _parse_string_expression(expression_string)
        if expr_tokens == ['<error>']:
            return ['<error>']
        tokens.extend(expr_tokens)
    elif expression_token == '<numeric_expression>':
        expr_tokens = _parse_numeric_expression(expression_string)
        if expr_tokens in (['<error>'], ['<no_match>']):
            return ['<error>']
        tokens.extend(expr_tokens)
    return tokens


# Parse a BASIC GOTO statement.
# Example:
# 280 GOTO 400
def _parse_goto(tokens: list[str], remainder_string: str) -> list[str]:
    match = re.match(r'^GOTO (\d+)$', remainder_string)
    if match:
        del tokens[-3:]
        tokens[0] = "<parse_complete>"
        tokens.append("<goto>")
        tokens.append("<line_number_ref>")
        tokens.append(match.group(1))
    return tokens


_NUMERIC_COMPARATORS = {
    '=':  '<equals>',
    '<>': '<not_equal>',
    '>':  '<greater_than>',
    '>=': '<greater_equal>',
    '<':  '<lesser_than>',
    '<=': '<lesser_equal>',
}

_STRING_COMPARATORS = {
    '=':  '<equals>',
    '<>': '<not_equals>',
}

_NUMERIC_OP_TOKENS = {
    '+': '<plus>',
    '-': '<minus>',
    '*': '<times>',
    '/': '<divide>',
    '^': '<power>',
    '(': '<left_paren>',
    ')': '<right_paren>',
}


def _parse_numeric_expression(expr_string: str) -> list[str]:
    result = ['<numeric_expression>']
    s = expr_string

    while s:
        if s.startswith('  '):
            return ['<error>']
        if s.startswith(' '):
            s = s[1:]
            continue

        m = re.match(r'^([A-Z]\d?)(?!\$)', s)
        if m:
            result.extend(_parse_numeric_variable(m.group(1)))
            s = s[m.end():]
            continue

        m = re.match(r'^(\d+(?:\.\d+)?)', s)
        if m:
            result.extend(['<numeric_literal>', m.group(1)])
            s = s[m.end():]
            continue

        if s[0] in _NUMERIC_OP_TOKENS:
            result.append(_NUMERIC_OP_TOKENS[s[0]])
            s = s[1:]
            continue

        return ['<no_match>']

    result.append('<numeric_expression_end>')
    return result


def _parse_string_expression(expr_string: str) -> list[str]:
    result = ['<string_expression>']
    s = expr_string

    while True:
        m = re.match(r'^([A-Z]\d?\$)', s)
        if m:
            result.extend(['<string_variable>', m.group(1)])
            s = s[m.end():]
        else:
            m = re.match(r'^"([^"]*)"', s)
            if m:
                result.extend(['<string_literal>', m.group(1)])
                s = s[m.end():]
            else:
                return ['<error>']

        if not s:
            break

        if s.startswith('  '):
            return ['<error>']
        if s.startswith(' '):
            s = s[1:]

        if not s or s[0] != '+':
            return ['<error>']

        result.append('<concatenate>')
        s = s[1:]

        if not s:
            return ['<error>']

        if s.startswith('  '):
            return ['<error>']
        if s.startswith(' '):
            s = s[1:]

        if not s:
            return ['<error>']

    result.append('<string_expression_end>')
    return result


def _parse_boolean_expression(
    expr_string: str,
    var_regex: str,
    var_token: str,
    comparators: dict,
    expression_token: str,
) -> list[str]:
    comp_pattern = '|'.join(re.escape(c) for c in sorted(comparators, key=len, reverse=True))
    if re.match(rf'^({var_regex})  ', expr_string):
        return ['<error>']
    match = re.match(rf'^({var_regex}) ?({comp_pattern}) ?(.+)$', expr_string)
    if not match:
        return ['<no_match>']
    rest = match.group(3)
    if rest.startswith(' '):
        return ['<error>']
    if expression_token == '<string_expression>':
        expr_tokens = _parse_string_expression(rest)
        if expr_tokens == ['<error>']:
            return ['<error>']
        return [
            '<boolean_expression>',
            var_token,
            match.group(1),
            comparators[match.group(2)],
        ] + expr_tokens + ['<boolean_expression_end>']
    elif expression_token == '<numeric_expression>':
        expr_tokens = _parse_numeric_expression(rest)
        if expr_tokens in (['<error>'], ['<no_match>']):
            return ['<error>']
        return [
            '<boolean_expression>',
            var_token,
            match.group(1),
            comparators[match.group(2)],
        ] + expr_tokens + ['<boolean_expression_end>']
    return ['<error>']


# Parse a BASIC IF/THEN statement.
# Example:
# 730 IF Z>A THEN 800
# 970 IF Q$="YES" THEN 900
def _parse_if_then(tokens: list[str], remainder_string: str) -> list[str]:
    match = re.match(r'^IF (.+) THEN (\d+)$', remainder_string)
    if match:
        expr_string = match.group(1)
        line_ref    = match.group(2)
        if expr_string.endswith(' '):
            return ['<error>']
        bool_tokens = _parse_boolean_expression(
            expr_string, r'[A-Z]\d?', '<numeric_variable>',
            _NUMERIC_COMPARATORS, '<numeric_expression>'
        )
        if bool_tokens == ['<error>']:
            return ['<error>']
        if bool_tokens == ['<no_match>']:
            bool_tokens = _parse_boolean_expression(
                expr_string, r'[A-Z]\d?\$', '<string_variable>',
                _STRING_COMPARATORS, '<string_expression>'
            )
        if bool_tokens in (['<error>'], ['<no_match>']):
            return ['<error>']
        del tokens[-3:]
        tokens[0] = '<parse_complete>'
        tokens.append('<if_then>')
        tokens.append('<if>')
        tokens.extend(bool_tokens)
        tokens.append('<then>')
        tokens.append('<line_number_ref>')
        tokens.append(line_ref)
    return tokens


# Parse a BASIC GOSUB statement.
# Example:
# 650 GOSUB 12000
def _parse_gosub(tokens: list[str], remainder_string: str) -> list[str]:
    match = re.match(r'^GOSUB (\d+)$', remainder_string)
    if match:
        del tokens[-3:]
        tokens[0] = "<parse_complete>"
        tokens.append("<gosub>")
        tokens.append("<line_number_ref>")
        tokens.append(match.group(1))
    return tokens


# Parse a BASIC RETURN statement.
# Example:
# 1680 RETURN
def _parse_return(tokens: list[str], remainder_string: str) -> list[str]:
    if remainder_string == "RETURN":
        del tokens[-3:]
        tokens[0] = "<parse_complete>"
        tokens.append("<gosub_return>")
    return tokens


# Parse a BASIC PRINT statement.
# Example:
# 200 PRINT "HELLO WORLD"
# 220 PRINT T6$
# 240 PRINT X
def _parse_print(tokens: list[str], remainder_string: str) -> list[str]:
    match = re.match(r'^PRINT (.+)$', remainder_string)
    if not match:
        return tokens

    arg = match.group(1)

    num_result = _parse_numeric_variable(arg)
    if num_result[0] != '<no_match>':
        arg_tokens = num_result
    else:
        str_result = _parse_string_variable(arg)
        if str_result[0] != '<no_match>':
            arg_tokens = str_result
        else:
            lit_match = re.match(r'^"([^"]*)"$', arg)
            if lit_match:
                arg_tokens = ['<string_literal>', lit_match.group(1)]
            else:
                return ['<error>']

    del tokens[-3:]
    tokens[0] = '<parse_complete>'
    tokens.append('<print>')
    tokens.extend(arg_tokens)
    return tokens


# Parse a BASIC INPUT statement.
# Example:
# 520 INPUT X
# 540 INPUT T$
# 560 INPUT "WHAT IS YOUR FIRST NUMBER?"; A1
# 580 INPUT "WHAT IS YOUR NAME?"; N$
def _parse_input(tokens: list[str], remainder_string: str) -> list[str]:
    match_with_query = re.match(r'^INPUT "([^"]+)"; ?(.{1,3})$', remainder_string)
    match = re.match(r'^INPUT (.{1,3})$', remainder_string)

    if match_with_query:
        var_string = match_with_query.group(2)
    elif match:
        var_string = match.group(1)
    else:
        return tokens

    num_var_result = _parse_numeric_variable(var_string)
    str_var_result = _parse_string_variable(var_string)
    if num_var_result[0] != "<no_match>":
        var_result = num_var_result
    elif str_var_result[0] != "<no_match>":
        var_result = str_var_result
    else:
        return ["<error>"]

    if match_with_query:
        del tokens[-3:]
        tokens[0] = "<parse_complete>"
        tokens.append("<input>")
        tokens.append("<query_string>")
        tokens.append(match_with_query.group(1))
        tokens.append("<receiving_variable>")
        tokens.extend(var_result)
    elif match:
        del tokens[-3:]
        tokens[0] = "<parse_complete>"
        tokens.append("<input>")
        tokens.append("<receiving_variable>")
        tokens.extend(var_result)
    return tokens


# Parse a BASIC END statement.
# Example:
# 990 END
def _parse_end(tokens: list[str], remainder_string: str) -> list[str]:
    if remainder_string == "END":
        del tokens[-3:]
        tokens[0] = "<parse_complete>"
        tokens.append("<end>")
    return tokens


# --------   "Utility" Parsers for Program Lines   -------- 
# For additional parsing of common constructs, such as variable names or numeric
# expressions, after a program line has been identified as a particular type of
# program line (GOTO, PRINT, etc.).

def _parse_line_number(digits: str) -> str:
    line_number = int(digits)
    if (line_number < 1) or (line_number > MAX_LINE_NUMBER):
        return "<error>"
    else:
        return digits


def _parse_numeric_variable(var_string: str) -> list[str]:
    match = re.match(r'^([A-Z]\d?)$', var_string)
    if match:
        return ["<numeric_variable>", match.group(1)]
    return ["<no_match>"]


def _parse_string_variable(var_string: str) -> list[str]:
    match = re.match(r'^([A-Z]\d?\$)$', var_string)
    if match:
        return ["<string_variable>", match.group(1)]
    return ["<no_match>"]


# --------   Console Command "Primary" Parser   --------

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
