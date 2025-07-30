"""
--- Day 3: Perfectly Spherical Houses in a Vacuum ---

Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and then an elf at the North Pole calls him via radio and tells him where to move next. Moves are always exactly one house to the north (^), south (v), east (>), or west (<). After each move, he delivers another present to the house at his new location.

For example:

    > delivers presents to 2 houses: one at the starting location, and one to the east.
    ^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.
    ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.

However, the elf back at the north pole has had a little too much eggnog, and so his directions are a little off, and Santa ends up visiting some houses more than once. How many houses receive at least one present?

--- Part Two ---

The next year, to speed up the process, Santa creates a robot version of himself, Robo-Santa, to deliver presents with him.
Santa and Robo-Santa start at the same location (delivering two presents to the same starting house), then take turns moving based on instructions from the elf, who is eggnoggedly reading from the same script as the previous year.

For example:

    ^v delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south.
    ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started.
    ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other.

This year, how many houses receive at least one present?
"""

def count_houses(directions: str, number_deliverers: int = 1) -> int:
    """
    Calculate the number of unique houses visited by Santa and optional Robo-Santa

    Args:
        directions (str): A string of directions consisting of characters `^`, `v`, `>`, `<`
        number_deliverers (int): The number of deliverers (1 for Santa, 2 for Santa and Robo-Santa)

    Returns:
        int: The number of unique houses that received at least one present
    """
    positions = [(0, 0)] * number_deliverers
    visited_houses = {(0, 0)}
    direction_map = {
        "^": (0, 1),
        "v": (0, -1),
        ">": (1, 0),
        "<": (-1, 0)
    }

    for i, direction in enumerate(directions):
        mover = i % number_deliverers
        x, y = direction_map.get(direction, (0, 0))
        positions[mover] = (positions[mover][0] + x, positions[mover][1] + y)
        visited_houses.add(positions[mover])
    return len(visited_houses)

def main():
    filename = "day3.txt"

    with open(filename, "r") as file:
        directions = file.read()

    unique_houses = count_houses(directions)
    print(f"Part 1: {unique_houses}")

    unique_houses = count_houses(directions, 2)
    print(f"Part 2: {unique_houses}")

if __name__ == "__main__":
    main()
