import itertools
import math

from utils import get_input_file_path

START = "you"
END = "out"


class Solver:
    def __init__(self, graph: dict[str, set[str]], *, start: str, end: str):
        super().__init__()
        self.graph = graph
        self._start = start
        self._cache: dict[str, int] = {end: 1}

    def _dfs_count(self, path: list[str]) -> int:
        current = path[-1]
        try:
            return self._cache[current]
        except KeyError:
            pass
        total = 0
        for neighbor in self.graph.get(current, []):
            if neighbor in path:
                raise RuntimeError("CYCLE ALERT!!")
            total += self._dfs_count([*path, neighbor])
        self._cache[current] = total
        return total

    def count_paths_to_end(self) -> int:
        return self._dfs_count([self._start])


def main():
    graph: dict[str, set[str]] = {}
    with open(get_input_file_path(11), "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                in_, outs_str = line.strip().split(":")
                outs = outs_str.strip().split()
                graph[in_] = set(outs)
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise

    n_paths = Solver(graph, start="you", end="out").count_paths_to_end()
    print(f"Part 1: {n_paths = }")

    # part 2
    n_paths = sum(
        math.prod(
            Solver(graph, start=a, end=b).count_paths_to_end()
            for a, b in itertools.pairwise(net_path)
        )
        for net_path in [
            ["svr", "dac", "fft", "out"],
            ["svr", "fft", "dac", "out"],
        ]
    )  # fmt: skip
    print(f"Part 2: {n_paths = }")


if __name__ == "__main__":
    main()
