"""
--- Day 20: Infinite Elves and Infinite Houses ---

To keep the Elves busy, Santa has them deliver some presents by hand, door-to-door. He sends them down a street with infinite houses numbered sequentially: 1, 2, 3, 4, 5, and so on.

Each Elf is assigned a number, too, and delivers presents to houses based on that number:

    The first Elf (number 1) delivers presents to every house: 1, 2, 3, 4, 5, ....
    The second Elf (number 2) delivers presents to every second house: 2, 4, 6, 8, 10, ....
    Elf number 3 delivers presents to every third house: 3, 6, 9, 12, 15, ....

There are infinitely many Elves, numbered starting with 1. Each Elf delivers presents equal to ten times his or her number at each house.

So, the first nine houses on the street end up like this:

House 1 got 10 presents.
House 2 got 30 presents.
House 3 got 40 presents.
House 4 got 70 presents.
House 5 got 60 presents.
House 6 got 120 presents.
House 7 got 80 presents.
House 8 got 150 presents.
House 9 got 130 presents.

The first house gets 10 presents: it is visited only by Elf 1, which delivers 1 * 10 = 10 presents. The fourth house gets 70 presents, because it is visited by Elves 1, 2, and 4, for a total of 10 + 20 + 40 = 70 presents.

What is the lowest house number of the house to get at least as many presents as the number in your puzzle input?

Your puzzle input is 33100000.

--- Part Two ---

The Elves decide they don't want to visit an infinite number of houses. Instead, each Elf will stop after delivering presents to 50 houses. To make up for it, they decide to deliver presents equal to eleven times their number at each house.

With these changes, what is the new lowest house number of the house to get at least as many presents as the number in your puzzle input?
"""
from array import array

def lowest_house_part1(target: int, search_limit: int) -> int:
    """
    Finds the lowest house number that receives at least 'target' presents

    Args:
        target (int): The minimum number of presents a house should receive
        search_limit (int): The maximum house number to search up to

    Returns:
        int: The lowest house number that meets the target presents
    """
    presents = [0] * (search_limit + 1)

    for elf in range(1, search_limit + 1):
        for house in range(elf, search_limit + 1, elf):
            presents[house] += elf * 10

        if presents[elf] >= target:
            return elf
    raise ValueError("Search limit too small for Part 1")

def lowest_house_part2(target: int, search_limit: int) -> int:
    """
    Finds the lowest house number that receives at least 'target' presents with the new delivery rules

    Args:
        target (int): The minimum number of presents a house should receive
        search_limit (int): The maximum house number to search up to

    Returns:
        int: The lowest house number that meets the target presents
    """
    presents = [0] * (search_limit + 1)

    for elf in range(1, search_limit + 1):
        last_house = min(elf * 50, search_limit)
        for house in range(elf, last_house + 1, elf):
            presents[house] += elf * 11

        if presents[elf] >= target:
            return elf
    raise ValueError("Search limit too small for Part 2")

def sieve_part1(target: int) -> int:
    """
    Finds the lowest house number that receives at least 'target' presents using a sieve-like approach

    Args:
        target (int): The minimum number of presents a house should receive

    Returns:
        int: The lowest house number that meets the target presents
    """
    limit = 100_000
    while True:
        presents = array("L", [0]) * (limit + 1)

        for elf in range(1, limit + 1):
            for house in range(elf, limit + 1, elf):
                presents[house] += elf * 10
            if presents[elf] >= target:
                return elf
        limit *= 2

def sieve_part2(target: int) -> int:
    """
    Finds the lowest house number that receives at least 'target' presents with the new delivery rules using a sieve-like approach

    Args:
        target (int): The minimum number of presents a house should receive

    Returns:
        int: The lowest house number that meets the target presents
    """
    limit = 100_000
    while True:
        presents = array("L", [0]) * (limit + 1)

        for elf in range(1, limit + 1):
            last_house = min(elf * 50, limit)
            for house in range(elf, last_house + 1, elf):
                presents[house] += elf * 11
            if presents[elf] >= target:
                return elf
        limit *= 2

def main():
    """
    Main function to execute the solution for both parts of the problem
    """
    target = 33_100_000
    # limit = 1_000_000

    # print(f"Part 1: {lowest_house_part1(target, limit)}")
    # print(f"Part 2: {lowest_house_part2(target, limit)}")

    print(f"Part 1: {sieve_part1(target)}")
    print(f"Part 2: {sieve_part2(target)}")

if __name__ == "__main__":
    main()
