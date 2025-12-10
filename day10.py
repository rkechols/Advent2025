import itertools
import re
from collections.abc import Sequence

import numpy as np

from utils import get_input_file_path

LIGHT_VALUES = {
    ".": False,
    "#": True,
}


class Machine:
    def __init__(
        self,
        lights: Sequence[bool],
        buttons: list[set[int]],
        joltages: tuple[int, ...],
    ):
        n = len(lights)
        self.target_lights = np.array(lights)
        if not all(0 <= i < n for button in buttons for i in button):
            raise ValueError("Button wiring value out of range")
        self.buttons = [
            np.array([i in button for i in range(n)])
            for button in buttons
        ]
        if len(joltages) != n:
            raise ValueError("Differing number of joltages and lights")
        self.joltages = joltages

    @property
    def n(self) -> int:
        return len(self.joltages)

    def lights_match(self, lights: np.ndarray) -> bool:
        lights_bools = (lights % 2).astype(bool)
        return np.array_equal(self.target_lights, lights_bools)

    def min_presses_to_match_lights(self) -> int:
        # find lights only connected to 1 button
        target_light_indices = {i for i, light in enumerate(self.target_lights) if light}
        needed_buttons: set[int] = set()
        for target_light in target_light_indices:
            connected_buttons = {
                i
                for i, button in enumerate(self.buttons)
                if button[target_light]
            }
            if len(connected_buttons) == 1:
                needed_buttons.add(next(iter(connected_buttons)))

        lights = np.zeros(self.n, dtype=int)
        for needed_button in needed_buttons:
            lights += self.buttons[needed_button]
        if self.lights_match(lights):
            return len(needed_buttons)

        buttons_unknown = [i for i in range(len(self.buttons)) if i not in needed_buttons]
        n_buttons_unknown = len(buttons_unknown)
        for n_chosen in range(1, n_buttons_unknown + 1):
            for chosen_buttons in itertools.combinations(buttons_unknown, r=n_chosen):
                result = lights + sum(
                    self.buttons[button]
                    for button in chosen_buttons
                )
                if self.lights_match(result):
                    return len(needed_buttons) + n_chosen
        raise ValueError(f"Could not find a matching button config")


def main():
    min_presses_to_match_lights = 0
    with open(get_input_file_path(10), "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                match = re.fullmatch(r"\[([.#]+)] (.*) \{([\d,]+)}", line.strip())
                if not match:
                    raise ValueError("Failed to parse line with regex")
                lights_str, wiring, joltage = match.groups()
                lights = tuple(LIGHT_VALUES[c] for c in lights_str)
                buttons = [
                    set(map(int, button_str.strip("()").split(",")))
                    for button_str in wiring.split(" ")
                ]
                joltages = tuple(map(int, joltage.strip("{}").split(",")))
                machine = Machine(lights, buttons, joltages)
                min_presses_to_match_lights += machine.min_presses_to_match_lights()
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise
    print(f"{min_presses_to_match_lights = }")
    # 403 is TOO LOW


if __name__ == "__main__":
    main()
