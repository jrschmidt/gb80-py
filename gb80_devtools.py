from typing import Callable
from gb80_line_objects import get_line_numbers, get_line_object


_dev_state: dict[str, bool] = {"show_tokens": False}


def _cmd_help(arg: str) -> list[str]:
    return DEV_HELP_LINES


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


def _cmd_tokens_on(arg: str) -> list[str]:
    _dev_state["show_tokens"] = True
    return ["[SHOW TOKENS ON]"]


def _cmd_tokens_off(arg: str) -> list[str]:
    _dev_state["show_tokens"] = False
    return ["[SHOW TOKENS OFF]"]


DEV_COMMANDS: dict[str, Callable[[str], list[str]]] = {
    "HELP": _cmd_help,
    "SHOW LINE-NUMBERS": _cmd_show_line_numbers,
    "SHOW LINE-OBJECT": _cmd_show_line_object,
    "TOKENS-ON": _cmd_tokens_on,
    "TOKENS-OFF": _cmd_tokens_off,
}

DEV_HELP_LINES: list[str] = [
    "Available DEV mode commands:",
    "help",
    "show line-numbers",
    "tokens-on",
    "tokens-off",
    "show line-object <line number>",
]
