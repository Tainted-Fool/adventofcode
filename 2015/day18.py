"""
--- Day 18: Like a GIF For Your Yard ---

After the million lights incident, the fire code has gotten stricter: now, at most ten thousand lights are allowed. You arrange them in a 100x100 grid.

Never one to let you down, Santa again mails you instructions on the ideal lighting configuration. With so few lights, he says, you'll have to resort to animation.

Start by setting your lights to the included initial configuration (your puzzle input). A # means "on", and a . means "off".

Then, animate your grid in steps, where each step decides the next configuration based on the current one. Each light's next state (either on or off) depends on its current state and the current states of the eight lights adjacent to it (including diagonals). Lights on the edge of the grid might have fewer than eight neighbors; the missing ones always count as "off".

For example, in a simplified 6x6 grid, the light marked A has the neighbors numbered 1 through 8, and the light marked B, which is on an edge, only has the neighbors marked 1 through 5:

1B5...
234...
......
..123.
..8A4.
..765.

The state a light should have next is based on its current state (on or off) plus the number of neighbors that are on:

    A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.

All of the lights update simultaneously; they all consider the same current state before moving to the next.

Here's a few steps from an example configuration of another 6x6 grid:

Initial state:
.#.#.#
...##.
#....#
..#...
#.#..#
####..

After 1 step:
..##..
..##.#
...##.
......
#.....
#.##..

After 2 steps:
..###.
......
..###.
......
.#....
.#....

After 3 steps:
...#..
......
...#..
..##..
......
......

After 4 steps:
......
......
..##..
..##..
......
......

After 4 steps, this example has four lights on.

In your grid of 100x100 lights, given your initial configuration, how many lights are on after 100 steps?

--- Part Two ---

You flip the instructions over; Santa goes on to point out that this is all just an implementation of Conway's Game of Life. At least, it was, until you notice that something's wrong with the grid of lights you bought: four lights, one in each corner, are stuck on and can't be turned off. The example above will actually run like this:

Initial state:
##.#.#
...##.
#....#
..#...
#.#..#
####.#

After 1 step:
#.##.#
####.#
...##.
......
#...#.
#.####

After 2 steps:
#..#.#
#....#
.#.##.
...##.
.#..##
##.###

After 3 steps:
#...##
####.#
..##.#
......
##....
####.#

After 4 steps:
#.####
#....#
...#..
.##...
#.....
#.#..#

After 5 steps:
##.###
.##..#
.##...
.##...
#.#...
##...#

After 5 steps, this example now has 17 lights on.

In your grid of 100x100 lights, given your initial configuration, but with the four corners always in the on state, how many lights are on after 100 steps?
"""
from typing import cast
import numpy as np
from numpy.typing import NDArray

def parse_data(filename: str) -> list[list[int]]:
    """
    Reads the input file and converts it into a 2D list of integers

    Args:
        filename (str): The name of the input file

    Returns:
        list[list[int]]: A 2D list where each element is either 0 (off) or 1 (on)
    """
    grid: list[list[int]] = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            row: list[int] = []
            for char in line.strip():
                if char == "#":
                    row.append(1)
                else:
                    row.append(0)
            grid.append(row)
    return grid

def parse_data2(filename: str) -> list[list[int]]:
    """
    Reads the input file and converts it into a 2D list of integers

    Args:
        filename (str): The name of the input file

    Returns:
        list[list[int]]: A 2D list where each element is either 0 (off) or 1 (on)
    """
    convert = {"#": 1, ".": 0}
    with open(filename, "r", encoding="utf-8") as file:
        return [[convert[char] for char in line.strip()] for line in file]

def count_on_neighbours(grid: list[list[int]], row: int, col: int) -> int:
    """
    Return how many of the eight neighbours of a cell are on

    Args:
        grid (list[list[int]]): The 2D grid of lights
        row (int): The row index of the cell
        col (int): The column index of the cell

    Returns:
        int: The count of neighbours that are on (1)
    """
    rows = len(grid)
    cols = len(grid[0])
    total = 0

    for delta_row in (-1, 0, 1):
        for delta_col in (-1, 0, 1):
            if delta_row == 0 and delta_col == 0:
                continue

            new_row = row + delta_row
            new_col = col + delta_col

            if 0 <= new_row < rows and 0 <= new_col < cols:
                total += grid[new_row][new_col]
    return total

def next_grid_state(current: list[list[int]], pin_corners: bool = False) -> list[list[int]]:
    """
    Compute the grid state for the next step based on the current state

    Args:
        current (list[list[int]]): The current state of the grid
        pin_corners (bool): If True, the corners will always be on

    Returns:
        list[list[int]]: The next state of the grid
    """
    rows = len(current)
    cols = len(current[0])
    new_grid = [[0] * cols for _ in range(rows)]
    # new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            # Corners stay on if pin_corners is True
            if pin_corners and (i, j) in ((0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)):
                new_grid[i][j] = 1
                continue

            neighbours = count_on_neighbours(current, i, j)

            if current[i][j] == 1:
                # a lit cell stays on with 2 or 3 neighbours
                if neighbours in (2, 3):
                    new_grid[i][j] = 1
            else:
                # An unlit cell turns on with exactly 3 neighbours
                if neighbours == 3:
                    new_grid[i][j] = 1
    return new_grid

def run_simulation(start: list[list[int]], steps: int, pin_corners: bool = False) -> list[list[int]]:
    """
    Run the simulation for `steps` iterations and returns the final grid

    Args:
        start (list[list[int]]): The initial state of the grid
        steps (int): The number of steps to simulate
        pin_corners (bool): If True, the corners will always be on

    Returns:
        list[list[int]]: The final state of the grid after `steps` iterations
    """
    # Create a copy of the initial grid
    grid = [row[:] for row in start]

    # Turn on the corners before the first step if required
    if pin_corners:
        last_row = len(grid) - 1
        last_col = len(grid[0]) - 1
        grid[0][0] = grid[0][last_col] = grid[last_row][0] = grid[last_row][last_col] = 1

    for _ in range(steps):
        grid = next_grid_state(grid, pin_corners)

    return grid

def count_lights_on(grid: list[list[int]]) -> int:
    """
    Count how many lights are on in the grid

    Args:
        grid (list[list[int]]): The grid to count lights in

    Returns:
        int: The total number of lights that are on
    """
    total = 0
    for row in grid:
        for value in row:
            total += value
    return total
    # return sum(sum(row) for row in grid)

def numpy_count(grid: NDArray[np.uint8]) -> NDArray[np.uint8]:
    """
    Return an array with the number of on neighbours for each cell

    Args:
        grid (NDArray[np.uint8]): The current state of the grid as a numpy array

    Returns:
        NDArray[np.uint8]: A numpy array with the count of neighbours that are on
    """
    pad = np.pad(grid, 1)  # zero-padd all around
    return (
        pad[0:-2, 0:-2] + pad[0:-2, 1:-1] + pad[0:-2, 2:] +
        pad[1:-1, 0:-2] + pad[1:-1, 2:] +
        pad[2:, 0:-2] + pad[2:, 1:-1] + pad[2:, 2:]
    )

def numpy_step(grid: NDArray[np.uint8], pin_corners: bool = False) -> NDArray[np.uint8]:
    """
    Perform a single step of the simulation using numpy

    Args:
        grid (NDArray[np.uint8]): The current state of the grid as a numpy array
        pin_corners (bool): If True, the corners will always be on

    Returns:
        NDArray[np.uint8]: The next state of the grid after applying the rules
    """
    n = numpy_count(grid)
    stay_on = cast(NDArray[np.bool], (grid == 1) & ((n == 2) | (n == 3)))
    turn_on = cast(NDArray[np.bool], (grid == 0) & (n == 3))
    next_grid = (stay_on | turn_on).astype(np.uint8)

    if pin_corners:
        rows, cols = next_grid.shape
        next_grid[0, 0] = next_grid[0, cols - 1] = 1
        next_grid[rows - 1, 0] = next_grid[rows - 1, cols - 1] = 1
    return next_grid

def numpy_run(filename: str, steps: int) -> tuple[int, int]:
    """
    Run the simulation using numpy for `steps` iterations and returns the count of lights on

    Args:
        filename (str): The name of the input file
        steps (int): The number of steps to simulate

    Returns:
        int: The total number of lights that are on after `steps` iterations
    """
    # grid = np.array([[c == "#" for c in line.strip()] for line in open(filename, "r", encoding="utf-8")], np.uint8)
    bool_grid: list[list[bool]] = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            bool_row = [c == "#" for c in line]
            bool_grid.append(bool_row)
    grid = np.array(bool_grid, dtype=np.uint8)

    grid1 = grid.copy()
    grid2 = grid.copy()
    grid2[0, 0] = grid2[0, -1] = grid2[-1, 0] = grid2[-1, -1] = 1

    for _ in range(steps):
        grid1 = numpy_step(grid1)
        grid2 = numpy_step(grid2, True)

    return grid1.sum(), grid2.sum()

def main():
    """
    Main function to read the input file, parse instructions, and apply them to the grids for both parts of the problem
    """
    filename = "day18.txt"
    # initial_grid = parse_data(filename)
    # initial_grid = parse_data2(filename)
    steps_to_run = 100

    # print(f"Part 1: {count_lights_on(run_simulation(initial_grid, steps_to_run))}")
    # print(f"Part 2: {count_lights_on(run_simulation(initial_grid, steps_to_run, True))}")

    print(f"Part 1 (numpy): {numpy_run(filename, steps_to_run)[0]}")
    print(f"Part 2 (numpy): {numpy_run(filename, steps_to_run)[1]}")

if __name__ == "__main__":
    main()
