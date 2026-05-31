import re
from gb80_types import BasicLine


def build_line_object(tokens: list[str]) -> BasicLine:
    return _build_line_object(tokens)


def _build_line_object(tokens: list[str]) -> BasicLine:
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

    line_object: BasicLine = {}

    for builder in _builders:
        inserts = builder(tokens)
        if inserts:
            line_object |= inserts
            break

    line_object["text"] = string_after("<original_line>", tokens)

    return line_object


def _build_remark(tokens: list[str]) -> BasicLine | None:
    if tokens[4] == "<remark>":
        inserts: BasicLine = {"op_type": "<remark>"}
        return inserts

    else:
        return None


def _build_numeric_assignment(tokens: list[str]) -> BasicLine | None:
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
    }


def _build_string_assignment(tokens: list[str]) -> BasicLine | None:
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
    }


def _build_goto(tokens: list[str]) -> BasicLine | None:
    if tokens[4] == "<goto>":
        inserts: BasicLine = {"op_type": "<goto>"}

        dest_str = string_after("<line_number_ref>", tokens)
        if dest_str.isdigit():
            dest = int(dest_str)
            inserts["destination"] = dest

        return inserts

    else:
        return None


def _build_if_then(tokens: list[str]) -> BasicLine | None:
    if tokens[4] != "<if_then>":
        return None

    inserts: BasicLine = {"op_type": "<if_then>"}

    expression = _build_boolean_exp(tokens[6:-5])
    if expression is None:
        return None
    inserts["expression"] = expression

    inserts["destination"] = int(string_after("<line_number_ref>", tokens))

    return inserts


def _build_print(tokens: list[str]) -> BasicLine | None:
    if tokens[4] != "<print>":
        return None

    inserts: BasicLine = {}
    match tokens[5]:
        case "<string_variable>":
            inserts = {
                "op_type": "<print_string_variable>",
                "variable": string_after("<string_variable>", tokens).rstrip("$")
            }
        case "<string_literal>":
            inserts = {
                "op_type": "<print_string_literal>",
                "string": string_after("<string_literal>", tokens)
            }
        case "<numeric_variable>":
            inserts = {
                "op_type": "<print_numeric_variable>",
                "variable": string_after("<numeric_variable>", tokens)
            }

    return inserts


def _build_input(tokens: list[str]) -> BasicLine | None:
    if tokens[4] != "<input>":
        return None

    inserts: BasicLine = {"op_type": "<input>"}

    if tokens[5] == "<query_string>":
        inserts["query_string"] = string_after("<query_string>", tokens)

    var_type = string_after("<receiving_variable>", tokens)

    if var_type == "<numeric_variable>":
        inserts["op_type"] = "<numeric_input>"
        inserts["variable"] = string_after("<numeric_variable>", tokens)
    else:
        inserts["op_type"] = "<string_input>"
        var_name = string_after("<string_variable>", tokens)
        inserts["variable"] = var_name.rstrip("$")

    return inserts


def _build_end(tokens: list[str]) -> BasicLine | None:
    if tokens[4] == "<end>":
        inserts: BasicLine = {"op_type": "<end>"}
        return inserts

    else:
        return None


def string_before(tag: str, tokens: list[str]) -> str:
    return tokens[tokens.index(tag) - 1]


def string_after(tag: str, tokens: list[str]) -> str:
    return tokens[tokens.index(tag) + 1]


# Methods to build expression objects to insert into program line objects
# for numeric, string and boolean expressions.


def _build_numeric_exp(tokens: list[str]) -> BasicLine | None:
    if tokens[0] != "<numeric_expression>" or tokens[-1] != "<numeric_expression_end>":
        return None
    if len(tokens) == 4:
        return _build_num_sing(tokens[1:-1])
    return _build_num_op(tokens)


def _build_num_lit(tokens: list[str]) -> BasicLine | None:
    try:
        number = float(tokens[1])
    except ValueError:
        return None
    return {
        "op" : "<numeric_literal>",
        "number" : number,
    }


def _build_num_var(tokens: list[str]) -> BasicLine | None:
    if not re.fullmatch(r'[A-Z][0-9]?', tokens[1]):
        return None
    return {
        "op" : "<numeric_variable>",
        "variable" : tokens[1],
    }


def _build_num_sing(tokens: list[str]) -> BasicLine | None:
    if len(tokens) != 2:
        return None
    return _build_num_var(tokens) or _build_num_lit(tokens)


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


def _build_num_op(tokens: list[str]) -> BasicLine | None:
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


def _build_string_exp(tokens: list[str]) -> BasicLine | None:
    if tokens[0] != "<string_expression>" or tokens[-1] != "<string_expression_end>":
        return None
    if "<concatenate>" not in tokens:
        return _build_str_sing(tokens[1:-1])
    return _build_str_op(tokens)


def _build_str_lit(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<string_literal>",
        "string" : tokens[1],
    }


def _build_str_var(tokens: list[str]) -> BasicLine | None:
    var_name = tokens[1].rstrip("$")
    if not re.fullmatch(r'[A-Z][0-9]?', var_name):
        return None
    return {
        "op" : "<string_variable>",
        "variable" : var_name,
    }


def _build_str_sing(tokens: list[str]) -> BasicLine | None:
    if len(tokens) != 2:
        return None
    return _build_str_var(tokens) or _build_str_lit(tokens)


def _build_str_op(tokens: list[str]) -> BasicLine | None:
    if tokens[0] != "<string_expression>" or tokens[-1] != "<string_expression_end>":
        return None
    if "<concatenate>" not in tokens:
        return None

    terms = []
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


def _build_boolean_exp(tokens: list[str]) -> BasicLine | None:
    if tokens[0] != "<boolean_expression>" or tokens[-1] != "<boolean_expression_end>":
        return None

    match tokens[1]:
        case "<numeric_variable>":
            return _build_num_bool_exp(tokens)
        case "<string_variable>":
            return _build_str_bool_exp(tokens)
        case _:
            return None


def _build_num_bool_exp(tokens: list[str]) -> BasicLine | None:
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

    inserts: BasicLine = {
        "comparator": tokens[3],
        "variable": var_name,
        "term": term,
    }
    return inserts


def _build_str_bool_exp(tokens: list[str]) -> BasicLine | None:
    if tokens[3] not in {"<string_equals>", "<string_not_equal>"}:
        return None

    var_name = string_after("<string_variable>", tokens)
    var_name = var_name.rstrip("$")
    if not re.fullmatch(r'[A-Z][0-9]?', var_name):
        return None

    term = _build_str_sing([tokens[5], tokens[6]])
    if term is None:
        return None

    inserts: BasicLine = {
        "comparator": tokens[3],
        "variable": var_name,
        "term": term,
    }
    return inserts
    