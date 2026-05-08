from gb80_types import BasicLine


def build_line_object(tokens: list[str]) -> BasicLine:
    return _build_line_object(tokens)


def _build_line_object(tokens: list[str]) -> BasicLine:
    _builders = [
        _build_remark,
        _build_goto,
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

def _build_expression(tokens: list[str]) -> BasicLine | None:
    match tokens[0] :

        case "<error>" :
            return None

        case "<numeric_expression>" :
            return _build_numeric_exp(tokens)

        case "<numeric_literal>" :
            return _build_num_lit(tokens)

        case "<numeric_variable>" :
            return _build_num_var(tokens)

        case "<numeric_operation>" :
            return _build_num_op(tokens)

        case "<numeric_singleton>" :
            return _build_num_sing(tokens)

        case "<string_expression>" :
            return _build_string_exp(tokens)

        case "<string_literal>" :
            return _build_str_lit(tokens)

        case "<string_variable>" :
            return _build_str_var(tokens)

        case "<string_operation>" :
            return _build_str_op(tokens)

        case "<string_singleton>" :
            return _build_str_sing(tokens)

        case "<boolean_expression>" :
            return _build_boolean_exp(tokens)

        case "<num_bool_expression>" :
            return _build_num_bool_exp(tokens)

        case "<str_bool_expression>" :
            return _build_str_bool_exp(tokens)

        case _ :
            return None


def _build_numeric_exp(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<numeric_expression>",
        "completed" : "<no>"
    }


def _build_num_lit(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<numeric_literal>",
        "completed" : "<no>"
    }


def _build_num_var(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<numeric_variable>",
        "completed" : "<no>"
    }


def _build_num_op(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<numeric_operation>",
        "completed" : "<no>"
    }


def _build_num_sing(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<numeric_singleton>",
        "completed" : "<no>"
    }


def _build_string_exp(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<string_expression>",
        "completed" : "<no>"
    }


def _build_str_lit(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<string_literal>",
        "completed" : "<no>"
    }


def _build_str_var(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<string_variable>",
        "completed" : "<no>"
    }


def _build_str_op(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<string_operation>",
        "completed" : "<no>"
    }


def _build_str_sing(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<string_singleton>",
        "completed" : "<no>"
    }


def _build_boolean_exp(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<boolean_expression>",
        "completed" : "<no>"
    }


def _build_num_bool_exp(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<num_bool_expression>",
        "completed" : "<no>"
    }


def _build_str_bool_exp(tokens: list[str]) -> BasicLine | None:
    return {
        "op" : "<str_bool_expression>",
        "completed" : "<no>"
    }
    