"""
--- Day 22: Wizard Simulator 20XX ---

Little Henry Case decides that defeating bosses with swords and stuff is boring. Now he's playing the game with a wizard. Of course, he gets stuck on another boss and needs your help again.

In this version, combat still proceeds with the player and the boss taking alternating turns. The player still goes first. Now, however, you don't get any equipment; instead, you must choose one of your spells to cast. The first character at or below 0 hit points loses.

Since you're a wizard, you don't get to wear armor, and you can't attack normally. However, since you do magic damage, your opponent's armor is ignored, and so the boss effectively has zero armor as well. As before, if armor (from a spell, in this case) would reduce damage below 1, it becomes 1 instead - that is, the boss' attacks always deal at least 1 damage.

On each of your turns, you must select one of your spells to cast. If you cannot afford to cast any spell, you lose. Spells cost mana; you start with 500 mana, but have no maximum limit. You must have enough mana to cast a spell, and its cost is immediately deducted when you cast it. Your spells are Magic Missile, Drain, Shield, Poison, and Recharge.

    Magic Missile costs 53 mana. It instantly does 4 damage.
    Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
    Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
    Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
    Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.

Effects all work the same way. Effects apply at the start of both the player's turns and the boss' turns. Effects are created with a timer (the number of turns they last); at the start of each turn, after they apply any effect they have, their timer is decreased by one. If this decreases the timer to zero, the effect ends. You cannot cast a spell that would start an effect which is already active. However, effects can be started on the same turn they end.

For example, suppose the player has 10 hit points and 250 mana, and that the boss has 13 hit points and 8 damage:

-- Player turn --
- Player has 10 hit points, 0 armor, 250 mana
- Boss has 13 hit points
Player casts Poison.

-- Boss turn --
- Player has 10 hit points, 0 armor, 77 mana
- Boss has 13 hit points
Poison deals 3 damage; its timer is now 5.
Boss attacks for 8 damage.

-- Player turn --
- Player has 2 hit points, 0 armor, 77 mana
- Boss has 10 hit points
Poison deals 3 damage; its timer is now 4.
Player casts Magic Missile, dealing 4 damage.

-- Boss turn --
- Player has 2 hit points, 0 armor, 24 mana
- Boss has 3 hit points
Poison deals 3 damage. This kills the boss, and the player wins.

Now, suppose the same initial conditions, except that the boss has 14 hit points instead:

-- Player turn --
- Player has 10 hit points, 0 armor, 250 mana
- Boss has 14 hit points
Player casts Recharge.

-- Boss turn --
- Player has 10 hit points, 0 armor, 21 mana
- Boss has 14 hit points
Recharge provides 101 mana; its timer is now 4.
Boss attacks for 8 damage!

-- Player turn --
- Player has 2 hit points, 0 armor, 122 mana
- Boss has 14 hit points
Recharge provides 101 mana; its timer is now 3.
Player casts Shield, increasing armor by 7.

-- Boss turn --
- Player has 2 hit points, 7 armor, 110 mana
- Boss has 14 hit points
Shield's timer is now 5.
Recharge provides 101 mana; its timer is now 2.
Boss attacks for 8 - 7 = 1 damage!

-- Player turn --
- Player has 1 hit point, 7 armor, 211 mana
- Boss has 14 hit points
Shield's timer is now 4.
Recharge provides 101 mana; its timer is now 1.
Player casts Drain, dealing 2 damage, and healing 2 hit points.

-- Boss turn --
- Player has 3 hit points, 7 armor, 239 mana
- Boss has 12 hit points
Shield's timer is now 3.
Recharge provides 101 mana; its timer is now 0.
Recharge wears off.
Boss attacks for 8 - 7 = 1 damage!

-- Player turn --
- Player has 2 hit points, 7 armor, 340 mana
- Boss has 12 hit points
Shield's timer is now 2.
Player casts Poison.

-- Boss turn --
- Player has 2 hit points, 7 armor, 167 mana
- Boss has 12 hit points
Shield's timer is now 1.
Poison deals 3 damage; its timer is now 5.
Boss attacks for 8 - 7 = 1 damage!

-- Player turn --
- Player has 1 hit point, 7 armor, 167 mana
- Boss has 9 hit points
Shield's timer is now 0.
Shield wears off, decreasing armor by 7.
Poison deals 3 damage; its timer is now 4.
Player casts Magic Missile, dealing 4 damage.

-- Boss turn --
- Player has 1 hit point, 0 armor, 114 mana
- Boss has 2 hit points
Poison deals 3 damage. This kills the boss, and the player wins.

You start with 50 hit points and 500 mana points. The boss's actual stats are in your puzzle input. What is the least amount of mana you can spend and still win the fight? (Do not include mana recharge effects as "spending" negative mana.)

--- Part Two ---

On the next run through the game, you increase the difficulty to hard.

At the start of each player turn (before any other effects apply), you lose 1 hit point. If this brings you to or below 0 hit points, you lose.

With the same starting stats for you and the boss, what is the least amount of mana you can spend and still win the fight?
"""
import sys
import copy

def get_spells() -> dict[str, dict[str, int]]:
    """
    Returns a dictionary of spells with their properties

    Args:
        None

    Returns:
        dict[str, dict[str, int]]: A dictionary where keys are spell names and values are dictionaries with spell properties
    """
    return {
        "Magic Missile": {"cost": 53, "damage": 4, "heal": 0, "armor": 0, "mana": 0, "duration": 0},
        "Drain": {"cost": 73, "damage": 2, "heal": 2, "armor": 0, "mana": 0, "duration": 0},
        "Shield": {"cost": 113, "damage": 0, "heal": 0, "armor": 7, "mana": 0, "duration": 6},
        "Poison": {"cost": 173, "damage": 3, "heal": 0, "armor": 0, "mana": 0, "duration": 6},
        "Recharge": {"cost": 229, "damage": 0, "heal": 0, "armor": 0, "mana": 101, "duration": 5}
    }

def apply_effect(state: dict[str, int | dict[str, int]], spells: dict[str, dict[str, int]]) -> None:
    """
    Applies the effects of active spells to the game state

    Args:
        state (dict[str, int]): The current game state containing player and boss stats, mana, and active
        spells (dict[str, dict[str, int]]): A dictionary of spells with their properties

    Returns:
        None
    """
    state["armor"] = 0
    expired: list[str] = []

    for name in state["effects"]:
        effect = spells[name]
        if effect["armor"] > 0:
            state["armor"] = effect["armor"]
        if effect["damage"] > 0:
            state["boss_hp"] -= effect["damage"]
        if effect["mana"] > 0:
            state["player_mana"] += effect["mana"]
        state["effects"][name] -= 1
        if state["effects"][name] == 0:
            expired.append(name)

    for name in expired:
        del state["effects"][name]

def can_cast(state: dict[str, int], spell_name: str, spells: dict[str, dict[str, int]]) -> bool:
    """
    Checks if a spell can be cast based on the current game state

    Args:
        state (dict[str, int]): The current game state containing player and boss stats, mana, and active
        spell_name (str): The name of the spell to check
        spells (dict[str, dict[str, int]]): A dictionary of spells with their properties

    Returns:
        bool: True if the spell can be cast, False otherwise
    """
    spell = spells[spell_name]
    is_active = spell_name in state["effects"] and state["effects"][spell_name] > 1
    return state["player_mana"] >= spell["cost"] and not is_active

def simulate(state: dict[str, int], is_player_turn: bool, spells: dict[str, dict[str, int]], best: list[int], hard_mode: bool) -> None:
    """
    Simulates the game state recursively to find the minimum mana spent to win

    Args:
        state (dict[str, int]): The current game state containing player and boss stats, mana, and active
        is_player_turn (bool): True if it's the player's turn, False if it's the boss's turn
        spells (dict[str, dict[str, int]]): A dictionary of spells with their properties
        best (list[int]): A list containing the best (minimum) mana spent found so far
        hard_mode (bool): True if hard mode is enabled, False otherwise

    Returns:
        None
    """
    if state["mana_spend"] >= best[0]:
        return

    if hard_mode and is_player_turn:
        state["player_hp"] -= 1
        if state["player_hp"] <= 0:
            return

    apply_effect(state, spells)
    if state["boss_hp"] <= 0:
        best[0] = min(best[0], state["mana_spend"])
        return

    if is_player_turn:
        for name in spells:
            if not can_cast(state, name, spells):
                continue

            new_state = copy.deepcopy(state)
            spell = spells[name]
            new_state["player_mana"] -= spell["cost"]
            new_state["mana_spend"] += spell["cost"]

            if spell["duration"] > 0:
                new_state["effects"][name] = spell["duration"]
            else:
                new_state["boss_hp"] -= spell["damage"]
                new_state["player_hp"] += spell["heal"]

            if new_state["boss_hp"] <= 0:
                best[0] = min(best[0], new_state["mana_spend"])
            else:
                simulate(new_state, False, spells, best, hard_mode)
    else:
        damage = max(1, state["boss_damage"] - state["armor"])
        state["player_hp"] -= damage
        if state["player_hp"] > 0:
            simulate(state, True, spells, best, hard_mode)

def run_simulation(boss_hp: int, boss_damage: int, hard_mode: bool = False) -> int:
    """
    Runs the wizard simulation with the given boss stats and returns the minimum mana spent to win

    Args:
        boss_hp (int): The hit points of the boss
        boss_damage (int): The damage dealt by the boss
        hard_mode (bool): True if hard mode is enabled, False otherwise

    Returns:
        int: The minimum mana spent to win the fight
    """
    initial_state = {
        "player_hp": 50,
        "player_mana": 500,
        "boss_hp": boss_hp,
        "boss_damage": boss_damage,
        "armor": 0,
        "mana_spend": 0,
        "effects": {}
    }

    best = [sys.maxsize]
    spells = get_spells()
    simulate(initial_state, True, spells, best, hard_mode)
    return best[0]

def main():
    """
    Main function to run the simulation with puzzle input and print results for both parts
    """
    boss_hp, boss_damage = 55, 8 # puzzle input
    print(f"Part 1: {run_simulation(boss_hp, boss_damage)}")
    print(f"Part 2: {run_simulation(boss_hp, boss_damage, hard_mode=True)}")

if __name__ == "__main__":
    main()
