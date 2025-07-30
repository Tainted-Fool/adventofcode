"""
--- Day 23: Opening the Turing Lock ---

Little Jane Marie just got her very first computer for Christmas from some unknown benefactor. It comes with instructions and an example program, but the computer itself seems to be malfunctioning. She's curious what the program does, and would like you to help her run it.

The manual explains that the computer supports two registers and six instructions (truly, it goes on to remind the reader, a state-of-the-art technology). The registers are named a and b, can hold any non-negative integer, and begin with a value of 0. The instructions are as follows:

    hlf r sets register r to half its current value, then continues with the next instruction.
    tpl r sets register r to triple its current value, then continues with the next instruction.
    inc r increments register r, adding 1 to it, then continues with the next instruction.
    jmp offset is a jump; it continues with the instruction offset away relative to itself.
    jie r, offset is like jmp, but only jumps if register r is even ("jump if even").
    jio r, offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).

All three jump instructions work with an offset relative to that instruction. The offset is always written with a prefix + or - to indicate the direction of the jump (forward or backward, respectively). For example, jmp +1 would simply continue with the next instruction, while jmp +0 would continuously jump back to itself forever.

The program exits when it tries to run an instruction beyond the ones defined.

For example, this program sets a to 2, because the jio instruction causes it to skip the tpl instruction:

inc a
jio a, +2
tpl a
inc a

What is the value in register b when the program in your puzzle input is finished executing?

--- Part Two ---

The unknown benefactor is very thankful for releasi-- er, helping little Jane Marie with her computer. Definitely not to distract you, what is the value in register b after the program is finished executing if register a starts as 1 instead?
"""
import re
from typing import Dict, List, Tuple

def execute_program(registers: Dict[str, int], instructions: List[Tuple[str, str, str]]) -> int:
    """
    Execute the instructions on the registers and return the value in register 'b'

    Args:
        registers (Dict[str, int]): A dictionary containing the initial values of registers 'a' and 'b'
        instructions (List[Tuple[str, str, str]]): A list of instructions to execute

    Returns:
        int: The value in register 'b' after executing all instructions
    """
    pointer = 0

    while 0 <= pointer < len(instructions):
        op, x, y = instructions[pointer]

        match op:
            case "hlf":
                registers[x] //= 2
            case "tpl":
                registers[x] *= 3
            case "inc":
                registers[x] += 1
            case "jmp":
                pointer += int(x) - 1
            case "jie":
                if registers[x] % 2 == 0:
                    pointer += int(y) - 1
            case "jio":
                if registers[x] == 1:
                    pointer += int(y) - 1
        pointer += 1
    return registers["b"]

def parse_data(filename: str) -> List[Tuple[str, str, str]]:
    """
    Parse the input file and return a list of instructions

    Args:
        filename (str): The name of the input file

    Returns:
        List[Tuple[str, str, str]]: A list of instructions where each instruction is
    """
    with open(filename, "r") as file:
        input = file.read().strip()

    pattern = r"(\w+) (\S+)(?:, (\S+))?$"
    return re.findall(pattern, input, re.M)

def main():
    filename = "day23.txt"
    instructions = parse_data(filename)

    print(f"Part 1: {execute_program({'a': 0, 'b': 0}, instructions)}")
    print(f"Part 2: {execute_program({'a': 1, 'b': 0}, instructions)}")

if __name__ == "__main__":
    main()
