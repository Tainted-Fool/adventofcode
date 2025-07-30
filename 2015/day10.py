"""
--- Day 10: Elves Look, Elves Say ---

Today, the Elves are playing a game called look-and-say. They take turns making sequences by reading aloud the previous sequence and using that reading as the next sequence. For example, 211 is read as "one two, two ones", which becomes 1221 (1 2, 2 1s).

Look-and-say sequences are generated iteratively, using the previous value as input for the next step. For each step, take the previous value, and replace each run of digits (like 111) with the number of digits (3) followed by the digit itself (1).

For example:

    1 becomes 11 (1 copy of digit 1).
    11 becomes 21 (2 copies of digit 1).
    21 becomes 1211 (one 2 followed by one 1).
    1211 becomes 111221 (one 1, one 2, and two 1s).
    111221 becomes 312211 (three 1s, two 2s, and one 1).

Starting with the digits in your puzzle input, apply this process 40 times. What is the length of the result?

--- Part Two ---

Neat, right? You might also enjoy hearing John Conway talking about this sequence (that's Conway of Conway's Game of Life fame).

Now, starting again with the digits in your puzzle input, apply this process 50 times. What is the length of the new result?
"""
from itertools import groupby

def look_and_say(sequence: str, iterations: int) -> str:
    """
    Applies the look-and-say process multiple times

    Args:
        sequence (str): The current sequence of numbers
        iterations (int): The number of iterations to apply the transformation

    Returns:
        str: The final sequence after the specified number of iterations
    """
    for _ in range(iterations):
        output = ''
        last_char = sequence[0]
        count = 1

        for char in sequence[1:]:
            if char == last_char:
                count += 1
            else:
                output += str(count) + last_char
                last_char = char
                count = 1

        output += str(count) + last_char
        sequence = output
    return sequence

def iterate_look_and_say(sequence: str, iterations: int) -> str:
    """
    Applies the look-and-say process multiple times

    Args:
        sequence (str): The initial sequence of numbers
        iterations (int): The number of iterations to apply the transformation

    Returns:
        str: The final sequence after the specified number of iterations
    """
    for _ in range(iterations):
        output = []
        for digit, group in groupby(sequence):
            output.append(str(len(list(group))) + digit)
        sequence = ''.join(output)
    return sequence
    #     sequence = ''.join([str(len(list(g))) + str(k) for k, g in groupby(sequence)])
    # return sequence

def main():
    input = "1321131112"
    answer = look_and_say(input, 40)
    print(f"Part 1: {len(answer)}")

    answer = iterate_look_and_say(answer, 10)
    print(f"Part 2: {len(answer)}")

if __name__ == "__main__":
    main()
