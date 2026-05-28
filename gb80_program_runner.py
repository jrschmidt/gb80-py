from typing import Callable
from gb80_types import BasicLine
from gb80_line_objects import get_line_numbers, get_line_object
from gb80_variable_registry import (
    start_var_registry,
    set_numeric_variable,
    get_numeric_variable,
    set_string_variable,
    get_string_variable
)


_BASIC_KEYWORDS: dict[str, str] = {
    "<remark>":             "REM",
    "<goto>":               "GOTO",
    "<if_then>":            "IF/THEN",
    "<print_string_variable>":  "PRINT",
    "<print_string_literal>":   "PRINT",
    "<print_numeric_variable>": "PRINT",
    "<string_input>":       "INPUT",
    "<numeric_input>":      "INPUT",
    "<end>":                "END",
    "<string_assignment>":  "--String Assignment--",
    "<numeric_assignment>": "--Numeric Assignment--",
}


_next_line: int | None = None
_input_request: dict | None = None

def _set_next_line(n: int) -> None:
    global _next_line
    _next_line = n

def _set_input_request(var_type: str, variable: str, query: str | None) -> None:
    global _input_request
    _input_request = {"type": var_type, "variable": variable, "query": query}


def run_program(output_text: Callable):
    return _run_program(output_text)


def _run_program(output_text: Callable):
    global _next_line, _input_request
    start_var_registry()
    line_numbers = get_line_numbers()
    if not line_numbers:
        return
    current_line_number = line_numbers[0]
    while True:
        _next_line = None
        _input_request = None
        line_object = get_line_object(current_line_number)
        if line_object:
            execute_program_line(current_line_number, line_object, output_text)
            if _input_request is not None:
                req = _input_request
                user_input = yield req
                if req["type"] == "string":
                    set_string_variable(req["variable"], user_input)
                elif req["type"] == "numeric":
                    try:
                        set_numeric_variable(req["variable"], float(user_input))
                    except ValueError:
                        pass
            if _next_line is not None:
                if _next_line in line_numbers:
                    current_line_number = _next_line
                    continue
                break
        idx = line_numbers.index(current_line_number)
        if idx + 1 >= len(line_numbers):
            break
        current_line_number = line_numbers[idx + 1]


def execute_program_line(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    match op_type:
        case "<remark>":             _run_remark(line_number, line_object, output_text)
        case "<goto>":               _run_goto(line_object)
        case "<end>":                _run_end(line_object)
        case "<if_then>":            _run_if_then(line_object)
        case "<numeric_assignment>": _run_numeric_assignment(line_object)
        case "<string_assignment>":  _run_string_assignment(line_object)
        case "<numeric_input>":      _run_numeric_input(line_object, output_text)
        case "<string_input>":       _run_string_input(line_object, output_text)
        case "<print_string_variable>":  _run_string_var_print(line_object, output_text)
        case "<print_string_literal>":   _run_string_lit_print(line_object, output_text)
        case "<print_numeric_variable>": _run_numeric_print(line_object, output_text)


def _run_remark(line_object: BasicLine) -> None:
    pass


def _run_goto(line_object: BasicLine) -> None:
    if line_object.get("op_type") != "<goto>":
        return
    destination = line_object.get("destination")
    if destination is not None:
        _set_next_line(destination)


def _run_if_then(line_object: BasicLine) -> None:
    if line_object.get("op_type") != "<if_then>":
        return
    result = evaluate_boolean_expression(line_object.get("expression"))
    if result:
        destination = line_object.get("destination")
        if destination is not None:
            _set_next_line(destination)


def _run_numeric_assignment(line_object: BasicLine) -> None:
    if line_object.get("op_type") != "<numeric_assignment>":
        return
    value = evaluate_numeric_expression(line_object.get("expression"))
    if value is None:
        return
    set_numeric_variable(line_object.get("variable"), value)


def _run_string_assignment(line_object: BasicLine) -> None:
    if line_object.get("op_type") != "<string_assignment>":
        return
    value = evaluate_string_expression(line_object.get("expression"))
    if value is None:
        return
    set_string_variable(line_object.get("variable"), value)


def _run_numeric_input(line_object: BasicLine, output_text: Callable) -> None:
    if line_object.get("op_type") != "<numeric_input>":
        return
    query = line_object.get("query_string")
    if query:
        output_text(query)
    _set_input_request("numeric", line_object.get("variable"), query)


def _run_string_input(line_object: BasicLine, output_text: Callable) -> None:
    if line_object.get("op_type") != "<string_input>":
        return
    query = line_object.get("query_string")
    if query:
        output_text(query)
    _set_input_request("string", line_object.get("variable"), query)


def _run_numeric_print(line_object: BasicLine, output_text: Callable) -> None:
    if line_object.get("op_type") != "<print_numeric_variable>":
        return
    value = get_numeric_variable(line_object.get("variable"))
    if value is None:
        return
    output_text(str(int(value)) if value == int(value) else str(value))


def _run_string_var_print(line_object: BasicLine, output_text: Callable) -> None:
    if line_object.get("op_type") != "<print_string_variable>":
        return
    var_name = get_string_variable(line_object.get("variable"))
    if var_name is None:
        return
    output_text(var_name)


def _run_string_lit_print(line_object: BasicLine, output_text: Callable) -> None:
    if line_object.get("op_type") != "<print_string_literal>":
        return
    value = line_object.get("string")
    if value is None:
        return
    output_text(value)


def _run_end(line_object: BasicLine) -> None:
    if line_object.get("op_type") != "<end>":
        return
    _set_next_line(-1)


# Methods to evaluate string, numeric, and boolean expressions.


def evaluate_string_literal(line_object: BasicLine) -> str | None:
    if line_object.get("op") != "<string_literal>":
        return None
    return line_object.get("string")


def evaluate_string_variable(line_object: BasicLine) -> str | None:
    if line_object.get("op") != "<string_variable>":
        return None
    name = line_object.get("variable")
    return get_string_variable(name)


def evaluate_string_singleton(line_object: BasicLine) -> str | None:
    result = evaluate_string_literal(line_object)
    if result is not None:
        return result
    return evaluate_string_variable(line_object)


def evaluate_string_op(line_object: BasicLine) -> str | None:
    if line_object.get("op") != "<string_concatenation>":
        return None
    terms = line_object.get("terms")
    if not terms:
        return None
    parts = []
    for term in terms:
        result = evaluate_string_singleton(term)
        if result is None:
            return None
        parts.append(result)
    return "".join(parts)


def evaluate_string_expression(line_object: BasicLine) -> str | None:
    op = line_object.get("op")
    if op in ("<string_literal>", "<string_variable>"):
        return evaluate_string_singleton(line_object)
    if op == "<string_concatenation>":
        return evaluate_string_op(line_object)
    return None


def evaluate_numeric_literal(line_object: BasicLine) -> float | None:
    if line_object.get("op") != "<numeric_literal>":
        return None
    return line_object.get("number")


def evaluate_numeric_variable(line_object: BasicLine) -> float | None:
    if line_object.get("op") != "<numeric_variable>":
        return None
    name = line_object.get("variable")
    return get_numeric_variable(name)


def evaluate_numeric_singleton(line_object: BasicLine) -> float | None:
    result = evaluate_numeric_literal(line_object)
    if result is not None:
        return result
    return evaluate_numeric_variable(line_object)


def evaluate_numeric_op(line_object: BasicLine) -> float | None:
    operand = line_object.get("operand")
    if operand not in ("<plus>", "<minus>", "<times>", "<divide>", "<power>"):
        return None
    term1 = line_object.get("term1")
    term2 = line_object.get("term2")
    if term1 is None or term2 is None:
        return None
    val1 = evaluate_numeric_expression(term1)
    val2 = evaluate_numeric_expression(term2)
    if val1 is None or val2 is None:
        return None
    match operand:
        case "<plus>":    return val1 + val2
        case "<minus>":   return val1 - val2
        case "<times>":   return val1 * val2
        case "<divide>":  return None if val2 == 0 else val1 / val2
        case "<power>":   return val1 ** val2
    return None


def evaluate_numeric_expression(line_object: BasicLine) -> float | None:
    op = line_object.get("op")
    if op in ("<numeric_literal>", "<numeric_variable>"):
        return evaluate_numeric_singleton(line_object)
    if line_object.get("operand") in ("<plus>", "<minus>", "<times>", "<divide>", "<power>"):
        return evaluate_numeric_op(line_object)
    return None


def evaluate_str_boolean_exp(line_object: BasicLine) -> bool | None:
    comparator = line_object.get("comparator")
    if comparator not in ("<string_equals>", "<string_not_equal>"):
        return None
    var_value = get_string_variable(line_object.get("variable"))
    if var_value is None:
        return None
    term_value = evaluate_string_singleton(line_object.get("term"))
    if term_value is None:
        return None
    match comparator:
        case "<string_equals>":    return var_value == term_value
        case "<string_not_equal>": return var_value != term_value
    return None


def evaluate_num_boolean_exp(line_object: BasicLine) -> bool | None:
    comparator = line_object.get("comparator")
    if comparator not in ("<numeric_equals>", "<numeric_not_equal>", "<lesser_than>",
                          "<lesser_equal>", "<greater_than>", "<greater_equal>"):
        return None
    var_value = get_numeric_variable(line_object.get("variable"))
    if var_value is None:
        return None
    term_value = evaluate_numeric_singleton(line_object.get("term"))
    if term_value is None:
        return None
    match comparator:
        case "<numeric_equals>":    return var_value == term_value
        case "<numeric_not_equal>": return var_value != term_value
        case "<lesser_than>":       return var_value <  term_value
        case "<lesser_equal>":      return var_value <= term_value
        case "<greater_than>":      return var_value >  term_value
        case "<greater_equal>":     return var_value >= term_value
    return None


def evaluate_boolean_expression(line_object: BasicLine) -> bool | None:
    comparator = line_object.get("comparator")
    if comparator in ("<string_equals>", "<string_not_equal>"):
        return evaluate_str_boolean_exp(line_object)
    if comparator in ("<numeric_equals>", "<numeric_not_equal>", "<lesser_than>",
                      "<lesser_equal>", "<greater_than>", "<greater_equal>"):
        return evaluate_num_boolean_exp(line_object)
    return None
