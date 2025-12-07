import re

from utils import get_input_file_path

EMPTY = "."
START = "S"
SPLITTER = "^"


def main():
    line_lengths: set[int] = set()
    beam_columns: set[int] = set()
    splitter_rows: list[set[int]] = []
    with open(get_input_file_path(7), "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                line = line.strip()
                if not line:
                    continue
                line_lengths.add(len(line))
                chars = set(line)
                if line_number == 1:
                    if chars != {EMPTY, START}:
                        raise ValueError(f"Unexpected line contents: {chars}")
                    if len(beam_columns) > 0:
                        raise ValueError(f"Oops: multiple starting lines?")
                    beam_columns = {
                        i
                        for i, char in enumerate(line)
                        if char == START
                    }
                    if len(beam_columns) != 1:
                        raise ValueError(f"Unexpected number of starting locations")
                elif line_number % 2 == 0:
                    if chars != {EMPTY}:
                        raise ValueError(f"Unexpected line contents: {chars}")
                else:
                    if chars != {EMPTY, SPLITTER}:
                        raise ValueError(f"Unexpected line contents: {chars}")
                    this_row_splitters = {
                        i
                        for i, char in enumerate(line)
                        if char == SPLITTER
                    }
                    splitter_rows.append(this_row_splitters)
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise
    if not beam_columns:
        raise ValueError("Never found start marker")
    if len(line_lengths) != 1:
        raise ValueError("Inconsistent line lengths")
    line_length = next(iter(line_lengths))

    split_count = 0
    for this_row_splitters in splitter_rows:
        new_beam_columns: set[int] = set()
        # what beams hit splitters?
        splitter_hits = beam_columns.intersection(this_row_splitters)
        split_count += len(splitter_hits)
        for splitter in splitter_hits:
            for shift in [-1, 1]:  # new beam on either side of the splitter
                new_beam = splitter + shift
                if not (0 <= new_beam < line_length):
                    print("WARNING: beam out of bounds")
                new_beam_columns.add(new_beam)
        # what beams miss splitters?
        splitter_misses = beam_columns - this_row_splitters
        new_beam_columns.update(splitter_misses)
        # prep for next iteration
        beam_columns = new_beam_columns
    print(f"{split_count = }")


if __name__ == "__main__":
    main()
