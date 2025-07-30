"""
--- Day 5: Doesn't He Have Intern-Elves For This? ---

Santa needs help figuring out which strings in his text file are naughty or nice.

A nice string is one with all of the following properties:

    It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.

For example:

    ugknbfddgicrmopn is nice because it has at least three vowels (u...i...o...), a double letter (...dd...), and none of the disallowed substrings.
    aaa is nice because it has at least three vowels and a double letter, even though the letters used by different rules overlap.
    jchzalrnumimnmhp is naughty because it has no double letter.
    haegwjzuvuyypxyu is naughty because it contains the string xy.
    dvszwmarrgswjxmb is naughty because it contains only one vowel.

How many strings are nice?

--- Part Two ---

Realizing the error of his ways, Santa has switched to a better model of determining whether a string is naughty or nice. None of the old rules apply, as they are all clearly ridiculous.

Now, a nice string is one with all of the following properties:

    It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.

For example:

    qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and a letter that repeats with exactly one letter between them (zxz).
    xxyxx is nice because it has a pair that appears twice and a letter that repeats with one between, even though the letters used by each rule overlap.
    uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a single letter between them.
    ieodomkazucvgmuy is naughty because it has a repeating letter with one between (odo), but no pair that appears twice.

How many strings are nice under these new rules?
"""
import re

def is_nice(word: str) -> bool:
    """
    Check if a word is nice according to the original rules
    Rule 1: At least three vowels
    Rule 2: At least one letter that appears twice in a row
    Rule 3: Does not contain disallowed strings

    Args:
        word (str): The word to check

    Returns:
        bool: True if the word is nice, False otherwise
    """
    vowels = ['a', 'e', 'i', 'o', 'u']
    vowel_count = 0
    for char in word:
        if char in vowels:
            vowel_count += 1
    if vowel_count < 3:
        return False

    has_double_letter = False
    for i in range(len(word) - 1):
        if word[i] == word[i + 1]:
            has_double_letter = True
            break
    if not has_double_letter:
        return False

    disallowed = ['ab', 'cd', 'pq', 'xy']
    for bad in disallowed:
        if bad in word:
            return False
    return True

def is_nice_two(word: str) -> bool:
    """
    Check if a word is nice according to the original rules
    Rule 1: At least one pair of any two letters that appears at least twice without overlapping
    Rule 2: At least one letter which repeats with exactly one letter between them

    Args:
        word (str): The word to check

    Returns:
        bool: True if the word is nice, False otherwise
    """
    has_pair_twice = False
    pairs = {}
    for i in range(len(word) - 1):
        pair = word[i:i + 2]
        if pair in pairs:
            if i - pairs[pair] > 1:
                has_pair_twice = True
                break
        else:
            pairs[pair] = i
    if not has_pair_twice:
        return False

    has_repeat_with_gap = False
    for i in range(len(word) - 2):
        if word[i] == word[i + 2]:
            has_repeat_with_gap = True
            break
    return has_repeat_with_gap

def is_nice_regex(word: str) -> bool:
    """
    Check if a word is nice according to the original rules
    Rule 1: At least one pair of any two letters that appears at least twice without overlapping
    Rule 2: At least one letter which repeats with exactly one letter between them

    Args:
        word (str): The word to check

    Returns:
        bool: True if the word is nice, False otherwise
    """
    if len(re.findall(r'[aeiou]', word)) < 3:
        return False

    # (.) captures any character
    # \1 matches the same character again
    if not re.search(r'(.)\1', word):
        return False

    if re.search(r'ab|cd|pq|xy', word):
        return False
    return True

def is_nice_two_regex(word: str) -> bool:
    """
    Check if a word is nice according to the original rules
    Rule 1: At least one pair of any two letters that appears at least twice without overlapping
    Rule 2: At least one letter which repeats with exactly one letter between them

    Args:
        word (str): The word to check

    Returns:
        bool: True if the word is nice, False otherwise
    """
    # (?=...) checks ahead for a pattern without consuming characters
    # (..) captures any two characters
    # .* matches any characters in between
    # \1 matches the same two characters again
    if not re.search(r'(?=(..).*\1)', word):
        return False

    # (.) captures any character
    # . matches any character or skips one
    # \1 matches the same character again
    if not re.search(r'(.).\1', word):
        return False
    return True

def is_nice_simple(word: str) -> bool:
    """
    Check if a word is nice according to the original rules
    Rule 1: At least one pair of any two letters that appears at least twice without overlapping
    Rule 2: At least one letter which repeats with exactly one letter between them

    Args:
        word (str): The word to check

    Returns:
        bool: True if the word is nice, False otherwise
    """
    has_three_vowels = sum(1 for char in word if char in "aeiou") >= 3
    has_double_letter = any(a == b for a, b in zip(word, word[1:]))
    has_disallowed = any(bad in word for bad in ("ab", "cd", "pq", "xy"))
    return has_three_vowels and has_double_letter and not has_disallowed

def is_nice_two_simple(word: str) -> bool:
    """
    Check if a word is nice according to the original rules
    Rule 1: At least one pair of any two letters that appears at least twice without overlapping
    Rule 2: At least one letter which repeats with exactly one letter between them

    Args:
        word (str): The word to check

    Returns:
        bool: True if the word is nice, False otherwise
    """
    has_pair_twice = any(word[i:i+2] in word[i+2:] for i in range(len(word) - 1))
    has_repeat_with_gap = any(word[i] == word[i+2] for i in range(len(word) - 2))
    return has_pair_twice and has_repeat_with_gap

def main():
    filename = "day5.txt"
    count = count2 = 0

    with open(filename, "r") as file:
        for line in file:
            if is_nice(line):
            # if is_nice_regex(line):
            # if is_nice_simple(line):
                count += 1

            if is_nice_two(line):
            # if is_nice_two_regex(line):
            # if is_nice_two_simple(line):
                count2 += 1
    print(f"Part 1: {count}")
    print(f"Part 2: {count2}")

if __name__ == "__main__":
    main()
