from typing import Callable
from gb80_line_objects import get_line_numbers


def _cmd_show_line_numbers(arg: str) -> list[str]:
    numbers = get_line_numbers()
    return [str(n) for n in numbers] if numbers else ["(NO PROGRAM LINES)"]


DEV_COMMANDS: dict[str, Callable[[str], list[str]]] = {
    "SHOW LINE-NUMBERS": _cmd_show_line_numbers,
}
