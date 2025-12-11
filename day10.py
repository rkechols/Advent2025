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
        button_wirings: list[set[int]],
        joltages: Sequence[int],
    ):
        n = len(lights)
        self.target_lights = np.array(lights)
        if not all(0 <= i < n for button_wiring in button_wirings for i in button_wiring):
            raise ValueError("Button wiring value out of range")
        self.buttons = [
            np.array([i in button_wiring for i in range(n)])
            for button_wiring in button_wirings
        ]  # fmt: skip
        if len(joltages) != n:
            raise ValueError("Differing number of joltages and lights")
        self.target_joltages = np.array(joltages)

    @property
    def n(self) -> int:
        return len(self.target_lights)

    def lights_match(self, lights: np.ndarray) -> bool:
        lights_bools = (lights % 2).astype(bool)
        return np.array_equal(self.target_lights, lights_bools)

    def min_presses_to_match_lights(self) -> int:
        # find lights only connected to 1 button
        target_light_indices = {i for i, light in enumerate(self.target_lights) if light}
        needed_buttons: set[int] = set()
        for target_light in target_light_indices:
            connected_buttons = {
                button_i
                for button_i, button in enumerate(self.buttons)
                if button[target_light]
            }  # fmt: skip
            if len(connected_buttons) == 1:
                needed_buttons.add(next(iter(connected_buttons)))

        lights = np.zeros(self.n, dtype=int)
        for needed_button_i in needed_buttons:
            lights += self.buttons[needed_button_i]
        if self.lights_match(lights):
            return len(needed_buttons)

        buttons_unknown = [i for i in range(len(self.buttons)) if i not in needed_buttons]
        n_buttons_unknown = len(buttons_unknown)
        for n_chosen in range(1, n_buttons_unknown + 1):
            for chosen_buttons in itertools.combinations(buttons_unknown, r=n_chosen):
                result = lights + sum(
                    self.buttons[button_i]
                    for button_i in chosen_buttons
                )  # fmt: skip
                if self.lights_match(result):
                    return len(needed_buttons) + n_chosen
        raise ValueError("Could not find button config to match lights")

    def get_unsolved_joltages(self, joltages: np.ndarray) -> set[int]:
        return {
            i
            for i, is_match in enumerate(joltages == self.target_joltages)
            if is_match
        }  # fmt: skip

    def joltages_match(self, joltages: np.ndarray) -> bool:
        return np.array_equal(self.target_joltages, joltages)

    def min_presses_to_match_joltages(self) -> int:
        joltages = np.zeros(self.n, dtype=int)

        needed_buttons: dict[int, int] = {}
        while True:
            # find unsolved joltages only connected to 1 unknown button
            found_needed_button = False
            joltage_diffs = self.target_joltages - joltages
            for joltage_diff_i, joltage_diff in enumerate(joltage_diffs):
                joltage_diff = int(joltage_diff)
                if joltage_diff == 0:
                    continue
                connected_buttons = {
                    button_i
                    for button_i, button in enumerate(self.buttons)
                    if button[joltage_diff_i]
                }  # fmt: skip
                if len(connected_buttons) == 1:
                    found_needed_button = True
                    needed_button_i = next(iter(connected_buttons))
                    if needed_button_i in needed_buttons:
                        raise ValueError("Oops! Should've added instead of overwriting")
                    needed_buttons[needed_button_i] = joltage_diff
                    joltages += joltage_diff * self.buttons[needed_button_i]
                    break
            if not found_needed_button:
                break

        if self.joltages_match(joltages):
            return sum(needed_buttons.values())

        buttons_unknown = [i for i in range(len(self.buttons)) if i not in needed_buttons]
        if len(buttons_unknown) == 0:
            raise ValueError("All buttons known, but joltages still don't match?")

        return 0
        n_buttons_unknown = len(buttons_unknown)
        for n_chosen in range(1, n_buttons_unknown + 1):
            for chosen_buttons in itertools.combinations(buttons_unknown, r=n_chosen):
                result = lights + sum(
                    self.buttons[button]
                    for button in chosen_buttons
                )  # fmt: skip
                if self.lights_match(result):
                    return len(needed_buttons) + n_chosen
        raise ValueError("Could not find a matching button config")


def main():
    min_presses_to_match_lights = 0
    min_presses_to_match_joltages = 0
    with open(get_input_file_path(10), "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                match = re.fullmatch(r"\[([.#]+)] (.*) \{([\d,]+)}", line.strip())
                if not match:
                    raise ValueError("Failed to parse line with regex")
                lights_str, wiring, joltage = match.groups()
                lights = [LIGHT_VALUES[c] for c in lights_str]
                button_wirings = [
                    set(map(int, button_str.strip("()").split(",")))
                    for button_str in wiring.split(" ")
                ]  # fmt: skip
                joltages = list(map(int, joltage.strip("{}").split(",")))
                machine = Machine(lights, button_wirings, joltages)
                min_presses_to_match_lights += machine.min_presses_to_match_lights()
                min_presses_to_match_joltages += machine.min_presses_to_match_joltages()
            except Exception:
                print(f"ERROR on input file line {line_number}")
                raise
    print(f"{min_presses_to_match_lights = }")
    print(f"{min_presses_to_match_joltages = }")


if __name__ == "__main__":
    main()
