from dataclasses import dataclass, field

@dataclass(frozen=True)  # Make object immutable and hashable
class Spell:
    """
    Represents a spell with its properties
    """
    name: str
    cost: int
    damage: int = 0
    heal: int = 0
    armor: int = 0
    mana: int = 0
    duration: int = 0

@dataclass  # Shortcut for creating classes with init, repr, etc.
class Effect:
    """
    Represents an active effect of a spell
    """
    spell: Spell
    timer: int

@dataclass
class GameState:
    """
    Represents the state of the game at any point
    """
    player_hp: int
    player_mana: int
    boss_hp: int
    boss_damage: int
    armor: int = 0
    mana_spent: int = 0
    effects: list[Effect] = field(default_factory=list)  # Every instance of the class gets its own list
    hard_mode: bool = False
    player_turn: bool = True

SPELLS = {
    "Magic Missile": Spell("Magic Missile", cost=53, damage=4),
    "Drain": Spell("Drain", cost=73, damage=2, heal=2),
    "Shield": Spell("Shield", cost=113, armor=7, duration=6),
    "Poison": Spell("Poison", cost=173, damage=3, duration=6),
    "Recharge": Spell("Recharge", cost=229, mana=101, duration=5),
}

def apply_effects(state: GameState) -> None:
    """
    Apply active effects to the game state

    Args:
        state (GameState): The current game state to modify

    Returns:
        None
    """
    state.armor = 0
    new_effects: list[Effect] = []

    for effect in state.effects:
        spell = effect.spell
        if spell.damage:
            state.boss_hp -= spell.damage
        if spell.mana:
            state.player_mana += spell.mana
        if spell.armor:
            state.armor = spell.armor
        effect.timer -= 1
        if effect.timer > 0:
            new_effects.append(effect)
    state.effects = new_effects

def is_spell_active(state: GameState, spell_name: str) -> bool:
    """
    Check if a spell is currently active

    Args:
        state (GameState): The current game state
        spell_name (str): The name of the spell to check

    Returns:
        bool: True if the spell is active, False otherwise
    """
    return any(effect.spell.name == spell_name for effect in state.effects)

def handle_player_turn(state: GameState) -> list[GameState]:
    """
    Handle the player's turn by generating all possible next states

    Args:
        state (GameState): The current game state

    Returns:
        list[GameState]: A list of possible next game states
    """
    if state.hard_mode:
        state.player_hp -= 1
        if state.player_hp <= 0:
            return []

    apply_effects(state)
    if state.boss_hp <= 0:
        return [state]

    next_states: list[GameState] = []
    for spell in SPELLS.values():
        if spell.cost > state.player_mana:
            continue
        if spell.duration > 0 and is_spell_active(state, spell.name):
            continue

        new_state = GameState(
            player_hp=state.player_hp,
            player_mana=state.player_mana - spell.cost,
            boss_hp=state.boss_hp,
            boss_damage=state.boss_damage,
            armor=state.armor,
            mana_spent=state.mana_spent + spell.cost,
            effects=[Effect(effect.spell, effect.timer) for effect in state.effects],
            hard_mode=state.hard_mode,
            player_turn=False
            )

        if spell.duration > 0:
            new_state.effects.append(Effect(spell, spell.duration))
        else:
            new_state.boss_hp -= spell.damage
            new_state.player_hp += spell.heal
        next_states.append(new_state)
    return next_states

def handle_boss_turn(state: GameState) -> list[GameState]:
    """
    Handle the boss's turn and return the new game state

    Args:
        state (GameState): The current game state

    Returns:
        list[GameState]: A list containing the next game state or empty if the player loses
    """
    apply_effects(state)
    if state.boss_hp <= 0:
        return [state]

    damage = max(1, state.boss_damage - state.armor)
    state.player_hp -= damage
    if state.player_hp <= 0:
        return []

    state.player_turn = True
    return [state]

def simulate(state: GameState, best_mana: float) -> float:
    """
    Simulate the game recursively to find the minimum mana to win

    Args:
        state (GameState): The current game state
        best_mana (float): The best mana found so far

    Returns:
        float: The updated best mana found
    """
    if state.mana_spent >= best_mana:
        return best_mana

    if state.boss_hp <= 0:
        return min(best_mana, state.mana_spent)

    next_states = (
        handle_player_turn(state) if state.player_turn
        else handle_boss_turn(state)
        )

    for next_state in next_states:
        best_mana = simulate(next_state, best_mana)
    return best_mana

def find_min_mana_to_win(boss_hp: int, boss_damage: int, hard_mode: bool = False) -> float:
    """
    Find the minimum mana required for the player to defeat the boss

    Args:
        boss_hp (int): The boss's hit points
        boss_damage (int): The boss's damage per attack
        hard_mode (bool): Whether to play in hard mode

    Returns:
        float: The minimum mana required to win
    """
    initial_state = GameState(
        player_hp=50,
        player_mana=500,
        boss_hp=boss_hp,
        boss_damage=boss_damage,
        hard_mode=hard_mode
        )
    return simulate(initial_state, best_mana=float("inf"))

def main():
    """
    Main function to execute the game simulation
    """
    boss_hp, boss_damage = 55, 8  # Puzzle input

    print(f"Part 1: {find_min_mana_to_win(boss_hp, boss_damage)}")
    print(f"Part 2: {find_min_mana_to_win(boss_hp, boss_damage, hard_mode=True)}")

if __name__ == "__main__":
    main()
