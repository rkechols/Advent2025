import numpy as np

from utils import GridSolver, Loc, get_input_file_path

SYMBOL_TO_BOOL = {
    "@": True,  # roll
    ".": False,  # empty
}
UNREMOVABLE_THRESHOLD = 4


class Solver(GridSolver):
    def count_neighbors(self, i: int, j: int) -> int:
        count = 0
        for loc in self.iter_8_neighbors(i, j):
            if self.grid[loc]:
                count += 1
        return count

    def get_removables(self) -> set[Loc]:
        removables: set[Loc] = set()
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if not self.grid[i, j]:
                    continue
                n_neighbors = self.count_neighbors(i, j)
                if n_neighbors < UNREMOVABLE_THRESHOLD:
                    removables.add((i, j))
        return removables

    def iteratively_remove_all(self) -> set[Loc]:
        removed: set[Loc] = set()
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
            [SYMBOL_TO_BOOL[c] for c in line.strip()]
            for line in f
        ])  # fmt: skip
    solver = Solver(grid)
    initially_removable = solver.get_removables()
    print(f"# initially removable: {len(initially_removable)}")
    ever_removable = solver.iteratively_remove_all()
    print(f"# ever removable: {len(ever_removable)}")


if __name__ == "__main__":
    main()
