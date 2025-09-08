"""
--- Day 1: No Time for a Taxicab ---

Santa's sleigh uses a very high-precision clock to guide its movements, and the clock's oscillator is regulated by stars. Unfortunately, the stars have been stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", unfortunately, is as close as you can get - the instructions on the Easter Bunny Recruiting Document the Elves intercepted start here, and nobody had time to work them out further.

The Document indicates that you should start at the given coordinates (where you just landed) and face North. Then, follow the provided sequence: either turn left (L) or right (R) 90 degrees, then walk forward the given number of blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you take a moment and work out the destination. Given that you can only walk on the street grid of the city, how far is the shortest path to the destination?

For example:

    Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
    R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
    R5, L5, R5, R3 leaves you 12 blocks away.

How many blocks away is Easter Bunny HQ?

--- Part Two ---

Then, you notice the instructions continue on the back of the Recruiting Document. Easter Bunny HQ is actually at the first location you visit twice.

For example, if your instructions are R8, R4, R4, R8, the first location you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?
"""
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

def parse_data(filename: str) -> list[tuple[str, int]]:
    """
    Parse the input data from the given filename

    Args:
        filename (str): The name of the file containing the input data

    Returns:
        list[tuple[str, int]]: A list of tuples containing the direction and distance
    """
    with open(filename, "r", encoding="utf-8") as file:
        data = file.read().strip().split(", ")
    return [(d[0], int(d[1:])) for d in data]

def taxicab(directions: list[tuple[str, int]]) -> tuple[int, int]:
    """
    Calculate the distance from the starting point and to the first location that is visited twice

    Args:
        directions (list[tuple[str, int]]): A list of tuples containing the direction and distance

    Returns:
        tuple[int, int]: distance from starting point and the distance to first revisited location
    """
    x, y = 0, 0  # Starting coordinates
    visited = {(x, y)}
    first_revisited = None
    direction_index = 0  # Facing north
    direction_map = [
        (0, 1),  # North
        (1, 0),  # East
        (0, -1),  # South
        (-1, 0),  # West
    ]

    for turn, steps in directions:
        if turn == "R":
            direction_index = (direction_index + 1) % 4
        else:
            direction_index = (direction_index - 1) % 4
        dx, dy = direction_map[direction_index]

        for _ in range(steps):
            x += dx
            y += dy
            if first_revisited is None and (x, y) in visited:
                first_revisited = (x, y)
            visited.add((x, y))
    distance = abs(x) + abs(y)

    if first_revisited:
        revist = abs(first_revisited[0]) + abs(first_revisited[1])
    else:
        revist = -1
    return distance, revist

def animate_path(directions: list[tuple[str, int]], save_as_gif: bool = False, gif_filename: str = "taxicab_path.gif"):
    """
    Animate the path taken based on the directions provided

    Args:
        directions (list[tuple[str, int]]): A list of tuples containing the direction and

    Returns:
        None
    """
    x, y = 0, 0
    direction_index = 0
    direction_map = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = {(0, 0)}
    path = [(0, 0)]
    first_revisit = None

    for turn, steps in directions:
        direction_index = (direction_index + 1) % 4 if turn == "R" else (direction_index - 1) % 4
        dx, dy = direction_map[direction_index]

        for _ in range(steps):
            x += dx
            y += dy
            if first_revisit is None and (x, y) in visited:
                first_revisit = (x, y)
            visited.add((x, y))
            path.append((x, y))

    # Set up the plot
    fig, ax = plt.subplots()
    ax.set_title("Taxicab Path Animation")
    ax.set_xlim(min(p[0] for p in path) - 1, max(p[0] for p in path) + 1)
    ax.set_ylim(min(p[1] for p in path) - 1, max(p[1] for p in path) + 1)
    ax.set_aspect("equal")
    line, = ax.plot([], [], "bo-", lw=2)
    red_dot, = ax.plot([], [], "ro", markersize=8)

    def update(frame):
        trail = path[:frame + 1]
        xs, ys = zip(*trail)
        line.set_data(xs, ys)
        if first_revisit and frame >= path.index(first_revisit):
            red_dot.set_data([first_revisit[0]], [first_revisit[1]])
        return line, red_dot

    ani = animation.FuncAnimation(fig, update, frames=len(path), interval=200, blit=True)
    if save_as_gif:
        print("Processing animation...")
        writer = PillowWriter(fps=5)
        with tqdm(total=len(path), desc="Rendering", ncols=70) as pbar:
            def custom_draw(frame):
                update(frame)
                fig.canvas.draw()
                pbar.update(1)

            for frame in range(len(path)):
                custom_draw(frame)
            ani.save(gif_filename, writer=writer)
        print(f"Animation saved as {gif_filename}")
    else:
        plt.show()

def main():
    """
    Main function to execute the code
    """
    filename = "day1.txt"
    directions = parse_data(filename)

    print(f"Part 1: {taxicab(directions)[0]}")
    print(f"Part 2: {taxicab(directions)[1]}")
    # animate_path(directions, save_as_gif=True)

if __name__ == "__main__":
    main()
