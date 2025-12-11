import math
from collections import defaultdict
from typing import cast

from utils import get_input_file_path

Box = tuple[int, int, int]


N_CONNECTIONS_PART_1 = 1000
N_LARGEST_TO_COUNT = 3


def calculate_distance(box_a: Box, box_b: Box) -> float:
    return math.sqrt(sum(
        (coord_a - coord_b) ** 2
        for coord_a, coord_b in zip(box_a, box_b)
    ))  # fmt: skip


class Solver:
    def __init__(self, boxes: list[Box]):
        self._boxes = boxes
        # calculate pairwise distances
        n = len(boxes)
        distances: list[tuple[Box, Box, float]] = []
        for i in range(n - 1):
            box_a = boxes[i]
            for j in range(i + 1, n):
                box_b = boxes[j]
                distance = calculate_distance(box_a, box_b)
                distances.append((box_a, box_b, distance))
        distances.sort(key=lambda tup: tup[-1])  # closes to furthest
        self._distances = distances
        # keep track of what things are joined
        self._circuits: dict[str, set[Box]] = defaultdict(set)
        self._circuit_memberships: dict[Box, str] = {}
        self._next_to_join = 0

    def add_next_connection(self) -> tuple[Box, Box, float]:
        i = self._next_to_join
        try:
            tup = self._distances[i]
        except IndexError as e:
            raise RuntimeError("No more things to join!") from e
        box_a, box_b, _distance = tup
        self._next_to_join += 1
        circuit_a = self._circuit_memberships.get(box_a)
        circuit_b = self._circuit_memberships.get(box_b)
        if circuit_a is None:
            if circuit_b is None:  # both alone
                new_circuit_id = str(i)
                self._circuits[new_circuit_id].add(box_a)
                self._circuits[new_circuit_id].add(box_b)
                self._circuit_memberships[box_a] = new_circuit_id
                self._circuit_memberships[box_b] = new_circuit_id
            else:  # a joins b
                self._circuits[circuit_b].add(box_a)
                self._circuit_memberships[box_a] = circuit_b
        else:  # noqa: PLR5501
            if circuit_b is None:  # b joins a
                self._circuits[circuit_a].add(box_b)
                self._circuit_memberships[box_b] = circuit_a
            else:  # noqa: PLR5501  # the two fully join
                if circuit_a == circuit_b:
                    pass  # JK, they're already in the same circuit
                else:
                    # arbitrarily move circuit b into circuit a
                    circuit_b_members = self._circuits.pop(circuit_b)
                    self._circuits[circuit_a].update(circuit_b_members)
                    for circuit_b_member in circuit_b_members:
                        self._circuit_memberships[circuit_b_member] = circuit_a
        return tup

    @property
    def n_singleton_circuits(self) -> int:
        return len(self._boxes) - len(self._circuit_memberships)

    @property
    def n_circuits(self) -> int:
        return len(self._circuits) + self.n_singleton_circuits

    def sorted_circuit_sizes(self) -> list[int]:
        circuit_sizes = sorted((len(members) for members in self._circuits.values()), reverse=True)
        circuit_sizes.extend(1 for _ in range(self.n_singleton_circuits))
        return circuit_sizes

    def is_fully_connected(self) -> bool:
        return self.n_circuits == 1


def main():
    with open(get_input_file_path(8), "r", encoding="utf-8") as f:
        boxes = [
            tuple(map(int, line.strip().split(",")))
            for line in f
        ]  # fmt: skip
    if any(len(box) != 3 for box in boxes):
        raise ValueError("Expected all box locations to be 3-dimensional")
    solver = Solver(cast(list[Box], boxes))

    # part 1
    for _ in range(N_CONNECTIONS_PART_1):
        solver.add_next_connection()
    circuit_sizes = solver.sorted_circuit_sizes()
    product_of_largest_sizes = math.prod(circuit_sizes[:N_LARGEST_TO_COUNT])
    print(f"Part 1: {product_of_largest_sizes = }")

    if solver.is_fully_connected():
        raise ValueError("Unexpectedly already fully connected before starting part 2")

    # part 2
    while True:
        box_a, box_b, _ = solver.add_next_connection()
        if solver.is_fully_connected():
            product_of_last_x_coords = box_a[0] * box_b[0]
            print(f"Part 2: {product_of_last_x_coords = }")
            break


if __name__ == "__main__":
    main()
