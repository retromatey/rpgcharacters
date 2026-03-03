from dataclasses import dataclass, fields
from typing import Any, cast

from diceroller.core import DiceRoller

from rpgcharacters.classes import CLASSES, ClassName
from rpgcharacters.equipment import ARMOR, ArmorName
from rpgcharacters.races import RACES, RaceName

# --- Constants ---

ABILITY_ROLL = "3d6"
STARTING_MONEY_ROLL = "3d6"
ABILITY_ROLL_ORDER = ("CHA", "CON", "DEX", "INT", "STR", "WIS")
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
    ability_mods: dict[str, int]
    ac: int
    attack_bonus: int
    class_name: str
    hp: int
    inventory: list[str]
    level: int
    money_gp: int
    name: str | None
    race: str
    saving_throws: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "race": self.race,
            "class": self.class_name,
            "level": self.level,
            "abilities": vars(self.abilities),
            "ability_mods": self.ability_mods,
            "hp": self.hp,
            "ac": self.ac,
            "attack_bonus": self.attack_bonus,
            "saving_throws": self.saving_throws,
            "money_gp": self.money_gp,
            "inventory": self.inventory,
        }


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

def calculate_ability_modifiers(abilities: AbilityScores) -> dict[str, int]:
    """
    Return dictionary mapping ability names to modifiers.
    """
    return {
        field.name: ability_modifier(getattr(abilities, field.name))
        for field in fields(AbilityScores)
    }


## --- Validation ---

def validate_race(abilities: AbilityScores, race: str) -> list[str]:
    """
    Validate racial ability requirements.
    Return list of validation error messages (empty if valid).
    """
    errors: list[str] = []

    # TODO: refactor this block into a helper function
    normalized_race = race.lower()
    if normalized_race not in RACES:
        errors.append(f"Unknown race: '{normalized_race}'")
        return errors
    race_key = cast(RaceName, normalized_race)
    race_data = RACES[race_key]

    ability_min = race_data["ability_min"]
    ability_max = race_data["ability_max"]

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


def validate_class(abilities: AbilityScores, race: str, class_name: str) -> list[str]:
    """
    Validate class prime requisite and race/class compatibility.
    Return list of validation error messages (empty if valid).
    """
    errors: list[str] = []

    # TODO: refactor this block into a helper function
    normalized_race = race.lower()
    if normalized_race not in RACES:
        errors.append(f"Unknown race '{normalized_race}'.")
    race_key = cast(RaceName, normalized_race)
    race_data = RACES[race_key]

    # TODO: refactor this block into a helper function
    normalized_class = class_name.lower()
    if normalized_class not in CLASSES:
        errors.append(f"Unknown class: '{normalized_class}'")
    class_key = cast(ClassName, normalized_class)
    class_data = CLASSES[class_key]

    if race_data and class_data:
        allowed_classes = race_data["allowed_classes"] or []
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


def valid_races_for_abilities(abilities: AbilityScores) -> list[str]:
    return [
        race for race in RACES
        if not validate_race(abilities, race)
    ]


def valid_classes_for_race(abilities: AbilityScores, race: str) -> list[str]:
    return [
        class_name for class_name in CLASSES
        if not validate_class(abilities, race, class_name)
    ]


# --- Derived Stats ---

def roll_hit_points(class_name: str, race: str, con_modifier: int, rng: DiceRoller) -> int:
    """
    Roll class hit die and apply CON modifier.
    """
    # TODO: refactor this block into a helper function
    normalized_class = class_name.lower()
    if normalized_class not in CLASSES:
        raise ValueError(f"Unknown class: {normalized_class}")
    class_key = cast(ClassName, normalized_class)
    class_data = CLASSES[class_key]

    # TODO: refactor this block into a helper function
    normalized_race = race.lower()
    if normalized_race not in RACES:
        raise ValueError(f"Unknown race: {normalized_race}")
    race_key = cast(RaceName, normalized_race)
    race_data = RACES[race_key]

    hit_die = class_data["hit_die"]
    hit_die_cap = race_data["hit_die_max"]
    dice_type = hit_die
    if hit_die_cap is not None:
        dice_type = min(hit_die, hit_die_cap)

    roll = rng.roll(f"1d{dice_type}")
    return max(1, roll + con_modifier)


def calculate_armor_class(dex_modifier: int) -> int:
    """
    Calculate AC for level 1 character with no armor or shield.
    Base 11 + DEX modifier.
    """
    armor_key = cast(ArmorName, "none")
    armor_data = ARMOR[armor_key]
    return armor_data["base_ac"] + dex_modifier


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


def calculate_saving_throws(class_name: str, race: str) -> dict[str, int]:
    """
    Return saving throws for level 1 character, applying racial modifiers.
    """
    # TODO: refactor this block into a helper function
    normalized_class = class_name.lower()
    if normalized_class not in CLASSES:
        raise ValueError(f"Unknown class: {normalized_class}")
    class_key = cast(ClassName, normalized_class)
    class_data = CLASSES[class_key]

    # TODO: refactor this block into a helper function
    normalized_race = race.lower()
    if normalized_race not in RACES:
        raise ValueError(f"Unknown race: {normalized_race}")
    race_key = cast(RaceName, normalized_race)
    race_data = RACES[race_key]

    base_saves = class_data["saving_throws"]
    modifiers = race_data["saving_throw_modifiers"]
    return {
        name: base_saves[name] + modifiers.get(name, 0)
        for name in base_saves
    }


# --- Character Factory ---

def generate_character(
    race: str,
    class_name: str,
    rng: DiceRoller,
    name: str | None = None,
    abilities: AbilityScores | None = None
) -> Character:
    """
    Generate a complete level 1 character using roll-first flow:

    1. Roll abilities
    2. Validate race
    3. Validate class
    4. Roll HP
    5. Calculate AC
    6. Set attack bonus
    7. Calculate saving throws
    8. Roll starting money
    9. Return Character object
    """
    # 1. Roll abilities
    # abilities = roll_abilities(rng)
    abilities = abilities if abilities is not None else roll_abilities(rng)

    # 2. Validate race
    race_errors = validate_race(abilities, race)
    if race_errors:
        raise ValueError("; ".join(race_errors))

    # 3. Validate class
    class_errors = validate_class(abilities, race, class_name)
    if class_errors:
        raise ValueError("; ".join(class_errors))

    # 4. Ability modifiers
    ability_mods = calculate_ability_modifiers(abilities)

    # 5. Hit points
    hp = roll_hit_points(
        class_name,
        race,
        ability_mods["CON"],
        rng
    )

    # 6. Armor class (no armor at creation)
    ac = calculate_armor_class(ability_mods["DEX"])

    # 7. Attack bonus
    attack_bonus = level_one_attack_bonus()

    # 8. Saving throws
    saving_throws = calculate_saving_throws(class_name, race)

    # 9. Starting money
    money = starting_money(rng)

    # 10. Return Character
    return Character(
        abilities=abilities,
        ability_mods=ability_mods,
        ac=ac,
        attack_bonus=attack_bonus,
        class_name=class_name.lower(),
        hp=hp,
        inventory=[],
        level=1,
        money_gp=money,
        name=name,
        race=race.lower(),
        saving_throws=saving_throws,
    )
