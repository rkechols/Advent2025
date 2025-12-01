from pathlib import Path

INPUTS_DIR = Path(__file__).parent / "inputs"


def get_input_file_path(day_number: int) -> Path:
    return INPUTS_DIR / f"day{day_number:02d}.txt"
