import re
from collections.abc import Iterable

import numpy as np

from utils import get_input_file_path


def product(values: Iterable[int]) -> int:
    prod = 1
    for value in values:
        prod *= value
    return prod


OPERATORS = {
    "+": sum,
    "*": product,
}


def main():
    parsed_lines: list[list[int]] = []
    operators: list[str] = []
    with open(get_input_file_path(6), "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                line = line.strip()
                if not line:
                    continue
                line_split = line.split()
                if line_split[0] in OPERATORS:
                    if operators:
                        raise ValueError("Multiple operator rows found")
                    operators = line_split
                    continue
                parsed_lines.append(list(map(int, line_split)))
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise
    if not operators:
        raise ValueError("No operators found")
    line_lengths = {len(line) for line in parsed_lines}
    line_lengths.add(len(operators))
    if len(line_lengths) != 1:
        raise ValueError(f"Inconsistent line lengths: {sorted(line_lengths)}")
    grand_total = 0
    for i, operator in enumerate(operators):
        column = (row[i] for row in parsed_lines)
        this_answer = OPERATORS[operator](column)
        grand_total += this_answer
    print(f"{grand_total = }")


if __name__ == "__main__":
    main()
