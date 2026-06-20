import json
import re
from pathlib import Path
from typing import Callable

from gb80_types import BasicLine
from gb80_line_objects import get_line_numbers, get_line_object

SAVE_DIR = Path("gb80_files")


def program_to_json(program_lines: dict[int, BasicLine]) -> str:
    return json.dumps(program_lines, indent=2)


def is_valid_gb80_filename(name: str) -> bool:
    return bool(re.match(r'^[A-Za-z0-9]{1,8}$', name))


def list_gb80_files(output_text: Callable) -> None:
    if not SAVE_DIR.exists():
        output_text("NO SAVED FILES")
        return
    files = sorted(p.name for p in SAVE_DIR.iterdir() if p.suffix == ".gb80")
    if not files:
        output_text("NO SAVED FILES")
        return
    for f in files:
        output_text(f.upper())


def save_gb80_file(filename: str, output_text: Callable) -> None:
    SAVE_DIR.mkdir(exist_ok=True)
    program_lines = {
        n: get_line_object(n)
        for n in get_line_numbers()
        if get_line_object(n) is not None
    }
    path = SAVE_DIR / filename
    path.write_text(program_to_json(program_lines))
    output_text("PROGRAM SAVED")
