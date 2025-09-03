"""
--- Day 9: All in a Single Night ---

Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit; his elves have provided him the distances between every pair of locations. He can start and end at any two (different) locations he wants, but he must visit each location exactly once. What is the shortest distance he can travel to achieve this?

For example, given the following distances:

London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141

The possible routes are therefore:

Dublin -> London -> Belfast = 982
London -> Dublin -> Belfast = 605
London -> Belfast -> Dublin = 659
Dublin -> Belfast -> London = 659
Belfast -> Dublin -> London = 605
Belfast -> London -> Dublin = 982

The shortest of these is London -> Dublin -> Belfast = 605, and so the answer is 605 in this example.

What is the distance of the shortest route?

--- Part Two ---

The next year, just to show off, Santa decides to take the route with the longest distance instead.

He can still start and end at any two (different) locations he wants, and he still must visit each location exactly once.

For example, given the distances above, the longest route would be 982 via (for example) Dublin -> London -> Belfast.

What is the distance of the longest route?
"""
import time
import itertools
from collections import defaultdict

def calculate_route_distances(cities: list[str], distances: dict[str, dict[str, int]]) -> list[int]:
    """
    Copmputes all possible route distances for the given cities

    Args:
        cities (list[str]): list of city names
        distance (dict[str, dict[str, int]]):
            A dictionary mapping city pairs to their distances

    Returns:
        list[int]: list of distances for all possible routes
    """
    route_distances: list[int] = []

    for route in itertools.permutations(cities): # O(8!) = 40320 possible routes
        total_distance = 0

        for i in range(len(route) - 1):
            city_a, city_b = route[i], route[i + 1]
            total_distance += distances[city_a][city_b]

        route_distances.append(total_distance)

    return route_distances
    # return [sum(distances[route[i]][route[i + 1]] for i in range(len(route) - 1)) for route in itertools.permutations(cities)]

def parse_input_file(filename: str) -> tuple[list[str], dict[str, dict[str, int]]]:
    """
    Reads the input file and constructs a distance mapping

    Args:
        filename (str): Path to the input file constaining city distances

    Returns:
        tuple[list[str], dict[str, dict[str, int]]]:
            A list of cities and a nested dictionary mapping city pairs to their distances
    """
    distances: dict[str, dict[str, int]] = defaultdict(dict)
    cities: set[str] = set()

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            connection, distance = line.strip().split(" = ")
            city1, city2 = connection.split(" to ")

            cities.update([city1, city2])
            distances[city1][city2] = distances[city2][city1] = int(distance)

    return list(cities), distances

def held_karp(cities: list[str], distances: dict[str, dict[str, int]], find_min: bool = True) -> int:
    """
    Solves the Traveling Salesman Problem using the Held-Karp algorithm

    Args:
        cities (list[str]): list of city names
        distances (dict[str, dict[str, int]]): A dictionary mapping city pairs to their distances
        find_min (bool): If True, finds the shortest route; if False, finds the longest route

    Returns:
        int: total distance of the optimal route
    """
    n = len(cities)

    # dp[(subset_mask, end_city)] = shortest distance to reach that subset ending at end_city
    dp: dict[tuple[int, int], float] = {}

    # Initialize: only one city visited - base case
    for i in range(n):
        dp[(1 << i, i)] = 0  # Starting from city i, distance is 0

    def get_initial_value() -> float:
        return float("inf") if find_min else float("-inf")

    def update_best(best: float, new_dist: float) -> float:
        return min(best, new_dist) if find_min else max(best, new_dist)

    # Iterate over subsets of increasing size
    for subset_size in range(2, n + 1):
        for subset in itertools.combinations(range(n), subset_size):
            mask = sum(1 << i for i in subset)
            for end in subset:
                prev_mask = mask ^ (1 << end)
                best = get_initial_value()

                for k in subset:
                    if k == end:
                        continue
                    prev_dist = dp.get((prev_mask, k), get_initial_value())
                    step_dist = distances[cities[k]][cities[end]]
                    best = update_best(best, prev_dist + step_dist)

                dp[(mask, end)] = best

    # Close the loop: find shortest path visiting all cities
    full_mask = (1 << n) - 1
    final_dists = [dp[(full_mask, j)] for j in range(n)]
    return int(min(final_dists)) if find_min else int(max(final_dists))

def main():
    """
    Main function to execute the solution for Day 9 of Advent of Code 2015
    """
    filename = "day9.txt"

    start = time.perf_counter()
    cities, destination = parse_input_file(filename)
    route_distances = calculate_route_distances(cities, destination)

    print(f"Part 1: {min(route_distances)}")
    print(f"Part 2: {max(route_distances)}")
    brute_time = time.perf_counter() - start

    start = time.perf_counter()
    print(f"Part 1 (Held-Karp): {held_karp(cities, destination)}")
    short_time = time.perf_counter() - start

    start = time.perf_counter()
    print(f"Part 2 (Held-Karp): {held_karp(cities, destination, False)}")
    long_time = time.perf_counter() - start

    print(f"All times: brute={brute_time:.4f}s, short={short_time:.4f}s, long={long_time:.4f}s")

if __name__ == "__main__":
    main()
