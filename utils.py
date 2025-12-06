from collections.abc import Generator
from pathlib import Path
from typing import Iterable

import numpy as np

INPUTS_DIR = Path(__file__).parent / "inputs"


def get_input_file_path(day_number: int) -> Path:
    return INPUTS_DIR / f"day{day_number:02d}.txt"


def product(values: Iterable[int]) -> int:
    prod = 1
    for value in values:
        prod *= value
    return prod


Loc = tuple[int, int]


class GridSolver:
    def __init__(self, grid: np.ndarray):
        super().__init__()
        if len(grid.shape) != 2:
            raise ValueError(f"Grid must be 2-dimensional, but shape was {grid.shape}")
        self.grid = grid

    @property
    def n_rows(self) -> int:
        return self.grid.shape[0]

    @property
    def n_cols(self) -> int:
        return self.grid.shape[1]

    def row_in_bounds(self, i: int) -> bool:
        return 0 <= i < self.n_rows

    def col_in_bounds(self, j: int) -> bool:
        return 0 <= j < self.n_cols

    def loc_in_bounds(self, i: int, j: int) -> bool:
        return self.row_in_bounds(i) and self.col_in_bounds(j)

    def iter_4_neighbors(self, i: int, j: int) -> Generator[Loc]:
        for i_shift, j_shift in [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
        ]:
            i_new = i + i_shift
            j_new = j + j_shift
            if self.loc_in_bounds(i_new, j_new):
                yield i_new, j_new

    def iter_8_neighbors(self, i: int, j: int) -> Generator[Loc]:
        for i_shift in [-1, 0, 1]:
            i_new = i + i_shift
            if not self.row_in_bounds(i_new):
                continue
            for j_shift in [-1, 0, 1]:
                if i_shift == 0 and j_shift == 0:
                    continue  # skip the center
                j_new = j + j_shift
                if self.col_in_bounds(j_new):
                    yield i_new, j_new
