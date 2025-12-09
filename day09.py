import math

from utils import get_input_file_path, Loc


def get_area(tile_a: Loc, tile_b: Loc) -> int:
    return math.prod(
        abs(dim_a - dim_b) + 1
        for dim_a, dim_b in zip(tile_a, tile_b)
    )


def main():
    tiles: list[Loc] = []
    with open(get_input_file_path(9), "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            x, y = map(int, line.split(","))
            tiles.append((x, y))

    biggest_area: int | None = None
    n = len(tiles)
    for i in range(n - 1):
        tile_i = tiles[i]
        for j in range(i + 1, n):
            tile_j = tiles[j]
            area = get_area(tile_i, tile_j)
            if biggest_area is None or area > biggest_area:
                biggest_area = area
    if biggest_area is None:
        raise ValueError("Failed to find a any area values")
    print(f"{biggest_area = }")


if __name__ == "__main__":
    main()
