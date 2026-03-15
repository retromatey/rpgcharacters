"""
Character generation logic for Basic Fantasy RPG.

This module implements a roll-first character creation flow including 3d6
ability rolls, race and class validation, hit points, armor class, saving
throws, and starting money.
"""

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
    """Container for the six Basic Fantasy ability scores.

    Attributes:
        CHA: Charisma score.
        CON: Constitution score.
        DEX: Dexterity score.
        INT: Intelligence score.
        STR: Strength score.
        WIS: Wisdom score.
    """

    CHA: int
    CON: int
    DEX: int
    INT: int
    STR: int
    WIS: int


@dataclass
class Character:
    """Represent a fully generated level-1 character.

    The object contains the character's rolled abilities along with all
    derived statistics such as hit points, armor class, attack bonus,
    saving throws, and starting wealth.
    """

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
        """Serialize the character to a JSON-friendly dictionary.

        Returns:
            dict[str, Any]: Character data including abilities, combat values,
                money, and inventory.
        """
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
    """Convert an ability score to its Basic Fantasy modifier.

    Args:
        score (int): Ability score value.

    Returns:
        int: Bonus or penalty for the score.

    Raises:
        ValueError: If ``score`` is outside the supported 3 to 18 range.
    """
    for low, high, mod in ABILITY_MOD_TABLE:
        if low <= score <= high:
            return mod
    raise ValueError("Ability score must be between 3 and 18.")

def roll_abilities(rng: DiceRoller) -> AbilityScores:
    """Roll ability scores using Basic Fantasy's 3d6 method.

    Rolls one ``3d6`` result for each ability in ``ABILITY_ROLL_ORDER``.

    Args:
        rng (DiceRoller): Dice roller used to generate each score.

    Returns:
        AbilityScores: Rolled scores for all six abilities.
    """
    rolled = {name: rng.roll(ABILITY_ROLL) for name in ABILITY_ROLL_ORDER}
    return AbilityScores(**rolled)

def calculate_ability_modifiers(abilities: AbilityScores) -> dict[str, int]:
    """Calculate modifiers for each ability score.

    Args:
        abilities (AbilityScores): Character ability scores.

    Returns:
        dict[str, int]: Mapping from ability name to modifier.
    """
    return {
        field.name: ability_modifier(getattr(abilities, field.name))
        for field in fields(AbilityScores)
    }


# --- Validation ---

def validate_race(abilities: AbilityScores, race: str) -> list[str]:
    """Validate race selection against race ability limits.

    Basic Fantasy races can define minimum and maximum values for specific
    abilities.

    Args:
        abilities (AbilityScores): Rolled or assigned ability scores.
        race (str): Race name to validate.

    Returns:
        list[str]: Validation messages. Empty when the race is valid.
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
    """Validate class choice for race compatibility and prime requisite.

    Basic Fantasy classes require a minimum prime requisite score and may be
    restricted by race.

    Args:
        abilities (AbilityScores): Rolled or assigned ability scores.
        race (str): Character race to check for allowed classes.
        class_name (str): Class name to validate.

    Returns:
        list[str]: Validation messages. Empty when the class is valid.

    Raises:
        KeyError: If ``race`` or ``class_name`` is unknown after normalization.
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
    """List races that satisfy ability-based racial requirements.

    Args:
        abilities (AbilityScores): Ability scores to evaluate.

    Returns:
        list[str]: Race names with no race-validation messages.
    """
    return [
        race for race in RACES
        if not validate_race(abilities, race)
    ]


def valid_classes_for_race(abilities: AbilityScores, race: str) -> list[str]:
    """List classes that are valid for a race and ability scores.

    Args:
        abilities (AbilityScores): Ability scores to evaluate.
        race (str): Race used for class compatibility checks.

    Returns:
        list[str]: Class names with no class-validation messages.
    """
    return [
        class_name for class_name in CLASSES
        if not validate_class(abilities, race, class_name)
    ]


# --- Derived Stats ---

def roll_hit_points(class_name: str, race: str, con_modifier: int, rng: DiceRoller) -> int:
    """Roll level-1 hit points from class hit die and Constitution modifier.

    Basic Fantasy uses class-based hit dice, with racial hit-die caps for some
    races. This function applies the cap (if any), adds the Constitution
    modifier, and enforces a minimum of 1 HP.

    Args:
        class_name (str): Character class.
        race (str): Character race.
        con_modifier (int): Constitution modifier.
        rng (DiceRoller): Dice roller used for the hit die.

    Returns:
        int: Final level-1 hit points, minimum 1.

    Raises:
        ValueError: If ``class_name`` or ``race`` is unknown.
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
    """Calculate base Armor Class before equipment is applied.

    Args:
        dex_modifier (int): Dexterity modifier.

    Returns:
        int: Base AC from "none" armor plus Dexterity modifier.
    """
    armor_key = cast(ArmorName, "none")
    armor_data = ARMOR[armor_key]
    return armor_data["base_ac"] + dex_modifier


def starting_money(rng: DiceRoller) -> int:
    """Roll starting gold using Basic Fantasy's 3d6 x 10 rule.

    Args:
        rng (DiceRoller): Dice roller used for the money roll.

    Returns:
        int: Starting money in gold pieces.
    """
    return rng.roll(STARTING_MONEY_ROLL) * 10


def level_one_attack_bonus() -> int:
    """Return the fixed Basic Fantasy level-1 attack bonus.

    Returns:
        int: Level-1 attack bonus.
    """
    return 1


def calculate_saving_throws(class_name: str, race: str) -> dict[str, int]:
    """Compute level-1 saving throws with racial modifiers.

    Args:
        class_name (str): Character class used for base saves.
        race (str): Character race used for save modifiers.

    Returns:
        dict[str, int]: Saving throw names mapped to adjusted values.

    Raises:
        ValueError: If ``class_name`` or ``race`` is unknown.
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
    """Generate a complete level-1 character from race, class, and dice rolls.

    The flow implements core Basic Fantasy creation steps: 3d6 ability rolling
    (when not provided), race/class eligibility checks, hit points, armor
    class, attack bonus, saving throws, and starting money.

    Args:
        race (str): Selected race name.
        class_name (str): Selected class name.
        rng (DiceRoller): Dice roller used for all random generation.
        name (str | None): Optional character name.
        abilities (AbilityScores | None): Optional pre-rolled ability scores.
            If ``None``, abilities are rolled with ``3d6`` per ability.

    Returns:
        Character: Fully built level-1 character record.

    Raises:
        ValueError: If race or class validation returns any messages.
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
