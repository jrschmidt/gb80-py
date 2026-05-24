from typing import Callable
from gb80_types import BasicLine
from gb80_line_objects import get_line_numbers, get_line_object


_BASIC_KEYWORDS: dict[str, str] = {
    "<remark>":             "REM",
    "<goto>":               "GOTO",
    "<if_then>":            "IF/THEN",
    "<string_print>":       "PRINT",
    "<numeric_print>":      "PRINT",
    "<string_input>":       "INPUT",
    "<numeric_input>":      "INPUT",
    "<end>":                "END",
    "<string_assignment>":  "--String Assignment--",
    "<numeric_assignment>": "--Numeric Assignment--",
}


def run_program(output_text: Callable) -> None:
    _run_program(get_line_numbers(), output_text)


def _run_program(line_numbers: list[int], output_text: Callable) -> None:
    for current_line in line_numbers:
        line_object = get_line_object(current_line)
        if line_object:
            execute_program_line(current_line, line_object, output_text)


def execute_program_line(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    match op_type:
        case "<remark>":             _run_remark(line_number, line_object, output_text)
        case "<goto>":               _run_goto(line_number, line_object, output_text)
        case "<if_then>":            _run_if_then(line_number, line_object, output_text)
        case "<numeric_assignment>": _run_numeric_assignment(line_number, line_object, output_text)
        case "<string_assignment>":  _run_string_assignment(line_number, line_object, output_text)
        case "<numeric_input>":      _run_numeric_input(line_number, line_object, output_text)
        case "<string_input>":       _run_string_input(line_number, line_object, output_text)
        case "<numeric_print>":      _run_numeric_print(line_number, line_object, output_text)
        case "<string_print>":       _run_string_print(line_number, line_object, output_text)
        case "<end>":                _run_end(line_number, line_object, output_text)


def _run_remark(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    keyword = _BASIC_KEYWORDS.get(op_type, op_type)
    output_text(f"LINE {line_number} {keyword}")


def _run_goto(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    keyword = _BASIC_KEYWORDS.get(op_type, op_type)
    output_text(f"LINE {line_number} {keyword}")


def _run_if_then(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    keyword = _BASIC_KEYWORDS.get(op_type, op_type)
    output_text(f"LINE {line_number} {keyword}")


def _run_numeric_assignment(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    keyword = _BASIC_KEYWORDS.get(op_type, op_type)
    output_text(f"LINE {line_number} {keyword}")


def _run_string_assignment(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    keyword = _BASIC_KEYWORDS.get(op_type, op_type)
    output_text(f"LINE {line_number} {keyword}")


def _run_numeric_input(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    keyword = _BASIC_KEYWORDS.get(op_type, op_type)
    output_text(f"LINE {line_number} {keyword}")


def _run_string_input(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    keyword = _BASIC_KEYWORDS.get(op_type, op_type)
    output_text(f"LINE {line_number} {keyword}")


def _run_numeric_print(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    keyword = _BASIC_KEYWORDS.get(op_type, op_type)
    output_text(f"LINE {line_number} {keyword}")


def _run_string_print(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    keyword = _BASIC_KEYWORDS.get(op_type, op_type)
    output_text(f"LINE {line_number} {keyword}")


def _run_end(line_number: int, line_object: BasicLine, output_text: Callable) -> None:
    op_type = line_object.get("op_type", "")
    keyword = _BASIC_KEYWORDS.get(op_type, op_type)
    output_text(f"LINE {line_number} {keyword}")
