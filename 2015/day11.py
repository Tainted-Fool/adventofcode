"""
--- Day 11: Corporate Policy ---

Santa's previous password expired, and he needs help choosing a new one.

To help him remember his new password after the old one expires, Santa has devised a method of coming up with a password based on the previous one. Corporate policy dictates that passwords must be exactly eight lowercase letters (for security reasons), so he finds his new password by incrementing his old password string repeatedly until it is valid.

Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so on. Increase the rightmost letter one step; if it was z, it wraps around to a, and repeat with the next letter to the left until one doesn't wrap around.

Unfortunately for Santa, a new Security-Elf recently started, and he has imposed some additional password requirements:

    Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
    Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
    Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.

For example:

    hijklmmn meets the first requirement (because it contains the straight hij) but fails the second requirement requirement (because it contains i and l).
    abbceffg meets the third requirement (because it repeats bb and ff) but fails the first requirement.
    abbcegjk fails the third requirement, because it only has one double letter (bb).
    The next password after abcdefgh is abcdffaa.
    The next password after ghijklmn is ghjaabcc, because you eventually skip all the passwords that start with ghi..., since i is not allowed.

Given Santa's current password (your puzzle input), what should his next password be?

Your puzzle input is hepxcrrq.

--- Part Two ---

Santa's password expired again. What's the next one?
"""
import re
from string import ascii_lowercase

def find_next_password(password: str, count: int = 1) -> str:
    """
    Finds the next valid password according to the policy

    Args:
        password (str): The current password
        count (int): how many valid passwords to find

    Returns:
        str: The next valid password after the specified number of increments
    """
    for _ in range(count):
        password = increment_password2(password)
        while not is_valid(password):
            password = increment_password2(password)
    return password

def is_valid(password: str) -> bool:
    """
    Check if the given password meets the security requirements:
        - Must contain an increasing straight of at least three letters
        - Must not contain the letters i, o, or l
        - Must contain at least two different, non-overlapping pairs of letters

    Args:
        password (str): The password to check

    Returns:
        bool: True if the password is valid, False otherwise
    """
    # Requirement 2
    if re.search(r"[iol]", password):
        return False

    # Requirement 1
    for i in range(len(password) - 2):
        if password[i:i+3] in ascii_lowercase:
            break
    else:
        return False

    # Requirement 3
    # return True if re.search(r"(\w)\1.*(\w)\2", password) else False
    # return bool(re.search(r"(\w)\1.*(?!\1)(\w)\3", password))
    return bool(re.search(r"(.)\1.*(.)\2", password))

def increment_password(password: str) -> str:
    """
    Increment the password by one character, wrapping around from 'z' to 'a'

    Args:
        password (str): The current password to increment

    Returns:
        str: The incremented password
    """
    if password.endswith("z"):
        i_z = password.index("z")
        n_z = len(password) - i_z
        boundary_letter = password[i_z - 1]
        return password[:i_z - 1] + next_letter(boundary_letter) + "a" * n_z
    else:
        return password[:-1] + next_letter(password[-1])

def next_letter(c: str) -> str:
    """
    Get the next letter in the alphabet, wrapping around from 'z' to 'a'

    Args:
        c (str): The current character

    Returns:
        str: The next character
    """
    return ascii_lowercase[(ascii_lowercase.index(c) + 1) % 26]

def increment_password2(password: str) -> str:
    """
    Increment the password by one character, wrapping around from 'z' to 'a'

    Args:
        password (str): The current password to increment

    Returns:
        str: The incremented password
    """
    password = list(password)
    for i in range(len(password) - 1, -1, -1):
        if password[i] == 'z':
            password[i] = 'a'
        else:
            password[i] = ascii_lowercase[ascii_lowercase.index(password[i]) + 1]
            break
    return "".join(password)

def main():
    password = "hepxcrrq"

    print(f"Part 1: {find_next_password(password)}")
    print(f"Part 2: {find_next_password(password, 2)}")

if __name__ == "__main__":
    main()
