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
import itertools
from collections import defaultdict
from typing import Dict, List, Tuple
import time

def calculate_route_distances(cities: List[str], distances: Dict[str, Dict[str, int]]) -> List[int]:
    """
    Copmputes all possible route distances for the given cities

    Args:
        cities (List[str]): List of city names
        distance (Dict[str, Dict[str, int]]):
            A dictionary mapping city pairs to their distances

    Returns:
        List[int]: List of distances for all possible routes
    """
    route_distances = []

    for route in itertools.permutations(cities): # O(8!) = 40320 possible routes
        total_distance = 0

        for i in range(len(route) - 1):
            city_a, city_b = route[i], route[i + 1]
            total_distance += distances[city_a][city_b]

        route_distances.append(total_distance)

    return route_distances
    # return [sum(distances[route[i]][route[i + 1]] for i in range(len(route) - 1)) for route in itertools.permutations(cities)]

def parse_input_file(filename: str) -> Tuple[List[str], Dict[str, Dict[str, int]]]:
    """
    Reads the input file and constructs a distance mapping

    Args:
        filename (str): Path to the input file constaining city distances

    Returns:
        Tuple[List[str], Dict[str, Dict[str, int]]]:
            A list of cities and a nested dictionary mapping city pairs to their distances
    """
    distances = defaultdict(dict)
    cities = set()

    with open(filename, "r") as file:
        for line in file:
            connection, distance = line.strip().split(" = ")
            city1, city2 = connection.split(" to ")

            cities.update([city1, city2])
            distances[city1][city2] = distances[city2][city1] = int(distance)

    return list(cities), distances

def held_karp(cities: List[str], distances: Dict[str, Dict[str, int]], find_min: bool = True) -> int:
    """
    Solves the Traveling Salesman Problem using the Held-Karp algorithm

    Args:
        cities (List[str]): List of city names
        distances (Dict[str, Dict[str, int]]): A dictionary mapping city pairs to their distances
        find_min (bool): If True, finds the shortest route; if False, finds the longest route

    Returns:
        int: total distance of the optimal route
    """
    n = len(cities)
    city_index = {city: idx for idx, city in enumerate(cities)}

    # dp[(subset_mask, end_city)] = shortest distance to reach that subset ending at end_city
    dp = {}

    # Initialize: only one city visited - base case
    for i in range(n):
        dp[(1 << i, i)] = 0  # Starting from city i, distance is 0

    # Iterate over subsets of increasing size
    for subset_size in range(2, n + 1):
        for subset in itertools.combinations(range(n), subset_size):
            mask = sum(1 << i for i in subset)
            for j in subset:
                prev_mask = mask ^ (1 << j)
                min_dist = float('inf')
                best = float('inf') if find_min else float('-inf')

                for k in subset:
                    if k == j:
                        continue
                    city_from = cities[k]
                    city_to = cities[j]
                    prev_dist = dp.get((prev_mask, k), float('inf') if find_min else float('-inf'))
                    step_dist = distances[city_from][city_to]
                    new_dist = prev_dist + step_dist

                    if find_min:
                        best = min(best, new_dist)
                    else:
                        best = max(best, new_dist)

                dp[(mask, j)] = best

    # Close the loop: find shortest path visiting all cities
    full_mask = (1 << n) - 1
    all_final_dists = [dp[(full_mask, j)] for j in range(n)]
    return min(all_final_dists) if find_min else max(all_final_dists)

def main():
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
