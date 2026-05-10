import re
from gb80_types import BasicLine


def build_line_object(tokens: list[str]) -> BasicLine:
    return _build_line_object(tokens)


def _build_line_object(tokens: list[str]) -> BasicLine:
    _builders = [
        _build_remark,
        _build_goto,
        _build_if_then,
        _build_print,
        _build_input,
        _build_end,
    ]

    line_object = {}

    for builder in _builders:
        inserts: BasicLine = builder(tokens)
        if inserts:
            line_object |= inserts
            break

    line_object["text"] = string_after("<original_line>", tokens)

    return line_object


def _build_remark(tokens: list[str]) -> BasicLine | None:
    if tokens[4] == "<remark>":
        inserts =  {"op_type": "<remark>"}
        return inserts

    else:
        return None


def _build_goto(tokens: list[str]) -> BasicLine | None:
    if tokens[4] == "<goto>":
        inserts = {"op_type": "<goto>"}

        dest_str = string_after("<line_number_ref>", tokens)
        if dest_str.isdigit():
            dest = int(dest_str)
            inserts["destination"] = dest

        return inserts

    else:
        return None


def _build_if_then(tokens: list[str]) -> BasicLine | None:
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

    match tokens[5]:
        case "<string_variable>":
            inserts: BasicLine = {
                "op_type": "<string_print>",
                "variable": string_after("<string_variable>", tokens)
            }
        case "<string_literal>":
            inserts: BasicLine = {
                "op_type": "<string_print>",
                "string": string_after("<string_literal>", tokens)
                }
        case "<numeric_variable>":
            inserts: BasicLine = {
                "op_type": "<numeric_print>",
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
        inserts =  {"op_type": "<end>"}
        return inserts

    else:
        return None


def string_after(tag: str, tokens: list[str]) -> str:
    return tokens[tokens.index(tag) + 1]


# Methods to build expression objects to insert into program line objects
# for numeric, string and boolean expressions.


def _build_numeric_exp(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<numeric_expression>",
        "completed" : "<no>"
    }


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


def _build_num_op(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<numeric_operation>",
        "completed" : "<no>"
    }


def _build_num_sing(tokens: list[str]) -> BasicLine | None:
    return _build_num_var(tokens) or _build_num_lit(tokens)


def _build_string_exp(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<string_expression>",
        "completed" : "<no>"
    }


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


def _build_str_op(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<string_operation>",
        "completed" : "<no>"
    }


def _build_str_sing(tokens: list[str]) -> BasicLine | None:
    return _build_str_var(tokens) or _build_str_lit(tokens)


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
    