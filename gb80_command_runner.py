from typing import Callable
from gb80_line_objects import (
    clear_all_program_lines,
    delete_program_line,
    get_line_numbers,
    get_line_object,
)


def execute_console_command(tokens: list[str], append_line: Callable) -> None:
    _execute_console_command(tokens, append_line)


def _execute_console_command(tokens: list[str], append_line: Callable) -> None:
    command = tokens[2]
    if command == "<list>":
        _list_cmd(append_line)
    if command == "<clear>":
        _clear_cmd()
    if command == "<run>":
        _run_cmd(append_line)
    if command == "<delete_program_line>":
        delete_program_line(int(tokens[4]))


def _list_cmd(append_line: Callable) -> None:
    for line_number in get_line_numbers():
        line = get_line_object(line_number)
        text = line["text"]
        append_line(text)


def _clear_cmd() -> None:
    clear_all_program_lines()


def _run_cmd(append_line: Callable) -> None:
    pass
