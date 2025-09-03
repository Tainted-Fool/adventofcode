"""
--- Day 13: Knights of the Dinner Table ---

In years past, the holiday feast with your family hasn't gone so well. Not everyone gets along! This year, you resolve, will be different. You're going to find the optimal seating arrangement and avoid all those awkward conversations.

You start by writing up a list of everyone invited and the amount their happiness would increase or decrease if they were to find themselves sitting next to each other person. You have a circular table that will be just big enough to fit everyone comfortably, and so each person will have exactly two neighbors.

For example, suppose you have only four attendees planned, and you calculate their potential happiness as follows:

Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.

Then, if you seat Alice next to David, Alice would lose 2 happiness units (because David talks so much), but David would gain 46 happiness units (because Alice is such a good listener), for a total change of 44.

If you continue around the table, you could then seat Bob next to Alice (Bob gains 83, Alice gains 54). Finally, seat Carol, who sits next to Bob (Carol gains 60, Bob loses 7) and David (Carol gains 55, David gains 41). The arrangement looks like this:

     +41 +46
+55   David    -2
Carol       Alice
+60    Bob    +54
     -7  +83

After trying every other seating arrangement in this hypothetical scenario, you find that this one is the most optimal, with a total change in happiness of 330.

What is the total change in happiness for the optimal seating arrangement of the actual guest list?

--- Part Two ---

In all the commotion, you realize that you forgot to seat yourself. At this point, you're pretty apathetic toward the whole thing, and your happiness wouldn't really go up or down regardless of who you sit next to. You assume everyone else would be just as ambivalent about sitting next to you, too.

So, add yourself to the list, and give all happiness relationships that involve you a score of 0.

What is the total change in happiness for the optimal seating arrangement that actually includes yourself?
"""
import re
import copy
# from collections import defaultdict
from itertools import permutations

def parse_input(filename: str) -> dict[str, dict[str, int]]:
    """
    Parses the input file and builds a nested dictionary of happiness values

    Args:
        filename (str): The name of the input file

    Returns:
        dict[str, dict[str, int]]: a nested dictionary of the form seating[person1][person2] = happiness
    """
    # seating: dict[str, dict[str, int]] = defaultdict(dict)
    seating: dict[str, dict[str, int]] = {}

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).", line)
            if match:
                person1, action, value, person2 = match.groups()
                happiness = int(value)
                if action == "lose":
                    happiness = -happiness

                if person1 not in seating:
                    seating[person1] = {}
                seating[person1][person2] = happiness
    return seating

def find_happiness(seating: dict[str, dict[str, int]], me: bool = False) -> int:
    """
    Calculates the maximum happiness for a given seating arrangement

    Args:
        seating (dict[str, dict[str, int]]): A nested dictionary of happiness values
        me (bool): Whether to include yourself in the seating arrangement

    Returns:
        int: The maximum happiness for the optimal seating arrangement
    """
    seating = copy.deepcopy(seating)  # Create a copy to avoid modifying the original

    if me:
        seating["me"] = {}
        for person in seating:
            seating[person]["me"] = 0
            seating["me"][person] = 0

    max_happiness = 0
    for ordering in permutations(seating):
        happiness = sum(seating[a][b] + seating[b][a] for a, b in zip(ordering, ordering[1:]))
        happiness += seating[ordering[0]][ordering[-1]] + seating[ordering[-1]][ordering[0]]
        max_happiness = max(max_happiness, happiness)
    return max_happiness

def main():
    """
    Main function to read the input file and compute the required happiness values
    """
    filename = "day13.txt"
    seating = parse_input(filename)

    print(f"Part 1: {find_happiness(seating)}")
    print(f"Part 2: {find_happiness(seating, True)}")

if __name__ == "__main__":
    main()
