from collections.abc import Sequence

from utils import get_input_file_path


DIGITS_DESCENDING = [9, 8, 7, 6, 5, 4, 3, 2, 1]


def max_joltage_in_line(digits: Sequence[int], *, k: int):
    n = len(digits)
    previous_chosen_index = -1
    chosen_digits: list[int] = []
    for i in range(k):
        k_after = k - i - 1
        for target_digit in DIGITS_DESCENDING:
            try:
                target_digit_index = digits.index(target_digit, previous_chosen_index + 1, n - k_after)
            except ValueError:
                continue
            chosen_digits.append(target_digit)
            previous_chosen_index = target_digit_index
            break
        else:
            raise ValueError(f"Goofed when finding max joltage")
    max_joltage = int("".join(str(d) for d in chosen_digits))
    return max_joltage


def main():
    joltage_sum_from_2 = 0
    joltage_sum_from_12 = 0
    with open(get_input_file_path(3), "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                digits = list(map(int, line.strip()))
                joltage_sum_from_2 += max_joltage_in_line(digits, k=2)
                joltage_sum_from_12 += max_joltage_in_line(digits, k=12)
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise
    print(f"{joltage_sum_from_2 = }")
    print(f"{joltage_sum_from_12 = }")


if __name__ == "__main__":
    main()
