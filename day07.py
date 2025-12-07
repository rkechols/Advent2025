from collections import defaultdict

from utils import get_input_file_path

EMPTY = "."
START = "S"
SPLITTER = "^"


def get_input() -> tuple[int, list[set[int]]]:
    line_lengths: set[int] = set()
    starting_col: int | None = None
    splitters: list[set[int]] = []
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
                    if starting_col is not None:
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
                    splitters.append(this_row_splitters)
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise
    if starting_col is None:
        raise ValueError("Never found start marker")
    if len(line_lengths) != 1:
        raise ValueError("Inconsistent line lengths")
    return starting_col, splitters


def main():
    starting_col, splitters = get_input()

    beam_split_count = 0
    counts_by_column_current = {starting_col: 1}
    for this_row_splitters in splitters:
        current_columns = set(counts_by_column_current)
        counts_by_column_new: dict[int, int] = defaultdict(int)
        # what beams hit splitters?
        splitter_hits = current_columns.intersection(this_row_splitters)
        beam_split_count += len(splitter_hits)
        for col in splitter_hits:
            multiplicity = counts_by_column_current[col]
            for shift in [-1, 1]:  # new beam on either side of the splitter
                new_col = col + shift
                counts_by_column_new[new_col] += multiplicity
        # what beams miss splitters?
        splitter_misses = current_columns - this_row_splitters
        for col in splitter_misses:
            counts_by_column_new[col] += counts_by_column_current[col]
        # prep for next iteration
        counts_by_column_current = counts_by_column_new
    print(f"{beam_split_count = }")
    timeline_count = sum(counts_by_column_current.values())
    print(f"{timeline_count = }")


if __name__ == "__main__":
    main()
