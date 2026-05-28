from typing import Callable, Generator
from gb80_program_runner import run_program
from gb80_line_objects import (
    clear_all_program_lines,
    delete_program_line,
    get_line_numbers,
    get_line_object,
)


def execute_console_command(tokens: list[str], output_text: Callable) -> None:
    _execute_console_command(tokens, output_text)


def _execute_console_command(tokens: list[str], output_text: Callable) -> None:
    command = tokens[2]
    if command == "<list>":
        execute_list_command(output_text)
    if command == "<clear>":
        execute_clear_command()
    if command == "<run>":
        execute_run_command(output_text)
    if command == "<delete_program_line>":
        delete_program_line(int(tokens[4]))


def execute_list_command(output_text: Callable) -> None:
    for line_number in get_line_numbers():
        line = get_line_object(line_number)
        text = line["text"]
        output_text(text)


def execute_clear_command() -> None:
    clear_all_program_lines()


_program_gen: Generator | None = None


def execute_run_command(output_text: Callable) -> None:
    global _program_gen
    _program_gen = run_program(output_text)
    _advance_program()


def _advance_program() -> None:
    global _program_gen
    try:
        next(_program_gen)
    except StopIteration:
        _program_gen = None


def resume_with_input(value: str) -> None:
    global _program_gen
    if _program_gen is None:
        return
    try:
        _program_gen.send(value)
    except StopIteration:
        _program_gen = None


def is_waiting_for_input() -> bool:
    return _program_gen is not None
