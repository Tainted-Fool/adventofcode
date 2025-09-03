"""
--- Day 12: JSAbacusFramework.io ---

Santa's Accounting-Elves need help balancing the books after a recent order. Unfortunately, their accounting software uses a peculiar storage format. That's where you come in.

They have a JSON document which contains a variety of things: arrays ([1,2,3]), objects ({"a":1, "b":2}), numbers, and strings. Your first job is to simply find all of the numbers throughout the document and add them together.

For example:

    [1,2,3] and {"a":2,"b":4} both have a sum of 6.
    [[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.
    {"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.
    [] and {} both have a sum of 0.

You will not encounter any strings containing numbers.

What is the sum of all numbers in the document?

--- Part Two ---

Uh oh - the Accounting-Elves have realized that they double-counted everything red.

Ignore any object (and all of its children) which has any property with the value "red". Do this only for objects ({...}), not arrays ([...]).

    [1,2,3] still has a sum of 6.
    [1,{"c":"red","b":2},3] now has a sum of 4, because the middle object is ignored.
    {"d":"red","e":[1,2,3,4],"f":5} now has a sum of 0, because the entire structure is ignored.
    [1,"red",5] has a sum of 6, because "red" in an array has no effect.

What is the sum of all numbers in the document after ignoring "red" object?
"""
import json
import re
from typing import cast

JSONType = int | str | list["JSONType"] | dict[str, "JSONType"]
def filter_red(obj: dict[str, JSONType]) -> dict[str, JSONType]:
    """
    Custom object hook to remove dictionaries containing the value "red"

    Args:
        obj (dict[str, JSONType]): A JSON parsed from the file

    Returns:
        dict[str, JSONType]: The object itself or an empty dictionary if it contains "red"
    """
    if "red" in obj.values():
        return {}
    return obj

def remove_red(obj: JSONType) -> int:
    """
    Recursively sums all numbers in a JSON-like structure, ignoring objects with "red" values

    Args:
        obj (JSONType): The JSON-like structure (could be a list, dict, or int)

    Returns:
        int: The sum of all numbers, ignoring objects with "red" values
    """
    text = json.dumps(obj)
    # filter_data = json.loads(text, object_hook=lambda d: {k: v for k, v in d.items() if "red" not in d.values()})
    filter_data = cast(JSONType, json.loads(text, object_hook=filter_red))
    return extract_numbers(filter_data)

def sum_numbers(obj: JSONType) -> int:
    """
    Recursively sums all numbers in a JSON-like structure, ignoring objects with "red" values

    Args:
        obj (JSONType): The JSON-like structure (could be a list, dict, or int)

    Returns:
        int: The sum of all numbers, ignoring objects with "red" values
    """
    if isinstance(obj, int):
        return obj
    if isinstance(obj, list):
        return sum(sum_numbers(item) for item in obj)
    if isinstance(obj, dict):
        if "red" in obj.values():
            return 0
        return sum(sum_numbers(value) for value in obj.values())
    return 0

def extract_numbers(data: JSONType) -> int:
    """
    Extracts all numbers from a JSON-like structure and returns their sum

    Args:
        data (JSONType): The JSON-like structure as a string

    Returns:
        int: The sum of all numbers found in the structure
    """
    return sum(map(int, re.findall(r"-?\d+", json.dumps(data))))

def main():
    """
    Main function to read the JSON file and compute the required sums
    """
    filename = "day12.json"
    with open(filename, "r", encoding="utf-8") as file:
        data = cast(JSONType, json.load(file))

    print(f"Part 1: {extract_numbers(data)}")
    print(f"Part 2: {remove_red(data)}")
    # print(f"Part 2: {sum_numbers(data)}")

if __name__ == "__main__":
    main()
