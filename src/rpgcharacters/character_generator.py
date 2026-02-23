from dataclasses import dataclass, fields
from typing import Dict, List, Optional, Protocol
from diceroller.core import DiceRoller

# --- Constants ---

ABILITY_ROLL = "3d6"
STARTING_MONEY_ROLL = "3d6"
ABILITY_ROLL_ORDER = ("STR", "DEX", "CON", "INT", "WIS", "CHA")
ABILITY_MOD_TABLE = (
    (3,   3, -3),
    (4,   5, -2),
    (6,   8, -1),
    (9,  12,  0),
    (13, 15,  1),
    (16, 17,  2),
    (18, 18,  3),
)

# --- Domain Models ---

@dataclass
class AbilityScores:
    CHA: int
    CON: int
    DEX: int
    INT: int
    STR: int
    WIS: int


@dataclass
class Character:
    abilities: AbilityScores
    ability_mods: Dict[str, int]
    ac: int
    attack_bonus: int
    class_name: str
    hp: int
    inventory: List[str]
    level: int
    money_gp: int
    name: Optional[str]
    race: str
    saving_throws: Dict[str, int]


# --- Ability Logic ---

def ability_modifier(score: int) -> int:
    """
    Return the ability bonus/penalty according to ABILITY_MOD_TABLE table.
    """
    for low, high, mod in ABILITY_MOD_TABLE:
        if low <= score <= high:
            return mod
    raise ValueError("Ability score must be between 3 and 18.")

def roll_abilities(rng: DiceRoller) -> AbilityScores:
    """
    Roll 3d6 in order for STR, DEX, CON, INT, WIS, CHA.
    """
    rolled = {name: rng.roll(ABILITY_ROLL) for name in ABILITY_ROLL_ORDER}
    return AbilityScores(**rolled)

def calculate_ability_modifiers(abilities: AbilityScores) -> Dict[str, int]:
    """
    Return dictionary mapping ability names to modifiers.
    """
    return {
        field.name: ability_modifier(getattr(abilities, field.name))
        for field in fields(AbilityScores)
    }


## --- Validation ---

def validate_race(abilities: AbilityScores, race: str) -> List[str]:
    """
    Validate racial ability requirements.
    Return list of validation error messages (empty if valid).
    """
    raise NotImplementedError("validate_race not implemented.")


def validate_class(abilities: AbilityScores, race: str, class_name: str) -> List[str]:
    """
    Validate class prime requisite and race/class compatibility.
    Return list of validation error messages (empty if valid).
    """
    raise NotImplementedError("validate_class not implemented.")


## --- Derived Stats ---
#
#def roll_hit_points(class_name: str, con_modifier: int, rng: DiceRoller) -> int:
#    """
#    Roll class hit die and apply CON modifier.
#    """
#    raise NotImplementedError("roll_hit_points not implemented.")
#
#
#def calculate_armor_class(dex_modifier: int) -> int:
#    """
#    Calculate AC for level 1 character with no armor or shield.
#    Base 11 + DEX modifier.
#    """
#    raise NotImplementedError("calculate_armor_class not implemented.")
#
#
#def starting_money(rng: DiceRoller) -> int:
#    """
#    Roll 3d6 * 10 to determine starting gold pieces.
#    """
#    raise NotImplementedError("starting_money not implemented.")
#
#
#def level_one_attack_bonus() -> int:
#    """
#    Return attack bonus for level 1 character.
#    """
#    raise NotImplementedError("level_one_attack_bonus not implemented.")
#
#
#def calculate_saving_throws(class_name: str, race: str) -> Dict[str, int]:
#    """
#    Return saving throws for level 1 character,
#    applying racial bonuses.
#    """
#    raise NotImplementedError("calculate_saving_throws not implemented.")
#
#
## --- Character Factory ---
#
#def generate_character(
#    race: str,
#    class_name: str,
#    rng: DiceRoller,
#    name: Optional[str] = None,
#) -> Character:
#    """
#    Generate a complete level 1 character using roll-first flow:
#
#    1. Roll abilities
#    2. Validate race
#    3. Validate class
#    4. Roll HP
#    5. Calculate AC
#    6. Set attack bonus
#    7. Calculate saving throws
#    8. Roll starting money
#    9. Return Character object
#    """
#    raise NotImplementedError("generate_character not implemented.")
