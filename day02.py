from typing import cast

from utils import get_input_file_path


def count_digits(x: int) -> int:
    return len(str(x))


def is_even(n: int) -> bool:
    return n % 2 == 0


def min_with_n_digits(n: int) -> int:
    return 10 ** (n - 1)


def max_with_n_digits(n: int) -> int:
    return (10 ** n) - 1


def split_digits_into_chunks(x: int, *, n_chunks: int) -> list[int]:
    x_str = str(x)
    chunk_size = len(x_str) // n_chunks
    return [
        int(x_str[(i * chunk_size) : (i + 1) * chunk_size])
        for i in range(n_chunks)
    ]


def sum_invalid_ids_in_fixed_digit_range(r_start: int, r_end: int, *, only_doubles: bool) -> int:
    digit_count = count_digits(r_start)
    invalid_ids: set[int] = set()
    max_chunks = 2 if only_doubles else digit_count  # part 1 vs part 2
    for n_chunks in range(2, max_chunks + 1):
        if digit_count % n_chunks != 0:
            continue
        search_start, *other_chunks = split_digits_into_chunks(r_start, n_chunks=n_chunks)
        if any(chunk > search_start for chunk in other_chunks):
            search_start += 1
        search_end, *other_chunks = split_digits_into_chunks(r_end, n_chunks=n_chunks)
        if any(chunk < search_end for chunk in other_chunks):
            search_end -= 1
        invalid_ids.update(
            int("".join([str(x)] * n_chunks))
            for x in range(search_start, search_end + 1)
        )
    return sum(invalid_ids)


def sum_invalid_ids(ranges: list[tuple[int, int]], *, only_doubles: bool) -> int:
    invalid_ids_sum = 0
    for r_start, r_end in ranges:
        digit_count_start = count_digits(r_start)
        digit_count_end = count_digits(r_end)
        if digit_count_start == digit_count_end:
            invalid_ids_sum += sum_invalid_ids_in_fixed_digit_range(r_start, r_end, only_doubles=only_doubles)
        else:
            invalid_ids_sum += sum_invalid_ids_in_fixed_digit_range(r_start, max_with_n_digits(digit_count_start), only_doubles=only_doubles)
            for digit_count in range(digit_count_start + 1, digit_count_end):
                invalid_ids_sum += sum_invalid_ids_in_fixed_digit_range(
                    min_with_n_digits(digit_count),
                    max_with_n_digits(digit_count),
                    only_doubles=only_doubles,
                )
            invalid_ids_sum += sum_invalid_ids_in_fixed_digit_range(min_with_n_digits(digit_count_end), r_end, only_doubles=only_doubles)
    return invalid_ids_sum


def main():
    with open(get_input_file_path(2), "r", encoding="utf-8") as f:
        ranges_raw = f.read().strip().split(",")
    ranges = [
        cast(tuple[int, int], tuple(map(int, range_raw.split("-"))))
        for range_raw in ranges_raw
    ]
    invalid_ids_sum = sum_invalid_ids(ranges, only_doubles=True)
    print(f"Part 1: {invalid_ids_sum = }")
    invalid_ids_sum = sum_invalid_ids(ranges, only_doubles=False)
    print(f"Part 2: {invalid_ids_sum = }")
    # 25027947512 is too LOW


if __name__ == "__main__":
    main()
