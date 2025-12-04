import numpy as np

from utils import get_input_file_path

SYMBOL_TO_BOOL = {
    "@": True,  # roll
    ".": False,  # empty
}
UNREMOVABLE_THRESHOLD = 4


class Solver:
    def __init__(self, grid: np.ndarray):
        self.grid = np.pad(grid, 1)  # effectively makes a copy

    @property
    def n_rows(self) -> int:
        return self.grid.shape[0]

    @property
    def n_cols(self) -> int:
        return self.grid.shape[1]

    def count_neighbors(self, i: int, j: int) -> int:
        count = 0
        for i_shift in [-1, 0, 1]:
            i_new = i + i_shift
            for j_shift in [-1, 0, 1]:
                if i_shift == 0 and j_shift == 0:
                    continue  # don't look at the center
                j_new = j + j_shift
                if self.grid[i_new, j_new]:
                    count += 1
        return count

    def get_removables(self) -> set[tuple[int, int]]:
        removables: set[tuple[int, int]] = set()
        for i in range(1, self.n_rows - 1):
            for j in range(1, self.n_cols - 1):
                if not self.grid[i, j]:
                    continue
                n_neighbors = self.count_neighbors(i, j)
                if n_neighbors < UNREMOVABLE_THRESHOLD:
                    removables.add((i, j))
        return removables

    def iteratively_remove_all(self) -> set[tuple[int, int]]:
        removed: set[tuple[int, int]] = set()
        while True:
            new_removables = self.get_removables()
            if len(new_removables) == 0:
                return removed
            for loc in new_removables:
                self.grid[loc] = False
            removed.update(new_removables)


def main():
    with open(get_input_file_path(4), "r", encoding="utf-8") as f:
        grid = np.array([
            [
                SYMBOL_TO_BOOL[c]
                for c in line.strip()
            ]
            for line in f
        ])
    solver = Solver(grid)
    initially_removable = solver.get_removables()
    print(f"# initially removable: {len(initially_removable)}")
    ever_removable = solver.iteratively_remove_all()
    print(f"# ever removable: {len(ever_removable)}")


if __name__ == "__main__":
    main()
