import re

from utils import get_input_file_path


def main():
    fresh_ranges: list[range] = []
    fresh_count = 0
    with open(get_input_file_path(5), "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            try:
                if line == "":
                    continue
                elif match := re.fullmatch(r"(\d+)-(\d+)", line):
                    r_start, r_end = map(int, match.groups())
                    fresh_ranges.append(range(r_start, r_end + 1))
                else:
                    id_to_check = int(line)
                    if any(
                        id_to_check in r
                        for r in fresh_ranges
                    ):
                        fresh_count += 1
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise
    print(f"{fresh_count = }")


if __name__ == "__main__":
    main()
