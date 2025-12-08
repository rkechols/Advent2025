import math
from collections import defaultdict
from typing import cast

from utils import get_input_file_path

Loc3 = tuple[int, int, int]


N_CONNECTIONS = 1000
N_LARGEST_TO_COUNT = 3


def distance(loc_a: Loc3, loc_b: Loc3) -> float:
    return math.sqrt(sum(
        (coord_a - coord_b) ** 2
        for coord_a, coord_b in zip(loc_a, loc_b)
    ))


def main():
    with open(get_input_file_path(8), "r", encoding="utf-8") as f:
        locs = [
            cast(Loc3, tuple(map(int, line.strip().split(","))))
            for line in f
        ]
    if len({len(loc) for loc in locs}) != 1:
        raise ValueError("inconsistent lengths")

    # calculate pairwise distances
    n = len(locs)
    distances: list[tuple[Loc3, Loc3, float]] = []
    for i in range(n - 1):
        loc_a = locs[i]
        for j in range(i + 1, n):
            loc_b = locs[j]
            d = distance(loc_a, loc_b)
            distances.append((loc_a, loc_b, d))
    distances.sort(key=lambda tup: tup[-1])  # closes to furthest

    # join closest locs
    circuits: dict[str, set[Loc3]] = defaultdict(set)
    circuit_memberships: dict[Loc3, str] = {}
    next_circuit_id = 0
    for loc_a, loc_b, d in distances[:N_CONNECTIONS]:
        circuit_a = circuit_memberships.get(loc_a)
        circuit_b = circuit_memberships.get(loc_b)
        if circuit_a is None:
            if circuit_b is None:  # both alone
                new_circuit_id = str(next_circuit_id)
                next_circuit_id += 1
                circuits[new_circuit_id].add(loc_a)
                circuits[new_circuit_id].add(loc_b)
                circuit_memberships[loc_a] = new_circuit_id
                circuit_memberships[loc_b] = new_circuit_id
            else:  # a joins b
                circuits[circuit_b].add(loc_a)
                circuit_memberships[loc_a] = circuit_b
        else:
            if circuit_b is None:  # b joins a
                circuits[circuit_a].add(loc_b)
                circuit_memberships[loc_b] = circuit_a
            else:  # the two fully join
                if circuit_a == circuit_b:
                    pass  # JK, they're already in the same circuit
                else:
                    # arbitrarily move circuit b into circuit a
                    circuit_b_members = circuits.pop(circuit_b)
                    circuits[circuit_a].update(circuit_b_members)
                    for circuit_b_member in circuit_b_members:
                        circuit_memberships[circuit_b_member] = circuit_a

    # multiply the 3 largest circuit sizes
    circuit_sizes = sorted((len(members) for members in circuits.values()), reverse=True)
    if (n_singletons_to_count := N_LARGEST_TO_COUNT - len(circuit_sizes)) > 0:
        circuit_sizes.extend(1 for _ in range(n_singletons_to_count))
    product_of_largest_sizes = math.prod(circuit_sizes[:N_LARGEST_TO_COUNT])
    print(f"{product_of_largest_sizes = }")



if __name__ == "__main__":
    main()
