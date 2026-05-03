from typing import Callable
from gb80_line_objects import get_line_numbers, get_line_object


def _cmd_show_line_numbers(arg: str) -> list[str]:
    numbers = get_line_numbers()
    return [str(n) for n in numbers] if numbers else ["[NO PROGRAM LINES]"]


def _cmd_show_line_object(arg: str) -> list[str]:
    try:
        line_number = int(arg)
    except ValueError:
        return [f"[INVALID LINE NUMBER: {arg}]"]
    line_object = get_line_object(line_number)
    if line_object is None:
        return [f"[NO PROGRAM LINE {line_number}]"]
    return [f"{k}: {v}" for k, v in line_object.items()]


DEV_COMMANDS: dict[str, Callable[[str], list[str]]] = {
    "SHOW LINE-NUMBERS": _cmd_show_line_numbers,
    "SHOW LINE-OBJECT": _cmd_show_line_object,
}
