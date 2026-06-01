from typing import Callable
from gb80_line_objects import get_line_numbers, get_line_object


_dev_state: dict[str, bool] = {"show_tokens": False}


def _cmd_help(arg: str) -> list[str]:
    return DEV_HELP_LINES


def _cmd_show_line_numbers(arg: str) -> list[str]:
    numbers = get_line_numbers()
    return [str(n) for n in numbers] if numbers else ["[no program lines]"]


def _format_line_object(obj, prefix="") -> list[str]:
    lines = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            full_key = f"{prefix}{k}" if prefix else k
            if isinstance(v, (dict, list)):
                lines.extend(_format_line_object(v, f"{full_key}."))
            else:
                lines.append(f"{full_key}: {v}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            lines.extend(_format_line_object(item, f"{prefix}{i}."))
    else:
        lines.append(f"{prefix.rstrip('.')}: {obj}")
    return lines


def _cmd_show_line_object(arg: str) -> list[str]:
    try:
        line_number = int(arg)
    except ValueError:
        return [f"[invalid line number: {arg}]"]
    line_object = get_line_object(line_number)
    if line_object is None:
        return [f"[no program line {line_number}]"]
    return _format_line_object(line_object)


def _cmd_list(arg: str) -> list[str]:
    numbers = get_line_numbers()
    if not numbers:
        return ["[no program lines]"]
    return [line["text"] for n in numbers if (line := get_line_object(n)) is not None]


def _cmd_tokens_on(arg: str) -> list[str]:
    _dev_state["show_tokens"] = True
    return ["[show tokens on]"]


def _cmd_tokens_off(arg: str) -> list[str]:
    _dev_state["show_tokens"] = False
    return ["[show tokens off]"]


DEV_COMMANDS: dict[str, Callable[[str], list[str]]] = {
    "help": _cmd_help,
    "list": _cmd_list,
    "show line-numbers": _cmd_show_line_numbers,
    "show line-object": _cmd_show_line_object,
    "slo": _cmd_show_line_object,
    "tokens-on": _cmd_tokens_on,
    "tokens-off": _cmd_tokens_off,
}

DEV_HELP_LINES: list[str] = [
    "Available DEV mode commands:",
    "help",
    "show line-numbers",
    "tokens-on",
    "tokens-off",
    "show line-object <line number>",
    "slo <line number>",
    "list",
]
