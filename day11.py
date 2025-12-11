from utils import get_input_file_path

START = "you"
END = "out"


class Solver:
    def __init__(self, graph: dict[str, set[str]]):
        super().__init__()
        self.graph = graph
        self._cache: dict[str, int] = {END: 1}

    def _dfs_count(self, path: list[str]) -> int:
        current = path[-1]
        try:
            return self._cache[current]
        except KeyError:
            pass
        total = 0
        for neighbor in self.graph[current]:
            if neighbor in path:
                print("CYCLE ALERT!!")
                continue
            total += self._dfs_count(path + [neighbor])
        self._cache[current] = total
        return total

    def count_paths_to_end(self) -> int:
        return self._dfs_count([START])


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
    solver = Solver(graph)
    n_paths_to_end = solver.count_paths_to_end()
    print(f"{n_paths_to_end = }")


if __name__ == "__main__":
    main()
