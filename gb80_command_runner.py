from typing import Any, Callable, Generator
from gb80_constants import HELP_MESSAGE
from gb80_files import is_valid_gb80_filename, list_gb80_files, save_gb80_file
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
    if command == "<save>":
        execute_save_command(tokens, output_text)
    if command == "<files>":
        execute_files_command(output_text)
    if command == "<help>":
        execute_help_command(output_text)


_list_gen: Generator[Any, Any, Any] | None = None


def execute_list_command(output_text: Callable) -> None:
    global _list_gen
    _list_gen = _list_generator(output_text)
    _advance_listing()


def _list_generator(output_text: Callable) -> Generator[Any, Any, Any]:
    line_numbers = get_line_numbers()
    total = len(line_numbers)

    if total <= 22:
        for line_number in line_numbers:
            line = get_line_object(line_number)
            if line is not None:
                output_text(line["text"])
        return

    count = 0
    page_limit = 20

    for i, line_number in enumerate(line_numbers):
        line = get_line_object(line_number)
        if line is None:
            continue
        output_text(line["text"])
        count += 1
        if count >= page_limit and (total - i - 1) > 0:
            output_text("( <ENTER> )")
            yield
            count = 0
            page_limit = 22


def is_listing() -> bool:
    return _list_gen is not None


def _advance_listing() -> None:
    global _list_gen
    if _list_gen is None:
        return
    try:
        next(_list_gen)
    except StopIteration:
        _list_gen = None


def advance_listing() -> None:
    _advance_listing()


def execute_help_command(output_text: Callable) -> None:
    for line in HELP_MESSAGE:
        output_text(line)


def execute_files_command(output_text: Callable) -> None:
    list_gb80_files(output_text)


def execute_save_command(tokens: list[str], output_text: Callable) -> None:
    name = tokens[4]
    if not is_valid_gb80_filename(name):
        output_text("NOT A VALID GB80 FILE NAME")
        return
    filename = name.lower() + ".gb80"
    save_gb80_file(filename, output_text)


def execute_clear_command() -> None:
    clear_all_program_lines()


_program_gen: Generator[Any, Any, Any] | None = None


def execute_run_command(output_text: Callable) -> None:
    global _program_gen
    _program_gen = run_program(output_text)
    _advance_program()


def _advance_program() -> None:
    global _program_gen
    if _program_gen is None:
        return
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
