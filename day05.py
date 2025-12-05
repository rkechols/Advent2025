import itertools
import re

from utils import get_input_file_path


def ranges_union(r1: range, r2: range) -> range | None:
    if r1.stop < r2.start or r2.stop < r1.start:  # no overlap
        return None
    start = min(r1.start, r2.start)
    stop = max(r1.stop, r2.stop)
    return range(start, stop)


def main():
    fresh_ranges: list[range] = []
    ids_to_check: list[int] = []
    with open(get_input_file_path(5), "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            try:
                if line == "":
                    continue
                elif match := re.fullmatch(r"(\d+)-(\d+)", line):
                    r_start, r_end = map(int, match.groups())
                    if r_start > r_end:
                        raise ValueError("Range not in proper order")
                    fresh_ranges.append(range(r_start, r_end + 1))
                else:
                    ids_to_check.append(int(line))
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise
    fresh_ranges.sort(key=lambda r: r.start)  # essential for part 2 to work correctly
    fresh_count = sum(
        any(id_to_check in r for r in fresh_ranges)
        for id_to_check in ids_to_check
    )
    print(f"{fresh_count = }")

    merged_ranges: list[range] = [fresh_ranges[0]]
    for new_range in fresh_ranges:
        for i, existing_range in enumerate(merged_ranges):
            if (merged_range := ranges_union(new_range, existing_range)) is not None:
                merged_ranges[i] = merged_range
                break
        else:
            merged_ranges.append(new_range)
    for r1, r2 in itertools.pairwise(merged_ranges):
        if ranges_union(r1, r2) is not None:
            print("BAD")
    n_fresh_total = sum(len(r) for r in merged_ranges)
    print(f"{n_fresh_total = }")


if __name__ == "__main__":
    main()
