import dataclasses
import itertools
import math
from functools import cache

from utils import Loc, get_input_file_path


@cache
def get_area(tile_a: Loc, tile_b: Loc) -> int:
    return math.prod(
        abs(dim_a - dim_b) + 1
        for dim_a, dim_b in zip(tile_a, tile_b)
    )  # fmt: skip


@dataclasses.dataclass
class LineSegmentX:
    x_start: int
    x_stop: int
    y: int

    def __post_init__(self):
        self.x_start, self.x_stop = sorted((self.x_start, self.x_stop))


@dataclasses.dataclass
class LineSegmentY:
    y_start: int
    y_stop: int
    x: int

    def __post_init__(self):
        self.y_start, self.y_stop = sorted((self.y_start, self.y_stop))


def main():
    tiles: list[Loc] = []
    with open(get_input_file_path(9), "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            x, y = map(int, line.split(","))
            tiles.append((x, y))

    n = len(tiles)
    boxes = [
        (tiles[i], tiles[j])
        for i in range(n - 1)
        for j in range(i + 1, n)
    ]  # fmt: skip
    boxes.sort(key=lambda box: get_area(*box), reverse=True)

    biggest_area_at_all = get_area(*boxes[0])
    print(f"Part 1: {biggest_area_at_all = }")

    x_line_segments: list[LineSegmentX] = []
    y_line_segments: list[LineSegmentY] = []
    for tile_a, tile_b in itertools.pairwise([*tiles, tiles[0]]):
        if tile_a == tile_b:
            raise ValueError("no movement?")
        if tile_a[0] == tile_b[0]:  # same x; moving in y
            line_segment = LineSegmentY(y_start=tile_a[1], y_stop=tile_b[1], x=tile_a[0])
            y_line_segments.append(line_segment)
        elif tile_a[1] == tile_b[1]:  # same y; moving in x
            line_segment = LineSegmentX(x_start=tile_a[0], x_stop=tile_b[0], y=tile_a[1])
            x_line_segments.append(line_segment)
        else:
            raise ValueError(f"Failed to find common dimension on sequential tiles: {tile_a} / {tile_b}")
    x_line_segments.sort(key=lambda seg: seg.y)
    y_line_segments.sort(key=lambda seg: seg.x)

    for tile_a, tile_b in boxes:  # biggest to smallest
        min_x, max_x = min(tile_a[0], tile_b[0]), max(tile_a[0], tile_b[0])
        min_y, max_y = min(tile_a[1], tile_b[1]), max(tile_a[1], tile_b[1])

        if any(
            (min_y < seg.y < max_y) and not (seg.x_stop <= min_x or max_x <= seg.x_start)
            for seg in x_line_segments
        ):  # fmt: skip
            continue

        if any(
            (min_x < seg.x < max_x) and not (seg.y_stop <= min_y or max_y <= seg.y_start)
            for seg in y_line_segments
        ):  # fmt: skip
            continue

        biggest_area_filled = get_area(tile_a, tile_b)
        print(f"Part 2: {biggest_area_filled = }")
        break
    else:
        raise ValueError("Failed to find any fully bounded box")


if __name__ == "__main__":
    main()
