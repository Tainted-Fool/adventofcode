"""
--- Day 6: Probably a Fire Hazard ---

Because your neighbors keep defeating you in the holiday house decorating contest year after year, you've decided to deploy one million lights in a 1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions include whether to turn on, turn off, or toggle various inclusive ranges given as coordinate pairs. Each coordinate pair represents opposite corners of a rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore refers to 9 lights in a 3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by doing the instructions Santa sent you in order.

For example:

    turn on 0,0 through 999,999 would turn on (or leave on) every light.
    toggle 0,0 through 999,0 would toggle the first line of 1000 lights, turning off the ones that were on, and turning on the ones that were off.
    turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights.

After following the instructions, how many lights are lit?

--- Part Two ---

You just finish implementing your winning light pattern when you realize you mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls; each light can have a brightness of zero or more. The lights all start at zero.

The phrase turn on actually means that you should increase the brightness of those lights by 1.

The phrase turn off actually means that you should decrease the brightness of those lights by 1, to a minimum of zero.

The phrase toggle actually means that you should increase the brightness of those lights by 2.

What is the total brightness of all lights combined after following Santa's instructions?

For example:

    turn on 0,0 through 0,0 would increase the total brightness by 1.
    toggle 0,0 through 999,999 would increase the total brightness by 2000000.

"""
import re
import numpy as np
from numpy.typing import NDArray

def parse_instruction(instruction: str) -> tuple[str, slice, slice]:
    """
    Parses a lighting instruction string into a command and coordinate slices

    Args:
        instruction (str): The instruction string to e.g. "turn on 0,0 through 999,999"

    Returns:
        tuple[str, slice, slice]: A tuple containing the command ("turn on", "turn off", "toggle") and two slices objects representing the x and y coordinate ranges
    """
    pattern = r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)"
    # pattern = r"([\w\s]+)\s(\d+),(\d+) through (\d+),(\d+)"
    match = re.match(pattern, instruction)
    if not match:
        raise ValueError(f"Invalid instruction: {instruction}")
    command, x0, y0, x1, y1 = match.groups()
    return command, slice(int(x0), int(x1) + 1), slice(int(y0), int(y1) + 1)

def apply_part1(grid: NDArray[np.bool], command: str, x_slice: slice, y_slice: slice) -> None:
    """
    Applies a light command to a boolean grid where each cell is either on or off

    Args:
        grid (NDArray[np.bool]): 2D array of boolean values representing the light grid
        command (str): The command to apply ('turn on', 'turn off', 'toggle')
        x_slice (slice): Slice object for row indexing
        y_slice (slice): Slice object for column indexing
    """
    # if command == 'turn on':
    #     grid[x_slice, y_slice] = True
    # elif command == 'turn off':
    #     grid[x_slice, y_slice] = False
    # elif command == 'toggle':
    #     grid[x_slice, y_slice] = ~grid[x_slice, y_slice]
    if command == "toggle":
        grid[x_slice, y_slice] = ~grid[x_slice, y_slice]
    else:
        value = command == "turn on"
        grid[x_slice, y_slice] = value

def apply_part2(grid: NDArray[np.integer], command: str, x_slice: slice, y_slice: slice) -> None:
    """
    Applies a light command to an integer grid where each cell can have a brightness level

    Args:
        grid (NDArray[np.integer]): 2D array of integer values representing the light grid brightness
        command (str): The command to apply ('turn on', 'turn off', 'toggle')
        x_slice (slice): Slice object for row indexing
        y_slice (slice): Slice object for column indexing
    """
    # if command == 'turn on':
    #     grid[x_slice, y_slice] += 1
    # elif command == 'turn off':
    #     grid[x_slice, y_slice] -= 1
    #     grid[grid < 0] = 0  # Clamp to 0
    # elif command == 'toggle':
    #     grid[x_slice, y_slice] += 2
    delta_map = {
        "turn on": 1,
        "turn off": -1,
        "toggle": 2
    }
    grid[x_slice, y_slice] += delta_map[command]
    # np.maximum(grid, 0, out=grid)  # Ensure no negative values remain
    grid[grid < 0] = 0  # Ensure no negative brightness values

def main():
    """
    Main function to read the input file, parse instructions, and apply them to the grids for both parts of the problem
    """
    filename = "day6.txt"

    grid_part1 = np.zeros((1000, 1000), dtype=bool)
    grid_part2 = np.zeros((1000, 1000), dtype=int)

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            command, x_slice, y_slice = parse_instruction(line)
            apply_part1(grid_part1, command, x_slice, y_slice)
            apply_part2(grid_part2, command, x_slice, y_slice)

    print(f"Part 1: {np.sum(grid_part1)}")
    print(f"Part 2: {np.sum(grid_part2)}")

if __name__ == "__main__":
    main()
