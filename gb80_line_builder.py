from gb80_types import BasicLine


def build_line_object(tokens: list[str]) -> BasicLine:
    return _build_line_object(tokens)


def _build_line_object(tokens: list[str]) -> BasicLine:
    _builders = [
        _build_remark,
        _build_goto,
        _build_end,
    ]

    line_object = {}

    for builder in _builders:
        inserts: BasicLine = builder(tokens)
        if inserts:
            line_object |= inserts
            break

    idx = tokens.index("<original_line>")
    line_object["text"] = tokens[idx + 1]

    return line_object


def _build_remark(tokens: list[str]) -> dict | None:
    if tokens[4] == "<remark>":
        inserts =  {"op_type": "<remark>"}
        return inserts

    else:
        return None


def _build_goto(tokens: list[str]) -> dict | None:
    if tokens[4] == "<goto>":
        inserts = {"op_type": "<goto>"}

        idx = tokens.index("<line_number_ref>")
        dest_str = tokens[idx + 1]
        if dest_str.isdigit():
            dest = int(dest_str)
            inserts["destination"] = dest

        return inserts

    else:
        return None


def _build_end(tokens: list[str]) -> dict | None:
    if tokens[4] == "<end>":
        inserts =  {"op_type": "<end>"}
        return inserts

    else:
        return None


# Methods to build expression objects to insert into program line objects.

def _build_expression(tokens: list[str]) -> dict | None:
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


def _build_numeric_exp(tokens) :
    if tokens[0] == "<numeric_expression>" :
        return {
            "op" : "<numeric_expression>",
            "completed" : "<no>"
        }

    else:
        return None


def _build_num_lit(tokens) :
    if tokens[0] == "<numeric_literal>" :
                return {
            "op" : "<numeric_literal>",
            "completed" : "<no>"
        }


    else:
        return None


def _build_num_var(tokens) :
    if tokens[0] == "<numeric_variable>" :
        return {
            "op" : "<numeric_variable>",
            "completed" : "<no>"
        }

    else:
        return None


def _build_num_op(tokens) :
    if tokens[0] == "<numeric_operation>" :
        return {
            "op" : "<numeric_operation>",
            "completed" : "<no>"
        }

    else:
        return None


def _build_num_sing(tokens) :
    if tokens[0] == "<numeric_singleton>" :
        return {
            "op" : "<numeric_singleton>",
            "completed" : "<no>"
        }

    else:
        return None


def _build_string_exp(tokens) :
    if tokens[0] == "<string_expression>" :
        return {
            "op" : "<string_expression>",
            "completed" : "<no>"
        }

    else:
        return None


def _build_str_lit(tokens) :
    if tokens[0] == "<string_literal>" :
        return {
            "op" : "<string_literal>",
            "completed" : "<no>"
        }

    else:
        return None


def _build_str_var(tokens) :
    if tokens[0] == "<string_variable>" :
        return {
            "op" : "<string_variable>",
            "completed" : "<no>"
        }

    else:
        return None


def _build_str_op(tokens) :
    if tokens[0] == "<string_operation>" :
        return {
            "op" : "<string_operation>",
            "completed" : "<no>"
        }

    else:
        return None


def _build_str_sing(tokens) :
    if tokens[0] == "<string_singleton>" :
        return {
            "op" : "<string_singleton>",
            "completed" : "<no>"
        }

    else:
        return None


def _build_boolean_exp(tokens) :
    if tokens[0] == "<boolean_expression>" :
        return {
            "op" : "<boolean_expression>",
            "completed" : "<no>"
        }

    else:
        return None


def _build_num_bool_exp(tokens) :
    if tokens[0] == "<num_bool_expression>" :
        return {
            "op" : "<num_bool_expression>",
            "completed" : "<no>"
        }

    else:
        return None


def _build_str_bool_exp(tokens) :
    if tokens[0] == "<str_bool_expression>" :
        return {
            "op" : "<str_bool_expression>",
            "completed" : "<no>"
        }

    else:
        return None
    