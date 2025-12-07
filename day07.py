from collections import defaultdict

from utils import get_input_file_path

EMPTY = "."
START = "S"
SPLITTER = "^"


def main():
    line_lengths: set[int] = set()
    starting_col = -1
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
                    if starting_col != -1:
                        raise ValueError(f"Oops: multiple starting lines?")
                    starting_columns = {i for i, char in enumerate(line) if char == START}
                    if len(starting_columns) != 1:
                        raise ValueError(f"Unexpected number of starting locations")
                    starting_col = next(iter(starting_columns))
                elif line_number % 2 == 0:
                    if chars != {EMPTY}:
                        raise ValueError(f"Unexpected line contents: {chars}")
                else:
                    if chars != {EMPTY, SPLITTER}:
                        raise ValueError(f"Unexpected line contents: {chars}")
                    this_row_splitters = {i for i, char in enumerate(line) if char == SPLITTER}
                    splitter_rows.append(this_row_splitters)
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise
    if starting_col == -1:
        raise ValueError("Never found start marker")
    if len(line_lengths) != 1:
        raise ValueError("Inconsistent line lengths")
    line_length = next(iter(line_lengths))

    beam_split_count = 0
    current_columns = {starting_col: 1}
    for this_row_splitters in splitter_rows:
        new_columns: dict[int, int] = defaultdict(int)
        # what beams hit splitters?
        splitter_hits = set(current_columns).intersection(this_row_splitters)
        beam_split_count += len(splitter_hits)
        for splitter in splitter_hits:
            multiplicity = current_columns[splitter]
            for shift in [-1, 1]:  # new beam on either side of the splitter
                new_beam = splitter + shift
                if not (0 <= new_beam < line_length):
                    print("WARNING: beam out of bounds")
                new_columns[new_beam] += multiplicity
        # what beams miss splitters?
        splitter_misses = set(current_columns) - this_row_splitters
        for miss in splitter_misses:
            new_columns[miss] += current_columns[miss]
        # prep for next iteration
        current_columns = new_columns
    print(f"{beam_split_count = }")
    timeline_count = sum(current_columns.values())
    print(f"{timeline_count = }")


if __name__ == "__main__":
    main()
