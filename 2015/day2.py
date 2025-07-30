"""
--- Day 2: I Was Told There Would Be No Math ---

The elves are running low on wrapping paper, and so they need to submit an order for more. They have a list of the dimensions (length l, width w, and height h) of each present, and only want to order exactly as much as they need.

Fortunately, every present is a box (a perfect right rectangular prism), which makes calculating the required wrapping paper for each gift a little easier: find the surface area of the box, which is 2*l*w + 2*w*h + 2*h*l. The elves also need a little extra paper for each present: the area of the smallest side.

For example:

    A present with dimensions 2x3x4 requires 2*6 + 2*12 + 2*8 = 52 square feet of wrapping paper plus 6 square feet of slack, for a total of 58 square feet.
    A present with dimensions 1x1x10 requires 2*1 + 2*10 + 2*10 = 42 square feet of wrapping paper plus 1 square foot of slack, for a total of 43 square feet.

All numbers in the elves' list are in feet. How many total square feet of wrapping paper should they order?

--- Part Two ---

The elves are also running low on ribbon. Ribbon is all the same width, so they only have to worry about the length they need to order, which they would again like to be exact.

The ribbon required to wrap a present is the shortest distance around its sides, or the smallest perimeter of any one face. Each present also requires a bow made out of ribbon as well; the feet of ribbon required for the perfect bow is equal to the cubic feet of volume of the present. Don't ask how they tie the bow, though; they'll never tell.

For example:

    A present with dimensions 2x3x4 requires 2+2+3+3 = 10 feet of ribbon to wrap the present plus 2*3*4 = 24 feet of ribbon for the bow, for a total of 34 feet.
    A present with dimensions 1x1x10 requires 1+1+1+1 = 4 feet of ribbon to wrap the present plus 1*1*10 = 10 feet of ribbon for the bow, for a total of 14 feet.

How many total feet of ribbon should they order?
"""
from typing import List, Tuple

def get_dimensions(filepath: str) -> List[Tuple[int, int, int]]:
    """
    Read and parse dimensions from a file

    Args:
        filepath (str): The filepath to read dimensions from

    Returns:
        List[Tuple[int, int, int]]: A list of tuples containing the dimensions (length, width, height) of each present
    """
    with open(filepath, "r") as file:
        return [tuple(map(int, line.strip().split("x"))) for line in file]

def calculate_wrapping_paper(dimensions: Tuple[int, int, int]) -> int:
    """
    Calculate the wrapping paper needed for a single present
    Formula:
        - Surface Area = 2lw + 2wh + 2hl
        - Slack = area of the smallest side

    Args:
        dimensions (Tuple[int, int, int]): A tuple containing the dimensions (length, width, height) of the present

    Returns:
        int: The total square feet of wrapping paper needed for the present
    """
    length, width, height = dimensions
    sides = [length * width, width * height, height * length]
    return 2 * sum(sides) + min(sides)

def calculate_ribbon(dimensions: Tuple[int, int, int]) -> int:
    """
    Calculate the ribbon needed for a single present
    Formula:
        - Smallest perimeter = 2 * (smallest + second smallest)
        - Bow = volume = l * w * h

    Args:
        dimensions (Tuple[int, int, int]): A tuple containing the dimensions (length, width, height) of the present

    Returns:
        int: The total feet of ribbon needed for the present
    """
    length, width, height = sorted(dimensions)
    return 2 * (length + width) + (length * width * height)

def main():
    filename = "day2.txt"

    dimensions_list = get_dimensions(filename)
    total_paper = sum(calculate_wrapping_paper(dim) for dim in dimensions_list)
    total_ribbon = sum(calculate_ribbon(dim) for dim in dimensions_list)

    print(f"Part 1: {total_paper}")
    print(f"Part 2: {total_ribbon}")

if __name__ == "__main__":
    main()
