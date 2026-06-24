import json
import re
from pathlib import Path
from typing import Callable

from gb80_line_objects import get_program_as_json
from gb80_types import ProgramLines

SAVE_DIR = Path("gb80_files")


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
    path = SAVE_DIR / filename
    path.write_text(get_program_as_json())
    output_text(f'PROGRAM SAVED AS "{filename.upper()}"')


def load_gb80_file(filename: str) -> ProgramLines | None:
    path = SAVE_DIR / filename
    try:
        data = json.loads(path.read_text())
        return {int(k): v for k, v in data.items()}
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return None
