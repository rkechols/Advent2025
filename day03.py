from utils import get_input_file_path


DIGITS_DESCENDING = [9, 8, 7, 6, 5, 4, 3, 2, 1]


def max_joltage_in_line(digits: list[int]):
    for target_digit_a in DIGITS_DESCENDING:
        try:
            i = digits.index(target_digit_a, 0, -1)
        except ValueError:
            continue
        for target_digit_b in DIGITS_DESCENDING:
            try:
                digits.index(target_digit_b, i + 1)
            except ValueError:
                continue
            max_joltage = int(f"{target_digit_a}{target_digit_b}")
            return max_joltage
    raise ValueError("Goofed when finding max joltage in line")


def main():
    joltage_sum = 0
    with open(get_input_file_path(3), "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                digits = list(map(int, line.strip()))
                max_joltage = max_joltage_in_line(digits)
                joltage_sum += max_joltage
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise
    print(f"{joltage_sum = }")


if __name__ == "__main__":
    main()
