from pathlib import Path
from typing import Iterable

INPUTS_DIR = Path(__file__).parent / "inputs"


def get_input_file_path(day_number: int) -> Path:
    return INPUTS_DIR / f"day{day_number:02d}.txt"


def product(values: Iterable[int]) -> int:
    prod = 1
    for value in values:
        prod *= value
    return prod
