"""
--- Day 15: Science for Hungry People ---

Today, you set out on the task of perfecting your milk-dunking cookie recipe. All you have to do is find the right balance of ingredients.

Your recipe leaves room for exactly 100 teaspoons of ingredients. You make a list of the remaining ingredients you could use to finish the recipe (your puzzle input) and their properties per teaspoon:

    capacity (how well it helps the cookie absorb milk)
    durability (how well it keeps the cookie intact when full of milk)
    flavor (how tasty it makes the cookie)
    texture (how it improves the feel of the cookie)
    calories (how many calories it adds to the cookie)

You can only measure ingredients in whole-teaspoon amounts accurately, and you have to be accurate so you can reproduce your results in the future. The total score of a cookie can be found by adding up each of the properties (negative totals become 0) and then multiplying together everything except calories.

For instance, suppose you have these two ingredients:

Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

Then, choosing to use 44 teaspoons of butterscotch and 56 teaspoons of cinnamon (because the amounts of each ingredient must add up to 100) would result in a cookie with the following properties:

    A capacity of 44*-1 + 56*2 = 68
    A durability of 44*-2 + 56*3 = 80
    A flavor of 44*6 + 56*-2 = 152
    A texture of 44*3 + 56*-1 = 76

Multiplying these together (68 * 80 * 152 * 76, ignoring calories for now) results in a total score of 62842880, which happens to be the best score possible given these ingredients. If any properties had produced a negative total, it would have instead become zero, causing the whole score to multiply to zero.

Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you can make?

--- Part Two ---

Your cookie recipe becomes wildly popular! Someone asks if you can make another recipe that has exactly 500 calories per cookie (so they can use it as a meal replacement). Keep the rest of your award-winning process the same (100 teaspoons, same ingredients, same scoring system).

For example, given the ingredients above, if you had instead selected 40 teaspoons of butterscotch and 60 teaspoons of cinnamon (which still adds to 100), the total calorie count would be 40*8 + 60*3 = 500. The total score would go down, though: only 57600000, the best you can do in such trying circumstances.

Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you can make with a calorie total of 500?
"""
import re
from itertools import product
from functools import reduce
from operator import mul
from collections.abc import Generator
from typing import cast

def parse_data(filename: str) -> list[list[int]]:
    """
    Parses the input file and returns a list of tuples containing ingredient properties

    Args:
        filename (str): The name of the input file

    Returns:
        list[list[int]]: A list of ingredient properties, each containing capacity, durability, flavor, texture, but not calories of an ingredient
    """
    ingredients: list[list[int]] = []
    pattern = re.compile(r"-?\d+")

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            properties = list(map(int, pattern.findall(line)))
            ingredients.append(properties)
    return ingredients

def calculate_score(ingredients: list[list[int]], amounts: tuple[int, ...]) -> tuple[int, int]:
    """
    Given a tuple of ingredient amounts and a list of igredent properties, calculates the score and calorie count of the cookie

    Args:
        ingredients (list[list[int]]): A list containing properties of an ingredient
        amounts (tuple[int, ...]): A tuple containing the amounts of each ingredient

    Returns:
        tuple[int, int]: A tuple containing the total score and calorie count of the cookie
    """
    totals = [0, 0, 0, 0]  # capacity, durability, flavor, texture
    total_calories = 0

    for amount, ingredient in zip(amounts, ingredients):
        for i in range(4):
            totals[i] += amount * ingredient[i]
        total_calories += amount * ingredient[4]

    totals = [max(0, total) for total in totals]  # Ensure no negative totals
    total_score = cast(int, reduce(mul, totals))

    return total_score, total_calories

def generate_combinations(ingredient_count: int, total_amount: int = 100) -> Generator[tuple[int, ...]]:
    """
    Generates all combinations of ingredient amounts that sum to `total_amount`
    Assume exactly 4 ingredients for simplicity

    Args:
        ingredient_count (int): The number of ingredients
        total_amount (int): The total amount of ingredients to use, default is 100

    Returns:
        Generator[tuple[int, ...]]: A tuple, each containing amounts of each ingredient that sum to `total_amount`
    """
    assert ingredient_count == 4, "This function is designed for exactly 4 ingredients"
    for a in range(total_amount + 1):
        for b in range(total_amount - a + 1):
            for c in range(total_amount - a - b + 1):
                d = total_amount - a - b - c
                yield (a, b, c, d)

def generate_products(ingredient_count: int, total_amount: int = 100) -> Generator[tuple[int, ... ]]:
    """
    Generates all combinations of ingredient amounts that sum to `total_amount` using product
    Args:
        ingredient_count (int): The number of ingredients
        total_amount (int): The total amount of ingredients to use, default is 100

    Returns:
        Generator[tuple[int]]: A tuple, each containing amounts of each ingredient that sum to `total_amount`
    """
    for combo in product(range(total_amount + 1), repeat=ingredient_count):
        if sum(combo) == total_amount:
            yield combo

def recursive_generate(ingredient_count: int, total_amount: int = 100) -> Generator[tuple[int, ...], None, None]:
    """
    Recrsively generates all combinations of integers that sum to `total_amount`

    Args:
        ingredient_count (int): The number of ingredients
        total_amount (int): The target sum

    Yields:
        Generator[tuple[int, ...]]: A combination of integers summing to `total_amount`
    """
    if ingredient_count == 1:
        yield (total_amount,)
    else:
        for i in range(total_amount + 1):
            for rest in recursive_generate(ingredient_count - 1, total_amount - i):
                yield (i,) + rest

def recursive_score(ingredients: list[list[int]], amounts: tuple[int, ...]) -> tuple[int, int]:
    """
    Computes the score and calorie count for a given combination of ingredient amount

    Args:
        ingredients (list[list[int]]): A list of ingredient properties
        amounts (tuple[int, ...]): A tuple containing the amounts of each ingredient

    Returns:
        tuple[int, int]: A tuple containing the total score and calorie count of the recipe
    """
    num_properties = len(ingredients[0])
    property_totals = [0] * num_properties

    for i, amount in enumerate(amounts):
        for j in range(num_properties):
            property_totals[j] += amount * ingredients[i][j]

    # Calories are the last property
    calories = property_totals[-1]

    # Score is the product of all other properties (negative become 0)
    score = 1
    for total in property_totals[:-1]:
        score *= max(0, total)

    return score, calories

def main():
    """
    Main function to execute the solution for Day 15 of Advent of Code 2015
    """
    filename = "day15.txt"
    ingredients = parse_data(filename)
    part1 = part2 = 0

    # for amounts in generate_products(len(ingredients)):  # this is slower
    for amounts in recursive_generate(len(ingredients)):  # recursive approach
    # for amounts in generate_combinations(len(ingredients)):
        # score, calories = calculate_score(ingredients, amounts)
        score, calories = recursive_score(ingredients, amounts)  # recursive approach
        if calories == 500:
            part2 = max(part2, score)
        part1 = max(part1, score)

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == "__main__":
    main()
