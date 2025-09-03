"""
--- Day 1: Not Quite Lisp ---

Santa was hoping for a white Christmas, but his weather machine's "snow" function is powered by stars, and he's fresh out! To save Christmas, he needs you to collect fifty stars by December 25th.

Collect stars by helping Santa solve puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Here's an easy puzzle to warm you up.

Santa is trying to deliver presents in a large apartment building, but he can't find the right floor - the directions he got are a little confusing. He starts on the ground floor (floor 0) and then follows the instructions one character at a time.

An opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ), means he should go down one floor.
The apartment building is very tall, and the basement is very deep; he will never find the top or bottom floors.

For example:

    (()) and ()() both result in floor 0.
    ((( and (()(()( both result in floor 3.
    ))((((( also results in floor 3.
    ()) and ))( both result in floor -1 (the first basement level).
    ))) and )())()) both result in floor -3.

To what floor do the instructions take Santa?

--- Part Two ---

Now, given the same instructions, find the position of the first character that causes him to enter the basement (floor -1). The first character in the instructions has position 1, the second character has position 2, and so on.

For example:

    ) causes him to enter the basement at character position 1.
    ()()) causes him to enter the basement at character position 5.

What is the position of the character that causes Santa to first enter the basement?
"""
from collections.abc import Generator

def read_char(filepath: str) -> Generator[str, None, None]:
    """
    Read a file character by character

    Args:
        filepath (str): The filepath to read characters from

    Returns:
        Generator[str, None, None]: A generator yielding each character in the file
    """
    with open(filepath, "r", encoding="utf-8") as file:
        while char := file.read(1):
            yield char

def calculate_floor_and_basement(directions: str) -> tuple[int, int | None]:
    """
    Calculate the final floor and the position of the first basement entry

    Args:
        directions (str): A string of parentheses `(` or `)` representing the directions

    Returns:
        tuple[int, int | None]: A tuple containing the final floor and the position of the first basement entry
    """
    floor, basement_position = 0, None
    for position, char in enumerate(directions, start=1):
        floor += 1 if char == "(" else -1
        if floor == -1 and basement_position is None:
            basement_position = position

    return floor, basement_position

def main():
    """
    Main function to read input and calculate results for Day 1 of Advent of Code 2015
    """
    filename = "day1.txt"

    with open(filename, "r", encoding="utf-8") as file:
        directions = file.read().strip()

    final_floor, basement_position = calculate_floor_and_basement(directions)
    print(f"Part 1: {final_floor}")
    print(f"Part 2: {basement_position}")

if __name__ == "__main__":
    main()
