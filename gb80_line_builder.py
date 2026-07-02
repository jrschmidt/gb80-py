import re
from gb80_types import (
    BasicLine,
    BooleanExp,
    NumericBooleanExp,
    NumericExp,
    NumericFunctionExp,
    NumericLiteralExp,
    NumericOpExp,
    NumericRandomExp,
    NumericVariableExp,
    StringAssignmentLine,
    StringBooleanExp,
    StringExp,
    StringInputLine,
    StringLiteralExp,
    StringOpExp,
    StringVariableExp,
    EndLine,
    GotoLine,
    IfThenLine,
    NumericAssignmentLine,
    NumericInputLine,
    PrintNumericVariableLine,
    PrintStringLiteralLine,
    PrintStringVariableLine,
    RemarkLine,
)


def build_line_object(tokens: list[str]) -> BasicLine | None:
    return _build_line_object(tokens)


def _build_line_object(tokens: list[str]) -> BasicLine | None:
    text = string_after("<original_line>", tokens)
    _builders = [
        _build_remark,
        _build_string_assignment,
        _build_numeric_assignment,
        _build_goto,
        _build_if_then,
        _build_print,
        _build_input,
        _build_end,
    ]
    for builder in _builders:
        result = builder(tokens, text)
        if result is not None:
            return result
    return None


def _build_remark(tokens: list[str], text: str) -> RemarkLine | None:
    if tokens[4] == "<remark>":
        return {"op_type": "<remark>", "text": text}
    return None


def _build_numeric_assignment(tokens: list[str], text: str) -> NumericAssignmentLine | None:
    if (
        tokens[4] != "<numeric_assignment>" or
        tokens[5] != "<numeric_variable>" or
        tokens[7] != "<equals>" or
        tokens[8] != "<numeric_expression>" or
        tokens[-3] != "<numeric_expression_end>"
    ):
        return None

    var_name = string_after("<numeric_variable>", tokens)
    expression = _build_numeric_exp(tokens[8:-2])
    if expression is None:
        return None

    return {
        "op_type": "<numeric_assignment>",
        "variable": var_name,
        "expression": expression,
        "text": text,
    }


def _build_string_assignment(tokens: list[str], text: str) -> StringAssignmentLine | None:
    if (
        tokens[4] != "<string_assignment>" or
        tokens[5] != "<string_variable>" or
        tokens[7] != "<equals>" or
        tokens[8] != "<string_expression>" or
        tokens[-3] != "<string_expression_end>"
    ):
        return None

    var_name = string_after("<string_variable>", tokens).rstrip("$")
    expression = _build_string_exp(tokens[8:-2])
    if expression is None:
        return None

    return {
        "op_type": "<string_assignment>",
        "variable": var_name,
        "expression": expression,
        "text": text,
    }


def _build_goto(tokens: list[str], text: str) -> GotoLine | None:
    if tokens[4] != "<goto>":
        return None

    dest_str = string_after("<line_number_ref>", tokens)
    if not dest_str.isdigit():
        return None

    return {
        "op_type": "<goto>",
        "destination": int(dest_str),
        "text": text,
    }


def _build_if_then(tokens: list[str], text: str) -> IfThenLine | None:
    if tokens[4] != "<if_then>":
        return None

    expression = _build_boolean_exp(tokens[6:-5])
    if expression is None:
        return None

    return {
        "op_type": "<if_then>",
        "expression": expression,
        "destination": int(string_after("<line_number_ref>", tokens)),
        "text": text,
    }


def _build_print(
    tokens: list[str], text: str
) -> PrintStringVariableLine | PrintStringLiteralLine | PrintNumericVariableLine | None:
    if tokens[4] != "<print>":
        return None

    match tokens[5]:
        case "<string_variable>":
            return {
                "op_type": "<print_string_variable>",
                "variable": string_after("<string_variable>", tokens).rstrip("$"),
                "text": text,
            }
        case "<string_literal>":
            return {
                "op_type": "<print_string_literal>",
                "string": string_after("<string_literal>", tokens),
                "text": text,
            }
        case "<numeric_variable>":
            return {
                "op_type": "<print_numeric_variable>",
                "variable": string_after("<numeric_variable>", tokens),
                "text": text,
            }
    return None


def _build_input(tokens: list[str], text: str) -> NumericInputLine | StringInputLine | None:
    if tokens[4] != "<input>":
        return None

    var_type = string_after("<receiving_variable>", tokens)

    if var_type == "<numeric_variable>":
        result: NumericInputLine = {
            "op_type": "<numeric_input>",
            "variable": string_after("<numeric_variable>", tokens),
            "text": text,
        }
        if tokens[5] == "<query_string>":
            result["query_string"] = string_after("<query_string>", tokens)
        return result
    else:
        result2: StringInputLine = {
            "op_type": "<string_input>",
            "variable": string_after("<string_variable>", tokens).rstrip("$"),
            "text": text,
        }
        if tokens[5] == "<query_string>":
            result2["query_string"] = string_after("<query_string>", tokens)
        return result2


def _build_end(tokens: list[str], text: str) -> EndLine | None:
    if tokens[4] == "<end>":
        return {"op_type": "<end>", "text": text}
    return None


def string_before(tag: str, tokens: list[str]) -> str:
    return tokens[tokens.index(tag) - 1]


def string_after(tag: str, tokens: list[str]) -> str:
    return tokens[tokens.index(tag) + 1]


# Methods to build expression objects to insert into program line objects
# for numeric, string and boolean expressions.


NUM_SINGLETON_KEYWORDS = ["<numeric_literal>", "<numeric_variable>"]
NUM_FUNCTION_KEYWORDS = ["<random>"]


def _build_numeric_exp(tokens: list[str]) -> NumericExp | None:
    if tokens[0] != "<numeric_expression>" or tokens[-1] != "<numeric_expression_end>":
        return None
    if find_splitter(tokens) is None:
        if tokens[1] in NUM_SINGLETON_KEYWORDS:
            return _build_num_sing(tokens[1:-1])
        if tokens[1] in NUM_FUNCTION_KEYWORDS:
            return _build_num_func(tokens[1:-1])
        return None
    return _build_num_op(tokens)


def _build_num_lit(tokens: list[str]) -> NumericLiteralExp | None:
    try:
        number = float(tokens[1])
    except ValueError:
        return None
    return {
        "op" : "<numeric_literal>",
        "number" : number,
    }


def _build_num_var(tokens: list[str]) -> NumericVariableExp | None:
    if not re.fullmatch(r'[A-Z][0-9]?', tokens[1]):
        return None
    return {
        "op" : "<numeric_variable>",
        "variable" : tokens[1],
    }


def _build_num_sing(tokens: list[str]) -> NumericLiteralExp | NumericVariableExp | None:
    if len(tokens) != 2:
        return None
    return _build_num_var(tokens) or _build_num_lit(tokens)


def _build_random_func(tokens: list[str]) -> NumericRandomExp | None:
    if tokens[0] == "<random>":
        return {"op": "<random>"}
    return None


def _build_num_func(tokens: list[str]) -> NumericFunctionExp | None:
    if tokens[0] == "<random>":
        return _build_random_func(tokens)
    return None


_OP_ORDER: dict[str, int] = {
    "<plus>": 3, "<minus>": 3,
    "<times>": 2, "<divide>": 2,
    "<power>": 1,
}


def find_splitter(tokens: list[str]) -> int | None:
    nesting_level = 0
    best_idx = None
    best_level = None

    for i, token in enumerate(tokens[1:-1], start=1):
        if token == "<left_paren>":
            nesting_level += 1
        elif token == "<right_paren>":
            if nesting_level == 0:
                return None
            nesting_level -= 1
        elif nesting_level == 0 and token in _OP_ORDER:
            level = _OP_ORDER[token]
            if best_level is None or level > best_level:
                best_idx, best_level = i, level
            elif level == best_level and token != "<power>":
                best_idx = i

    if nesting_level != 0:
        return None

    return best_idx


def prep_op_tokens(tokens: list[str]) -> list[str]:
    if tokens[0] != "<numeric_expression>":
        tokens = ["<numeric_expression>"] + tokens
    if tokens[-1] != "<numeric_expression_end>":
        tokens = tokens + ["<numeric_expression_end>"]

    while len(tokens) >= 4 and tokens[1] == "<left_paren>" and tokens[-2] == "<right_paren>":
        nesting_level = 1
        matched = True
        for token in tokens[2:-2]:
            if token == "<left_paren>":
                nesting_level += 1
            elif token == "<right_paren>":
                nesting_level -= 1
                if nesting_level == 0:
                    matched = False
                    break
        if not matched:
            break
        tokens = ["<numeric_expression>"] + tokens[2:-2] + ["<numeric_expression_end>"]

    return tokens


def _build_num_op(tokens: list[str]) -> NumericOpExp | None:
    idx = find_splitter(tokens)
    if idx is None:
        return None

    operand = tokens[idx]

    left_tokens = prep_op_tokens(tokens[:idx])
    right_tokens = prep_op_tokens(tokens[idx+1:])

    term1 = _build_numeric_exp(left_tokens)
    if term1 is None:
        return None

    term2 = _build_numeric_exp(right_tokens)
    if term2 is None:
        return None

    return {
        "operand": operand,
        "term1": term1,
        "term2": term2,
    }


def _build_string_exp(tokens: list[str]) -> StringExp | None:
    if tokens[0] != "<string_expression>" or tokens[-1] != "<string_expression_end>":
        return None
    if "<concatenate>" not in tokens:
        return _build_str_sing(tokens[1:-1])
    return _build_str_op(tokens)


def _build_str_lit(tokens: list[str]) -> StringLiteralExp | None:
    return {
        "op" : "<string_literal>",
        "string" : tokens[1],
    }


def _build_str_var(tokens: list[str]) -> StringVariableExp | None:
    var_name = tokens[1].rstrip("$")
    if not re.fullmatch(r'[A-Z][0-9]?', var_name):
        return None
    return {
        "op" : "<string_variable>",
        "variable" : var_name,
    }


def _build_str_sing(tokens: list[str]) -> StringLiteralExp | StringVariableExp | None:
    if len(tokens) != 2:
        return None
    return _build_str_var(tokens) or _build_str_lit(tokens)


def _build_str_op(tokens: list[str]) -> StringOpExp | None:
    if tokens[0] != "<string_expression>" or tokens[-1] != "<string_expression_end>":
        return None
    if "<concatenate>" not in tokens:
        return None

    terms: list[StringLiteralExp | StringVariableExp] = []
    inner = tokens[1:-1]
    i = 0
    while i < len(inner):
        if inner[i] == "<concatenate>":
            i += 1
            continue
        if i + 1 >= len(inner):
            return None
        term = _build_str_sing([inner[i], inner[i + 1]])
        if term is None:
            return None
        terms.append(term)
        i += 2

    return {"op": "<string_concatenation>", "terms": terms}


def _build_boolean_exp(tokens: list[str]) -> BooleanExp | None:
    if tokens[0] != "<boolean_expression>" or tokens[-1] != "<boolean_expression_end>":
        return None

    match tokens[1]:
        case "<numeric_variable>":
            return _build_num_bool_exp(tokens)
        case "<string_variable>":
            return _build_str_bool_exp(tokens)
        case _:
            return None


def _build_num_bool_exp(tokens: list[str]) -> NumericBooleanExp | None:
    _comparators = {
        "<numeric_equals>",
        "<numeric_not_equal>",
        "<greater_than>",
        "<greater_equal>",
        "<lesser_than>",
        "<lesser_equal>"
    }

    if tokens[3] not in _comparators:
        return None

    var_name = string_after("<numeric_variable>", tokens)
    if not re.fullmatch(r'[A-Z][0-9]?', var_name):
        return None

    term = _build_num_sing([tokens[5], tokens[6]])
    if term is None:
        return None

    return {
        "comparator": tokens[3],
        "variable": var_name,
        "term": term,
    }


def _build_str_bool_exp(tokens: list[str]) -> StringBooleanExp | None:
    if tokens[3] not in {"<string_equals>", "<string_not_equal>"}:
        return None

    var_name = string_after("<string_variable>", tokens)
    var_name = var_name.rstrip("$")
    if not re.fullmatch(r'[A-Z][0-9]?', var_name):
        return None

    term = _build_str_sing([tokens[5], tokens[6]])
    if term is None:
        return None

    return {
        "comparator": tokens[3],
        "variable": var_name,
        "term": term,
    }
