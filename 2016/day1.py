"""
--- Day 1: No Time for a Taxicab ---

Santa's sleigh uses a very high-precision clock to guide its movements, and the clock's oscillator is regulated by stars. Unfortunately, the stars have been stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", unfortunately, is as close as you can get - the instructions on the Easter Bunny Recruiting Document the Elves intercepted start here, and nobody had time to work them out further.

The Document indicates that you should start at the given coordinates (where you just landed) and face North. Then, follow the provided sequence: either turn left (L) or right (R) 90 degrees, then walk forward the given number of blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you take a moment and work out the destination. Given that you can only walk on the street grid of the city, how far is the shortest path to the destination?

For example:

    Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
    R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
    R5, L5, R5, R3 leaves you 12 blocks away.

How many blocks away is Easter Bunny HQ?

--- Part Two ---

Then, you notice the instructions continue on the back of the Recruiting Document. Easter Bunny HQ is actually at the first location you visit twice.

For example, if your instructions are R8, R4, R4, R8, the first location you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?
"""

def parse_data(filename: str) -> list[tuple[str, int]]:
    """
    Parse the input data from the given filename

    Args:
        filename (str): The name of the file containing the input data

    Returns:
        list[tuple[str, int]]: A list of tuples containing the direction and distance
    """
    with open(filename, "r", encoding="utf-8") as file:
        data = file.read().strip().split(", ")
    return [(d[0], int(d[1:])) for d in data]

def get_distance(directions: list[tuple[str, int]]) -> int:
    """
    Calculate the distance from the starting point after following the given directions

    Args:
        directions (list[tuple[str, int]]): A list of tuples containing the direction and distance

    Returns:
        int: The distance from the starting point
    """
    x, y = 0, 0  # Starting coordinates
    for turn, steps in directions:
        if turn == "R":
            x, y = -y, x
        else:
            x, y = y, -x
        x += steps
    return abs(x) + abs(y)

def get_first_revisited_distance(directions: list[tuple[str, int]]) -> int:
    """
    Calculate the distance to the first location that is visited twice

    Args:
        directions (list[tuple[str, int]]): A list of tuples containing the direction and distance

    Returns:
        int: The distance to the first location that is visited twice
    """
    x, y = 0, 0  # Starting coordinates
    visited: set[tuple[int, int]] = set()
    visited.add((x, y))
    direction_index = 0  # Facing north
    direction_map = [
        (0, 1),  # North
        (1, 0),  # East
        (0, -1),  # South
        (-1, 0),  # West
    ]

    for turn, steps in directions:
        if turn == "R":
            direction_index = (direction_index + 1) % 4
        else:
            direction_index = (direction_index - 1) % 4
        dx, dy = direction_map[direction_index]

        for _ in range(steps):
            x += dx
            y += dy
            if (x, y) in visited:
                return abs(x) + abs(y)
            visited.add((x, y))
    return -1  # If no location is visited twice

def main():
    """
    Main function to execute the code
    """
    filename = "day1.txt"
    directions = parse_data(filename)

    print(f"Part 1: {get_distance(directions)}")
    print(f"Part 2: {get_first_revisited_distance(directions)}")

if __name__ == "__main__":
    main()
