"""
--- Day 21: RPG Simulator 20XX ---

Little Henry Case got a new video game for Christmas. It's an RPG, and he's stuck on a boss. He needs to know what equipment to buy at the shop. He hands you the controller.

In this game, the player (you) and the enemy (the boss) take turns attacking. The player always goes first. Each attack reduces the opponent's hit points by at least 1. The first character at or below 0 hit points loses.

Damage dealt by an attacker each turn is equal to the attacker's damage score minus the defender's armor score. An attacker always does at least 1 damage. So, if the attacker has a damage score of 8, and the defender has an armor score of 3, the defender loses 5 hit points. If the defender had an armor score of 300, the defender would still lose 1 hit point.

Your damage score and armor score both start at zero. They can be increased by buying items in exchange for gold. You start with no items and have as much gold as you need. Your total damage or armor is equal to the sum of those stats from all of your items. You have 100 hit points.

Here is what the item shop is selling:

Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3

You must buy exactly one weapon; no dual-wielding. Armor is optional, but you can't use more than one. You can buy 0-2 rings (at most one for each hand). You must use any items you buy. The shop only has one of each item, so you can't buy, for example, two rings of Damage +3.

For example, suppose you have 8 hit points, 5 damage, and 5 armor, and that the boss has 12 hit points, 7 damage, and 2 armor:

    The player deals 5-2 = 3 damage; the boss goes down to 9 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 6 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 6 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 4 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 3 hit points.
    The boss deals 7-5 = 2 damage; the player goes down to 2 hit points.
    The player deals 5-2 = 3 damage; the boss goes down to 0 hit points.

In this scenario, the player wins! (Barely.)

You have 100 hit points. The boss's actual stats are in your puzzle input. What is the least amount of gold you can spend and still win the fight?

--- Part Two ---

Turns out the shopkeeper is working with the boss, and can persuade you to buy whatever items he wants. The other rules still apply, and he still only has one of each item.

What is the most amount of gold you can spend and still lose the fight?
"""
import itertools
import math
from typing import List, Tuple

def shop_items() -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
    """
    Returns a tuple of lists containing the items available in the shop

    Args:
        None

    Returns:
        Tuple containing three lists:
            - Weapons: List of tuples (cost, damage, armor)
            - Armor: List of tuples (cost, damage, armor)
            - Rings: List of tuples (cost, damage, armor)
    """
    weapons = [
        (8, 4, 0),  # Dagger
        (10, 5, 0), # Shortsword
        (25, 6, 0), # Warhammer
        (40, 7, 0), # Longsword
        (74, 8, 0)  # Greataxe
    ]

    armor = [
        (0, 0, 0),  # No armor
        (13, 0, 1), # Leather
        (31, 0, 2), # Chainmail
        (53, 0, 3), # Splintmail
        (75, 0, 4), # Bandedmail
        (102, 0, 5) # Platemail
    ]

    rings = [
        (0, 0, 0),   # No ring
        (25, 1, 0),  # Damage +1
        (50, 2, 0),  # Damage +2
        (100, 3, 0), # Damage +3
        (20, 0, 1),  # Defense +1
        (40, 0, 2),  # Defense +2
        (80, 0, 3)   # Defense +3
    ]
    return weapons, armor, rings

def fight(player_hp: int, player_damage: int, player_armor: int, boss_hp: int, boss_damage: int, boss_armor: int) -> bool:
    """
    Simulates a fight between the player and the boss - turn based combat

    Args:
        player_hp (int): Player's hit points
        player_damage (int): Player's damage score
        player_armor (int): Player's armor score
        boss_hp (int): Boss's hit points
        boss_damage (int): Boss's damage score
        boss_armor (int): Boss's armor score

    Returns:
        bool: True if the player wins, False if the player loses
    """
    while True:
        boss_hp -= max(player_damage - boss_armor, 1)
        if boss_hp <= 0:
            return True

        player_hp -= max(boss_damage - player_armor, 1)
        if player_hp <= 0:
            return False

def all_loadouts() -> List[Tuple[int, int, int]]:
    """
    Generates all possible loadouts of items from the shop

    Args:
        None

    Returns:
        List[Tuple[int, int, int]]: List of tuples containing (cost, total_damage, total_armor) for each loadout
    """
    weapons, armor, rings = shop_items()

    for weapon_cost, weapon_damage, weapon_armor in weapons:
        for armor_cost, armor_damage, armor_armor in armor:
            for ring1, ring2 in itertools.combinations(rings, 2):
                total_cost = weapon_cost + armor_cost + ring1[0] + ring2[0]
                total_damage = weapon_damage + armor_damage + ring1[1] + ring2[1]
                total_armor = weapon_armor + armor_armor + ring1[2] + ring2[2]
                yield total_cost, total_damage, total_armor

def solve() -> Tuple[int, int]:
    """
    Solves the puzzle by finding the minimum cost to win and maximum cost to lose

    Args:
        None

    Returns:
        Tuple[int, int]: Minimum cost to win, Maximum cost to lose
    """
    boss_hp, boss_damage, boss_armor = 100, 8, 2  # from puzzle input
    min_win_cost = float('inf')
    max_loss_cost = 0

    for cost, damage, armor in all_loadouts():
        player_wins = fight(100, damage, armor, boss_hp, boss_damage, boss_armor)
        if player_wins:
            min_win_cost = min(min_win_cost, cost)
        else:
            max_loss_cost = max(max_loss_cost, cost)
    return min_win_cost, max_loss_cost

def loadouts() -> List[Tuple[int, int, int]]:
    """
    Generates all possible loadouts of items from the shop, including combinations of rings

    Args:
        None

    Returns:
        List[Tuple[int, int, int]]: List of tuples containing (cost, total_damage, total_armor) for each loadout
    """
    weapons, armors, rings = shop_items()
    builds = []

    for weapon in weapons:
        for armor in armors:
            for ring_count in range(3):
                for ring_combination in itertools.combinations(rings, ring_count):
                    total_cost = weapon[0] + armor[0] + sum(ring[0] for ring in ring_combination)
                    total_damage = weapon[1] + armor[1] + sum(ring[1] for ring in ring_combination)
                    total_armor = weapon[2] + armor[2] + sum(ring[2] for ring in ring_combination)
                    builds.append((total_cost, total_damage, total_armor))
    return builds

def player_wins(player_damage: int, player_armor: int, boss_hp: int, boss_damage: int, boss_armor: int) -> bool:
    """
    Math formula: compare how many turns it takes for the player to defeat the boss and vice versa

    Args:
        player_damage (int): Player's damage score
        player_armor (int): Player's armor score
        boss_hp (int): Boss's hit points
        boss_damage (int): Boss's damage score
        boss_armor (int): Boss's armor score

    Returns:
        bool: True if the player wins, False if the player loses
    """
    turns_player = math.ceil(boss_hp / max(player_damage - boss_armor, 1))
    turns_boss = math.ceil(100 / max(boss_damage - player_armor, 1))
    return turns_player <= turns_boss

def solve2() -> Tuple[int, int]:
    """
    Solves the puzzle by finding the minimum cost to win and maximum cost to lose using the loadouts function

    Args:
        None

    Returns:
        Tuple[int, int]: Minimum cost to win, Maximum cost to lose
    """
    boss_hp, boss_damage, boss_armor = 100, 8, 2  # from puzzle input
    builds = loadouts()

    for cost, damage, armor in sorted(builds, key=lambda x: x[0]):
        if player_wins(damage, armor, boss_hp, boss_damage, boss_armor):
            best_price_to_win = cost
            break

    for cost, damage, armor in sorted(builds, key=lambda x: -x[0]):
        if not player_wins(damage, armor, boss_hp, boss_damage, boss_armor):
            worst_price_to_lose = cost
            break
    return best_price_to_win, worst_price_to_lose

def main():
    # part1, part2 = solve()
    # print(f"Part 1: {part1}")
    # print(f"Part 2: {part2}")

    part1, part2 = solve2()
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == "__main__":
    main()
