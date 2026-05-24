from typing import Callable
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


def execute_run_command(output_text: Callable) -> None:
    run_program(output_text)
