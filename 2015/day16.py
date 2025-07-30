"""
--- Day 16: Aunt Sue ---

Your Aunt Sue has given you a wonderful gift, and you'd like to send her a thank you card. However, there's a small problem: she signed it "From, Aunt Sue".

You have 500 Aunts named "Sue".

So, to avoid sending the card to the wrong person, you need to figure out which Aunt Sue (which you conveniently number 1 to 500, for sanity) gave you the gift. You open the present and, as luck would have it, good ol' Aunt Sue got you a My First Crime Scene Analysis Machine! Just what you wanted. Or needed, as the case may be.

The My First Crime Scene Analysis Machine (MFCSAM for short) can detect a few specific compounds in a given sample, as well as how many distinct kinds of those compounds there are. According to the instructions, these are what the MFCSAM can detect:

    children, by human DNA age analysis.
    cats. It doesn't differentiate individual breeds.
    Several seemingly random breeds of dog: samoyeds, pomeranians, akitas, and vizslas.
    goldfish. No other kinds of fish.
    trees, all in one group.
    cars, presumably by exhaust or gasoline or something.
    perfumes, which is handy, since many of your Aunts Sue wear a few kinds.

In fact, many of your Aunts Sue have many of these. You put the wrapping from the gift into the MFCSAM. It beeps inquisitively at you a few times and then prints out a message on ticker tape:

children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1

You make a list of the things you can remember about each Aunt Sue. Things missing from your list aren't zero - you simply don't remember the value.

What is the number of the Sue that got you the gift?

--- Part Two ---

As you're about to send the thank you note, something in the MFCSAM's instructions catches your eye. Apparently, it has an outdated retroencabulator, and so the output from the machine isn't exact values - some of them indicate ranges.

In particular, the cats and trees readings indicates that there are greater than that many (due to the unpredictable nuclear decay of cat dander and tree pollen), while the pomeranians and goldfish readings indicate that there are fewer than that many (due to the modial interaction of magnetoreluctance).

What is the number of the real Aunt Sue?
"""
import re
from collections import defaultdict
from typing import Dict

def parse_input(filename: str) -> Dict[int, Dict[str, int]]:
    """
    Parse the input file and return a dictionary mapping Aunt Sue profiles

    Args:
        filename (str): The name of the input file

    Returns:
        Dict[int, Dict[str, int]]: A dictionary where keys are Aunt Sue numbers and values are dictionaries of properties
    """
    pattern = r"(\w+): (\d+),?"
    aunts = {}

    with open(filename, "r") as file:
        for index, line in enumerate(file, start=1):
            aunts[index] = {}
            for prop, val in re.findall(pattern, line):
                aunts[index][prop] = int(val)
    return aunts

def match_sue(sue_attributes: Dict[str, int], mfcsam: Dict[str, int], part_two: bool = False) -> bool:
    """
    Determines whether a Sue attributes match the MFCSAM description

    Args:
        sue_attributes (Dict[str, int]): Attributes of the Aunt Sue
        mfcsam (Dict[str, int]): The MFCSAM reference tape
        part_two (bool): If True, applies the rules for part two

    Returns:
        bool: True if Sue match, False otherwise
    """
    for item, sue_value in sue_attributes.items():
        target_value = mfcsam[item]

        if part_two:
            if item in ("cats", "trees"):
                if sue_value <= target_value:
                    return False
            elif item in ("pomeranians", "goldfish"):
                if sue_value >= target_value:
                    return False
            elif sue_value != target_value:
                return False
        else:
            if sue_value != target_value:
                return False
    return True

def find_sue(aunts: Dict[int, Dict[str, int]], mfcsam: Dict[str, int], part_two: bool = False) -> int:
    """
    Finds the Aunt Sue that matches the MFCSAM data

    Args:
        aunts (Dict[int, Dict[str, int]]): Dictionary of all Aunt Sues
        mfcsam (Dict[str, int]): The MFCSAM reference tape
        part_two (bool): If True, applies the rules for part two

    Returns:
        int: The number of the matching Aunt Sue
    """
    for sue_number, attributes in aunts.items():
        if match_sue(attributes, mfcsam, part_two):
            return sue_number
    return -1  # not found

def main():
    filename = "day16.txt"
    mfcsam_tape = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }
    aunts = parse_input(filename)

    print(f"Part 1: {find_sue(aunts, mfcsam_tape)}")
    print(f"Part 2: {find_sue(aunts, mfcsam_tape, True)}")

if __name__ == "__main__":
    main()
