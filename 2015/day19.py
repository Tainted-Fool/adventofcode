"""
--- Day 19: Medicine for Rudolph ---

Rudolph the Red-Nosed Reindeer is sick! His nose isn't shining very brightly, and he needs medicine.

Red-Nosed Reindeer biology isn't similar to regular reindeer biology; Rudolph is going to need custom-made medicine. Unfortunately, Red-Nosed Reindeer chemistry isn't similar to regular reindeer chemistry, either.

The North Pole is equipped with a Red-Nosed Reindeer nuclear fusion/fission plant, capable of constructing any Red-Nosed Reindeer molecule you need. It works by starting with some input molecule and then doing a series of replacements, one per step, until it has the right molecule.

However, the machine has to be calibrated before it can be used. Calibration involves determining the number of molecules that can be generated in one step from a given starting point.

For example, imagine a simpler machine that supports only the following replacements:

H => HO
H => OH
O => HH

Given the replacements above and starting with HOH, the following molecules could be generated:

    HOOH (via H => HO on the first H).
    HOHO (via H => HO on the second H).
    OHOH (via H => OH on the first H).
    HOOH (via H => OH on the second H).
    HHHH (via O => HH).

So, in the example above, there are 4 distinct molecules (not five, because HOOH appears twice) after one replacement from HOH. Santa's favorite molecule, HOHOHO, can become 7 distinct molecules (over nine replacements: six from H, and three from O).

The machine replaces without regard for the surrounding characters. For example, given the string H2O, the transition H => OO would result in OO2O.

Your puzzle input describes all of the possible replacements and, at the bottom, the medicine molecule for which you need to calibrate the machine. How many distinct molecules can be created after all the different ways you can do one replacement on the medicine molecule?

--- Part Two ---

Now that the machine is calibrated, you're ready to begin molecule fabrication.

Molecule fabrication always begins with just a single electron, e, and applying replacements one at a time, just like the ones during calibration.

For example, suppose you have the following replacements:

e => H
e => O
H => HO
H => OH
O => HH

If you'd like to make HOH, you start with e, and then make the following replacements:

    e => O to get O
    O => HH to get HH
    H => OH (on the second H) to get HOH

So, you could make HOH after 3 steps. Santa's favorite molecule, HOHOHO, can be made in 6 steps.

How long will it take to make the medicine? Given the available replacements and the medicine molecule in your puzzle input, what is the fewest number of steps to go from e to the medicine molecule?
"""
import re
import random

def parse_data(filename: str) -> tuple[dict[str, list[str]], dict[str, str], str]:
    """
    Parses the input file to extract forward and reverse mappings of replacements

    Args:
        filename (str): The name of the input file containing the replacement rules and molecule

    Returns:
        tuple containing:
            - forward (dict[str, list[str]]): A dictionary mapping each left-hand side molecule to a list of right-hand side molecules
            - reverse (dict[str, str]): A dictionary mapping each right-hand side molecule back to its left-hand side molecule
            - molecule (str): The final molecule string
    """
    forward: dict[str, list[str]] = {}
    reverse: dict[str, str] = {}
    molecule = ""

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "=>" in line:
                lhs, rhs = line.split(" => ")
                forward.setdefault(lhs, []).append(rhs)
                reverse[rhs] = lhs
            elif line:
                molecule = line
    return forward, reverse, molecule

def parse_data2(filename: str) -> tuple[dict[str, list[str]], str]:
    """
    Parses the input file to extract forward mappings of replacements and the molecule

    Args:
        filename (str): The name of the input file containing the replacement rules and molecule

    Returns:
        tuple containing:
            - forward (dict[str, list[str]]): A dictionary mapping each left-hand side molecule to a list of right-hand side molecules
            - molecule (str): The final molecule string
    """
    forward: dict[str, list[str]] = {}
    molecule = ""

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if "=>" in line:
                lhs, rhs = line.split(" => ")
                forward.setdefault(lhs, []).append(rhs)
            elif line:
                molecule = line
    return forward, molecule

def distinct_one_step(forward: dict[str, list[str]], molecule: str) -> set[str]:
    """
    Generates distinct molecules by applying one replacement from the forward mapping

    Args:
        forward (dict[str, list[str]]): A dictionary mapping each left-hand side molecule to a list of right-hand side molecules
        molecule (str): The initial molecule string

    Returns:
        set[str]: A set of distinct molecules generated by one replacement
    """
    results: set[str] = set()

    for lhs, replacements in forward.items():
        start = 0
        while (index := molecule.find(lhs, start)) != -1:
            for rhs in replacements:
                new_molecule = molecule[:index] + rhs + molecule[index + len(lhs) :]
                results.add(new_molecule)
            start = index + 1
    return results

def distinct_one_step2(forward: dict[str, list[str]], molecule: str) -> set[str]:
    """
    Generates distinct molecules by applying one replacement from the forward mapping

    Args:
        forward (dict[str, list[str]]): A dictionary mapping each left-hand side molecule to a list of right-hand side molecules
        molecule (str): The initial molecule string

    Returns:
        set[str]: A set of distinct molecules generated by one replacement
    """
    results: set[str] = set()

    for lhs, replacements in forward.items():
        for mol in re.finditer(lhs, molecule):
            index = mol.start()
            for rhs in replacements:
                new_molecule = molecule[:index] + rhs + molecule[index + len(lhs) :]
                results.add(new_molecule)
    return results

def fewest_steps(reverse: dict[str, str], target: str) -> int:
    """
    Finds the fewest number of steps to go from 'e' to the target molecule using the reverse mapping

    Args:
        reverse (dict[str, str]): A dictionary mapping each right-hand side molecule back to its left-hand side molecule
        target (str): The target molecule string

    Returns:
        int: The fewest number of steps required to create the target molecule from 'e'
    """
    keys = sorted(reverse.keys(), key=len, reverse=True)

    attempt = 0
    while True:
        attempt += 1
        steps = 0
        current = target

        random.shuffle(keys)

        while current != "e":
            original = current
            for rhs in keys:
                if rhs in current:
                    current = current.replace(rhs, reverse[rhs], 1)
                    steps += 1
                    break
            if current == original:
                break

        if current == "e":
            return steps

def fewest_steps_formula(molecule: str) -> int:
    """
    Calculates the fewest number of steps to create the target molecule from 'e' using a formula

    Args:
        molecule (str): The target molecule string

    Returns:
        int: The fewest number of steps required to create the target molecule from 'e'
    """
    regex = re.compile(r"[A-Z][a-z]?")
    tokens = regex.findall(molecule)
    steps = (
        len(tokens)
        - molecule.count("Rn")
        - molecule.count("Ar")
        - 2 * molecule.count("Y")
        - 1
    )
    return steps

def main():
    """
    Main function to execute the solution for Day 19 of Advent of Code 2015
    """
    filename = "day19.txt"
    # forward, reverse, molecule = parse_data(filename)

    # print(f"Part 1: {len(distinct_one_step(forward, molecule))}")
    # print(f"Part 2: {fewest_steps(reverse, molecule)}")

    forward, molecule = parse_data2(filename)

    print(f"Part 1: {len(distinct_one_step2(forward, molecule))}")
    print(f"Part 2: {fewest_steps_formula(molecule)}")

if __name__ == "__main__":
    main()
