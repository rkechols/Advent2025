import itertools
import re
from collections.abc import Iterable

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


def part1(input_: str):
    parsed_lines: list[list[int]] = []
    operators: list[str] = []
    for line_number, line in enumerate(input_.splitlines(), start=1):
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
    print(f"Part 1: {grand_total = }")


def part2(input_: str):
    lines = input_.splitlines()
    # transpose
    cols = ["".join(col) for col in itertools.zip_longest(*lines, fillvalue=" ")]
    if not cols[-1].isspace():  # ensure there's a final column of spaces
        cols.append(" ")
    grand_total = 0
    nums: list[int] = []
    operator: str | None = None
    for col in cols:
        if col.isspace():  # do this calculation
            if not operator:
                raise ValueError("No operator found before blank col triggered calculation")
            if not nums:
                raise ValueError("No numbers found before blank col triggered calculation")
            grand_total += OPERATORS[operator](nums)
            # reset for the next calculation
            nums = []
            operator = None
        else:
            match = re.fullmatch(r"(\d+)\s*([*+]?)", col.strip())
            if not match:
                raise ValueError(f"Invalid column value: {col!r}")
            num_str, maybe_operator = match.groups()
            nums.append(int(num_str))
            if maybe_operator:
                if operator:
                    raise ValueError("Multiple operators found in same section")
                operator = maybe_operator
    print(f"Part 2: {grand_total = }")


def main():
    with open(get_input_file_path(6), "r", encoding="utf-8") as f:
        input_ = f.read()
    part1(input_)
    part2(input_)


if __name__ == "__main__":
    main()
