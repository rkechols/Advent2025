import numpy as np

from utils import get_input_file_path

SYMBOL_TO_BOOL = {
    "@": True,  # roll
    ".": False,  # empty
}


def count_neighbors(grid: np.ndarray, i: int, j: int) -> int:
    count = 0
    for i_shift in [-1, 0, 1]:
        i_new = i + i_shift
        for j_shift in [-1, 0, 1]:
            if i_shift == 0 and j_shift == 0:
                continue  # don't look at the center
            j_new = j + j_shift
            count += int(grid[i_new, j_new])
    return count


def main():
    with open(get_input_file_path(4), "r", encoding="utf-8") as f:
        grid = np.array([
            [
                SYMBOL_TO_BOOL[c]
                for c in line.strip()
            ]
            for line in f
        ])
    grid = np.pad(grid, 1)
    n_rows, n_cols = grid.shape
    count = 0
    for i in range(1, n_rows - 1):
        for j in range(1, n_cols - 1):
            if not grid[i, j]:
                continue
            n_neighbors = count_neighbors(grid, i, j)
            if n_neighbors < 4:
                count += 1
    print(f"Removable count: {count}")


if __name__ == "__main__":
    main()
