"""
--- Day 4: The Ideal Stocking Stuffer ---

Santa needs help mining some AdventCoins (very similar to bitcoins) to use as gifts for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at least five zeroes. The input to the MD5 hash is some secret key (your puzzle input, given below) followed by a number in decimal. To mine AdventCoins, you must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...) that produces such a hash.

For example:

    If your secret key is abcdef, the answer is 609043, because the MD5 hash of abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest such number to do so.
    If your secret key is pqrstuv, the lowest number it combines with to make an MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of pqrstuv1048970 looks like 000006136ef....

Your puzzle input is yzbqklnj.

--- Part Two ---

Now find one that starts with six zeroes.
"""
import hashlib

def find_adventcoin(secret_key: str, leading_zeros: int) -> tuple[int, str]:
    """
    Brute-force search for the lowest integer that, when appended to the secret key, produces an MD5 hash starting with the specified number of leading zeros

    Args:
        secret_key (str): The secret key to use for hashing
        leading_zeros (int): The number of leading zeros the hash must start with

    Returns:
        tuple[int, str]: A tuple containing the lowest number and the corresponding hash
    """
    prefix = "0" * leading_zeros
    number = 1

    while True:
        my_hash = hashlib.md5(f"{secret_key}{number}".encode()).hexdigest()
        if my_hash.startswith(prefix):
            return number, my_hash
        number += 1

def main():
    """
    Main function to find the AdventCoin for the given secret key with specified leading zeros
    """
    secret_key = "yzbqklnj"

    num, my_hash = find_adventcoin(secret_key, 5)
    print(f"Part 1: number = {num}, hash = {my_hash}")

    num, my_hash = find_adventcoin(secret_key, 6)
    print(f"Part 2: number = {num}, hash = {my_hash}")

if __name__ == "__main__":
    main()
