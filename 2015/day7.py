"""
--- Day 7: Some Assembly Required ---

This year, Santa brought little Bobby Tables a set of wires and bitwise logic gates! Unfortunately, little Bobby is a little under the recommended age range, and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit signal (a number from 0 to 65535). A signal is provided to each wire by a gate, another wire, or some specific value. Each wire can only get a signal from one source, but can provide its signal to multiple destinations. A gate provides no signal until all of its inputs have a signal.

The included instructions booklet describes how to connect the parts together: x AND y -> z means to connect wires x and y to an AND gate, and then connect its output to wire z.

For example:

    123 -> x means that the signal 123 is provided to wire x.
    x AND y -> z means that the bitwise AND of wire x and wire y is provided to wire z.
    p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then provided to wire q.
    NOT e -> f means that the bitwise complement of the value from wire e is provided to wire f.

Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If, for some reason, you'd like to emulate the circuit instead, almost all programming languages (for example, C, JavaScript, or Python) provide operators for these gates.

For example, here is a simple circuit:

123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i

After it is run, these are the signals on the wires:

d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456

In little Bobby's kit's instructions booklet (provided as your puzzle input), what signal is ultimately provided to wire a?

--- Part Two ---

Now, take the signal you got on wire a, override wire b to that signal, and reset the other wires (including wire a). What new signal is ultimately provided to wire a?
"""
from functools import lru_cache
from typing import Callable

def parse_instructions(filename: str) -> dict[str, list[str]]:
    """
    Parses circuit instructions from a file into a dictionary structure

    Each line of the file is expected to be in the format "expression -> wire". The expression
    is split into its components to form a list, which is then associated with the corresponding
    wire identifier in the returned dictionary

    Args:
        filename (str): The path to the input file containing wire instructions

    Returns:
        dict[str, list[str]]: A dictionary mapping wire names to their operations
    """
    instructions: dict[str, list[str]] = {}
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            if "->" in line:
                left_side, wire = line.strip().split(" -> ")
                instructions[wire] = left_side.split()
    return instructions
        # return {
        #     result.strip(): operation.split()
        #     for line in file
        #     for operation, result in [line.strip().split('->')]
        # }

def build_calculator(instructions: dict[str, list[str]]) -> Callable[[str], int]:
    """
    Creates a cached calculator function for computing the signal on a given wire

    This function returns a nested, memoized `calculate` function that evaluates
    the 16-bit signal for any wire identifier or numeric signal specified. The function
    handles direct assignments, unary operations (like NOT), and binary operations (such as AND,
    OR, LSHIFT, and RSHIFT), ensuring that the results conform to the 16-bit constraint

    Args:
        instructions (dict[str, list[str]]): A dictionary mapping wire identifiers to a list of operation
            components. Each value represents an operation in the form of a list of strings,
            describing how to compute the signal for that wire

    Returns:
        Callable[[str], int]: A function that takes a wire identifier (or integer as a string)
            and returns the computed 16-bit signal as an integer
    """
    @lru_cache(maxsize=None)
    def calculate(wire: str) -> int:
        """
        Recursively calculates the 16-bit signal for a given wire or numeric value

        This function evaluates the signal by performing one of the following:
            - Direct assignment i.e. "123" or assignment like "x -> y"
            - Unary operation like NOT
            - Binary operations like AND, OR, LSHIFT, RSHIFT
        All results are constrained to a 16-bit value (0 to 65535)

        Args:
            wire (str): The wire identifier or numeric signal

        Returns:
            int: The computed 16-bit signal
        """
        try:
            return int(wire)  # Direct number assignment
        except ValueError:
            pass

        operation = instructions[wire]
        if len(operation) == 1:  # Direct wire assignment
            return calculate(operation[0])
        if operation[0] == "NOT":  # Unary operation
            return ~calculate(operation[1]) & 0xFFFF
        left_operand, operator, right_operand = operation

        operations: dict[str, Callable[[int, int], int]] = {  # Binary operations
            "AND": lambda x, y: x & y,
            "OR": lambda x, y: x | y,
            # "NOT": lambda x, _: ~x & 0xFFFF,
            "RSHIFT": lambda x, y: x >> y,
            "LSHIFT": lambda x, y: x << y,
            # "LSHIFT": lambda x, y: (x << y) & 0xFFFF  # Maintain 16-bit result,
        }
        return operations[operator](calculate(left_operand), calculate(right_operand))
    return calculate

def main():
    """
    Main function to execute the circuit assembly and signal calculation
    """
    filename = "day7.txt"

    instructions = parse_instructions(filename)
    calculate = build_calculator(instructions)

    part1 = calculate("a")
    print(f"Part 1: {part1}")

    instructions["b"] = [str(part1)]
    calculate = build_calculator(instructions)  # Rebuild the calculator with updated instructions
    print(f"Part 2: {calculate('a')}")

if __name__ == "__main__":
    main()
