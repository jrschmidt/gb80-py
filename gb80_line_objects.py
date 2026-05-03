from gb80_types import BasicLine

_program_lines: dict[int, BasicLine] = {}


def clear_all_program_lines() -> None:
    global _program_lines
    _program_lines = {}


def add_program_line(line_number: int, program_line: BasicLine) -> None:
    _program_lines[line_number] = program_line


def delete_program_line(line_number: int) -> None:
    _program_lines.pop(line_number, None)


def get_line_numbers() -> list[int]:
    return sorted(_program_lines.keys())


def get_line_object(line_number: int) -> BasicLine | None:
    return _program_lines.get(line_number)
