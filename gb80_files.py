import json

from gb80_types import BasicLine


def program_to_json(program_lines: dict[int, BasicLine]) -> str:
    return json.dumps(program_lines, indent=2)
