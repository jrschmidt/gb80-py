import json
import re
from typing import Callable

from gb80_types import BasicLine


def program_to_json(program_lines: dict[int, BasicLine]) -> str:
    return json.dumps(program_lines, indent=2)


def is_valid_gb80_filename(name: str) -> bool:
    return bool(re.match(r'^[A-Za-z0-9]{1,8}$', name))


def save_gb80_file(filename: str, output_text: Callable) -> None:
    output_text("FILE SAVE IS NOT YET IMPLEMENTED")
