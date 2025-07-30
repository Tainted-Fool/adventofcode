"""
--- Day 17: No Such Thing as Too Much ---

The elves bought too much eggnog again - 150 liters this time. To fit it all into your refrigerator, you'll need to move it into smaller containers. You take an inventory of the capacities of the available containers.

For example, suppose you have containers of size 20, 15, 10, 5, and 5 liters. If you need to store 25 liters, there are four ways to do it:

    15 and 10
    20 and 5 (the first 5)
    20 and 5 (the second 5)
    15, 5, and 5

Filling all containers entirely, how many different combinations of containers can exactly fit all 150 liters of eggnog?

--- Part Two ---

While playing with all the containers in the kitchen, another load of eggnog arrives! The shipping and receiving department is requesting as many containers as you can spare.

Find the minimum number of containers that can exactly fit all 150 liters of eggnog. How many different ways can you fill that number of containers and still hold exactly 150 litres?

In the example above, the minimum number of containers was two. There were three ways to use that many containers, and so the answer there would be 3.
"""
from itertools import combinations
from typing import List, Tuple

def parse_data(filename: str) -> List[int]:
    """
    Returns a list of container sizes from the input file

    Args:
        filename (str): The name of the input file

    Returns:
        List[int]: A list of integers representing the sizes of the containers
    """
    containers = []
    with open(filename, "r") as file:
        for line in file:
            containers.append(int(line.strip()))
        return containers
        # return [int(line.strip()) for line in file]

def count_valid_combos(sizes: List[int], target: int) -> Tuple[int, int]:
    """
    Counts all combinations that sums to `target`
    Counts all combinations that use the minimun number of containers

    Args:
        sizes (List[int]): List of container sizes
        target (int): The target sum to achieve with the combinations

    Returns:
        Tuple[int, int]: A tuple containing the count of all valid combinations and the count of combinations using the minimum number of containers
    """
    total_valid = 0
    min_size = None
    combos_with_min_size = 0

    for i in range(1, len(sizes) + 1):
        for combo in combinations(sizes, i):
            if sum(combo) == target:
                total_valid += 1

                if min_size is None or i < min_size:
                    min_size = i
                    combos_with_min_size = 1
                elif i == min_size:
                    combos_with_min_size += 1
    return total_valid, combos_with_min_size

def main():
    filename = "day17.txt"
    target_volume = 150

    container_sizes = parse_data(filename)
    part1, part2 = count_valid_combos(container_sizes, target_volume)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == "__main__":
    main()
