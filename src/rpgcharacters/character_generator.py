from dataclasses import dataclass, fields
from typing import Dict, List, Optional, Protocol
from diceroller.core import DiceRoller

from rpgcharacters.classes import CLASSES
from rpgcharacters.races import RACES
from rpgcharacters.equipment import ARMOR

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
    errors: List[str] = []
    normalized_race = race.lower()
    race_data = RACES.get(normalized_race)
    if not race_data:
        errors.append(f"Unknown race '{race}'.")
        return errors

    ability_min = race_data.get("ability_min", {})
    ability_max = race_data.get("ability_max", {})

    for ability, minimum in ability_min.items():
        score = getattr(abilities, ability, None)
        if score is None:
            continue
        if score < minimum:
            errors.append(
                f"{race.title()} requires {ability} >= {minimum}; found {score}."
            )

    for ability, maximum in ability_max.items():
        score = getattr(abilities, ability, None)
        if score is None:
            continue
        if score > maximum:
            errors.append(
                f"{race.title()} limits {ability} to <= {maximum}; found {score}."
            )

    return errors


def validate_class(abilities: AbilityScores, race: str, class_name: str) -> List[str]:
    """
    Validate class prime requisite and race/class compatibility.
    Return list of validation error messages (empty if valid).
    """
    errors: List[str] = []
    normalized_race = race.lower()
    normalized_class = class_name.lower()

    race_data = RACES.get(normalized_race)
    if not race_data:
        errors.append(f"Unknown race '{race}'.")

    class_data = CLASSES.get(normalized_class)
    if not class_data:
        errors.append(f"Unknown class '{class_name}'.")

    if race_data and class_data:
        allowed_classes = race_data.get("allowed_classes", [])
        if normalized_class not in allowed_classes:
            errors.append(
                f"{race.title()} characters cannot be {class_name.title()}s."
            )
        prime = class_data["prime_requisite"]
        min_prime = class_data["min_prime"]
        score = getattr(abilities, prime, None)
        if score is not None and score < min_prime:
            errors.append(
                f"{class_name.title()} requires {prime} >= {min_prime}; found {score}."
            )

    return errors


# --- Derived Stats ---

def roll_hit_points(class_name: str, race: str, con_modifier: int, rng: DiceRoller) -> int:
    """
    Roll class hit die and apply CON modifier.
    """
    normalized_class = class_name.lower()
    class_data = CLASSES.get(normalized_class)
    if not class_data:
        raise ValueError(f"Unknown class '{class_name}'.")

    normalized_race = race.lower()
    race_data = RACES.get(normalized_race, {})
    if not race_data:
        raise ValueError(f"Unknown race '{race}'.")

    hit_die = class_data["hit_die"]
    hit_die_cap = race_data.get("hit_die_max")
    dice_type = hit_die
    if hit_die_cap is not None:
        dice_type = min(hit_die, hit_die_cap)

    roll = rng.roll(f"1d{dice_type}")
    return roll + con_modifier


def calculate_armor_class(dex_modifier: int) -> int:
    """
    Calculate AC for level 1 character with no armor or shield.
    Base 11 + DEX modifier.
    """
    return ARMOR["none"]["base_ac"] + dex_modifier


def starting_money(rng: DiceRoller) -> int:
    """
    Roll 3d6 * 10 to determine starting gold pieces.
    """
    return rng.roll(STARTING_MONEY_ROLL) * 10


def level_one_attack_bonus() -> int:
    """
    Return attack bonus for level 1 character.
    """
    return 1


def calculate_saving_throws(class_name: str, race: str) -> Dict[str, int]:
    """
    Return saving throws for level 1 character, applying racial modifiers.
    """
    normalized_class = class_name.lower()
    class_data = CLASSES.get(normalized_class)
    if not class_data:
        raise ValueError(f"Unknown class '{class_name}'.")

    normalized_race = race.lower()
    race_data = RACES.get(normalized_race, {})
    if not race_data:
        raise ValueError(f"Unknown race '{race}'.")

    base_saves = class_data["saving_throws"]
    modifiers = race_data.get("saving_throw_modifiers", {})
    return {
        name: base_saves[name] + modifiers.get(name, 0)
        for name in base_saves
    }


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
