import re

from utils import get_input_file_path

DIAL_START_POSITION = 50
DIAL_SIZE = 100

RE_DIAL_TURN = re.compile(r"([LR])(\d+)")
DIRECTION_TO_SIGN = {
    "L": -1,
    "R": 1,
}


def main():
    dial = DIAL_START_POSITION
    count_dial_stops_on_zero = 0  # part 1
    count_dial_hits_zero = 0  # part 2
    with open(get_input_file_path(1), "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                turn_direction, turn_count = RE_DIAL_TURN.fullmatch(line.strip()).groups()
                turn_count = int(turn_count)
                if turn_count == 0:
                    raise ValueError("Unexpected turn_count value of 0")
                turn_count *= DIRECTION_TO_SIGN[turn_direction]
                dial_before = dial
                dial += turn_count
                if not (0 < dial < DIAL_SIZE):
                    if dial >= DIAL_SIZE:
                        count_add = dial // DIAL_SIZE
                    elif dial == 0:
                        count_add = 1
                    else:  # dial < 0
                        count_add = abs(dial // DIAL_SIZE)
                        if dial_before == 0:
                            count_add -= 1
                        if dial % DIAL_SIZE == 0:
                            count_add += 1
                    count_dial_hits_zero += count_add
                dial %= DIAL_SIZE
                if dial == 0:
                    count_dial_stops_on_zero += 1
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise
    print(f"{count_dial_stops_on_zero = }")
    print(f"{count_dial_hits_zero = }")


if __name__ == "__main__":
    main()
