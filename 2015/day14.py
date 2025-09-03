"""
--- Day 14: Reindeer Olympics ---

This year is the Reindeer Olympics! Reindeer can fly at high speeds, but must rest occasionally to recover their energy. Santa would like to know which of his reindeer is fastest, and so he has them race.

Reindeer can only either be flying (always at their top speed) or resting (not moving at all), and always spend whole seconds in either state.

For example, suppose you have the following Reindeer:

    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.

After one second, Comet has gone 14 km, while Dancer has gone 16 km. After ten seconds, Comet has gone 140 km, while Dancer has gone 160 km. On the eleventh second, Comet begins resting (staying at 140 km), and Dancer continues on for a total distance of 176 km. On the 12th second, both reindeer are resting. They continue to rest until the 138th second, when Comet flies for another ten seconds. On the 174th second, Dancer flies for another 11 seconds.

In this example, after the 1000th second, both reindeer are resting, and Comet is in the lead at 1120 km (poor Dancer has only gotten 1056 km by that point). So, in this situation, Comet would win (if the race ended at 1000 seconds).

Given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds, what distance has the winning reindeer traveled?

--- Part Two ---

Seeing how reindeer move in bursts, Santa decides he's not pleased with the old scoring system.

Instead, at the end of each second, he awards one point to the reindeer currently in the lead. (If there are multiple reindeer tied for the lead, they each get one point.) He keeps the traditional 2503 second time limit, of course, as doing otherwise would be entirely ridiculous.

Given the example reindeer from above, after the first second, Dancer is in the lead and gets one point. He stays in the lead until several seconds into Comet's second burst: after the 140th second, Comet pulls into the lead and gets his first point. Of course, since Dancer had been in the lead for the 139 seconds before that, he has accumulated 139 points by the 140th second.

After the 1000th second, Dancer has accumulated 689 points, while poor Comet, our old champion, only has 312. So, with the new scoring system, Dancer would win (if the race ended at 1000 seconds).

Again given the descriptions of each reindeer (in your puzzle input), after exactly 2503 seconds, how many points does the winning reindeer have?
"""
import re
from itertools import cycle, accumulate
from collections import Counter

def parse_data(filename: str, race_duration: int) -> dict[str, list[int]]:
    """
    Parse the input file and returns cumlative distances for each reindeer over time

    Args:
        filename (str): The name of the input file.
        race_duration (int): The total time

    Returns:
        dict[str, list[int]]: A dictionary where keys are reindeer names and values are lists of cumulative distances
    """
    pattern = re.compile(r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")
    # race_data = defaultdict(list)
    race_data: dict[str, list[int]] = {}

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            match = pattern.match(line)
            if not match:
                continue

            name, speed, fly_time, rest_time = match.groups()
            speed, fly_time, rest_time = map(int, (speed, fly_time, rest_time))
            movement = cycle([speed] * fly_time + [0] * rest_time)  # create repeating pattern
            # distances = []
            # current_distance = 0
            # for _ in range(race_duration):
            #     current_distance += next(movement)
            #     distances.append(current_distance)
            distances = list(accumulate(next(movement) for _ in range(race_duration)))
            race_data[name] = distances
    return race_data

def calculate_distance(race_data: dict[str, list[int]]) -> int:
    """
    Calculate the distance traveled by the reindeer

    Args:
        race_data (dict[str, list[int]]): A dictionary where keys are reindeer names and values are lists of cumulative distances

    Returns:
        int: The maximum distance traveled by any reindeer
    """
    return max(distances[-1] for distances in race_data.values())

def calculate_points(race_data: dict[str, list[int]]) -> int:
    """
    Calculate the most points scored by any reindeer

    Args:
        race_data (dict[str, list[int]]): A dictionary where keys are reindeer names and values are lists of cumulative distances

    Returns:
        int: The maximum points scored by any reindeer
    """
    points: Counter[str] = Counter()
    reindeer_names = list(race_data.keys())

    # for second in zip(*race_data.values()):
    #     leaders = [i for i, distance in enumerate(second) if distance == max(second)]
    #     points.update(leaders)
    # return max(points.values())

    second: tuple[int, ...]  # Ensure second is a tuple of distances
    for second in zip(*race_data.values()):
        for i, distance in enumerate(second):
            if distance == max(second):
                points[reindeer_names[i]] += 1
    return max(points.values())

def calculate_max_points(race_data: dict[str, list[int]]) -> int:
    """
    Calculate the most points scored by any reindeer

    Args:
        race_data (dict[str, list[int]]): A dictionary where keys are reindeer names and values are lists of cumulative distances

    Returns:
        int: The maximum points scored by any reindeer
    """
    points: Counter[str] = Counter()
    total_seconds = len(next(iter(race_data.values())))

    for second in range(total_seconds):
        # Create a dictionary of current distances at this second
        current_distances = {name: distances[second] for name, distances in race_data.items()}

        # Find the leading distance
        max_distance = max(current_distances.values())

        # Award points to all reindeer that are tied for the lead
        for name, distance in current_distances.items():
            if distance == max_distance:
                points[name] += 1
    return max(points.values())

def main():
    """
    Main function to execute the solution for the Reindeer Olympics problem
    """
    filename = "day14.txt"
    race_data = parse_data(filename, 2503)

    print(f"Part 1: {calculate_distance(race_data)}")
    print(f"Part 2: {calculate_points(race_data)}")
    # print(f"Part 2: {calculate_max_points(race_data)}")

if __name__ == "__main__":
    main()
