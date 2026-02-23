import pytest
from dataclasses import fields
from typing import override

from diceroller.core import DiceRoller, CustomRandom
from rpgcharacters.classes import CLASSES
from rpgcharacters.races import RACES
from rpgcharacters.character_generator import (
    ABILITY_ROLL_ORDER,
    AbilityScores,
    ability_modifier,
    calculate_ability_modifiers,
    calculate_armor_class,
    calculate_saving_throws,
    generate_character,
    level_one_attack_bonus,
    roll_abilities,
    roll_hit_points,
    starting_money,
    valid_classes_for_race,
    valid_races_for_abilities,
    validate_class,
    validate_race,
)

class CustomRandomMoc(CustomRandom):
    def __init__(self):
        self.randint_return_value = 0
        self.dice_type = None
        self.randint_seq = []

    def randint_sequence(self, seq: list[int]):
        self.randint_seq = [x for x in seq]
        self.randint_seq.reverse()

    def randint_returns(self, value: int):
        self.randint_return_value = value

    @override
    def randint(self, start: int, end: int) -> int:
        self.dice_type = end
        if len(self.randint_seq) > 0:
            return self.randint_seq.pop()
        else:
            return self.randint_return_value


def make_ability_scores(**overrides):
    base = {field.name: 10 for field in fields(AbilityScores)}
    base.update(overrides)
    return AbilityScores(**base)


# --- Ability Tests ---

def test_ability_modifier_rejects_invalid_low():
    with pytest.raises(ValueError):
        ability_modifier(2)


def test_ability_modifier_rejects_invalid_high():
    with pytest.raises(ValueError):
        ability_modifier(19)


@pytest.mark.parametrize(
    "score,expected",
    [
        ( 3, -3),
        ( 4, -2),
        ( 5, -2),
        ( 6, -1),
        ( 7, -1),
        ( 8, -1),
        ( 9,  0),
        (10,  0),
        (11,  0),
        (12,  0),
        (13,  1),
        (14,  1),
        (15,  1),
        (16,  2),
        (17,  2),
        (18,  3),
    ],
)
def test_ability_modifier_table(score, expected):
    """Verify ability bonus/penalty table matches ABILITY_MOD_TABLE."""
    assert ability_modifier(score) == expected


def test_roll_abilities_returns_six_scores():
    """Roll-first should return six ability scores between 3 and 18."""
    moc = CustomRandomMoc()
    moc.randint_returns(3)
    rng = DiceRoller(moc)
    abilities = roll_abilities(rng)
    rolled_values = [getattr(abilities, field.name) for field in fields(AbilityScores)]
    assert len(rolled_values) == 6
    assert all(3 <= value <= 18 for value in rolled_values)


def test_calculate_ability_modifiers_returns_all_keys():
    """Ensure modifier dictionary includes all six abilities."""
    abilities = AbilityScores(CHA=16, CON=12, DEX=14, INT=10, STR=11, WIS=9)
    modifiers = calculate_ability_modifiers(abilities)
    ability_keys = {field.name for field in fields(AbilityScores)}
    assert set(modifiers) == ability_keys
    for name in ability_keys:
        assert modifiers[name] == ability_modifier(getattr(abilities, name))


# --- Validation Tests ---
@pytest.mark.parametrize(
    "race,field,value",
    [
        ("dwarf",    "CHA", 18),
        ("elf",      "CON", 18),
        ("halfling", "STR", 18),
    ],
)
def test_race_maximum_constraints(race, field, value):
    """Ability scores higher than race allows should produce valiation errors."""
    abilities = make_ability_scores(**{field: value})
    errors = validate_race(abilities, race)
    assert errors, "Expected race validation to reject abilities above the racial maximum."


@pytest.mark.parametrize(
    "race,field,value",
    [
        ("dwarf",      "CON", 8),
        ("elf",        "INT", 8),
        ("halfling",   "DEX", 8),
    ],
)
def test_race_minimum_constraints(race, field, value):
    """Ability scores lower than race allows should produce valiation errors."""
    abilities = make_ability_scores(**{field: value})
    errors = validate_race(abilities, race)
    assert errors, "Expected race validation to reject abilities below the racial minimum."


@pytest.mark.parametrize(
    "class_,field,value",
    [
        ("cleric",    "WIS", 8),
        ("fighter",   "STR", 8),
        ("magic-user","INT", 8),
        ("thief",     "DEX", 8),
    ],
)
def test_class_prime_requisite_min_constraints(class_, field, value):
    """Ability scores lower than class allows should produce valiation errors."""
    abilities = make_ability_scores(**{field: value})
    errors = validate_class(abilities, "human", class_)
    assert errors, "Expected class validation to reject abilities below the prime requisite."


def test_invalid_race_class_combo_returns_error():
    """Invalid race/class combinations should produce validation errors."""
    overrides = {
        "CHA": 12,
        "CON": 12,
        "DEX": 12,
        "INT": 12,
        "STR": 12,
        "WIS": 12,
    }
    # Halflings are not allowed to be magic-users per RACES data.
    abilities = make_ability_scores(**overrides)
    errors = validate_class(abilities, "halfling", "magic-user")
    assert errors, "Expected class validation to reject disallowed race/class combos."


# --- valid_races_for_abilities tests ---

def test_valid_races_all_available_with_neutral_stats():
    """
    With all stats at 10, all races should be valid.
    """
    abilities = AbilityScores(
        STR=10, DEX=10, CON=10,
        INT=10, WIS=10, CHA=10
    )

    races = valid_races_for_abilities(abilities)

    assert set(races) == set(RACES.keys())


def test_valid_races_filters_out_dwarf_when_con_too_low():
    """
    Dwarf requires CON >= 9.
    """
    abilities = AbilityScores(
        STR=10, DEX=10, CON=8,
        INT=10, WIS=10, CHA=10
    )

    races = valid_races_for_abilities(abilities)

    assert "dwarf" not in races
    assert "human" in races


def test_valid_races_filters_out_elf_when_con_too_high():
    """
    Elf requires CON <= 17.
    """
    abilities = AbilityScores(
        STR=10, DEX=10, CON=18,
        INT=10, WIS=10, CHA=10
    )

    races = valid_races_for_abilities(abilities)

    assert "elf" not in races


# --- valid_classes_for_race tests ---

def test_valid_classes_human_all_classes_available():
    """
    Human should be able to choose any class with sufficient prime stats.
    """
    abilities = AbilityScores(
        STR=12, DEX=12, CON=12,
        INT=12, WIS=12, CHA=12
    )

    classes = valid_classes_for_race(abilities, "human")

    assert set(classes) == set(CLASSES.keys())


def test_valid_classes_filters_by_prime_requisite():
    """
    Fighter requires STR >= 9.
    """
    abilities = AbilityScores(
        STR=8, DEX=12, CON=12,
        INT=12, WIS=12, CHA=12
    )

    classes = valid_classes_for_race(abilities, "human")

    assert "fighter" not in classes
    assert "cleric" in classes


def test_valid_classes_respects_race_class_restrictions():
    """
    Dwarf cannot be magic-user.
    """
    abilities = AbilityScores(
        STR=12, DEX=12, CON=12,
        INT=12, WIS=12, CHA=12
    )

    classes = valid_classes_for_race(abilities, "dwarf")

    assert "magic-user" not in classes


def test_valid_classes_returns_empty_if_no_class_valid():
    """
    If all prime requisites fail, no classes should be returned.
    """
    abilities = AbilityScores(
        STR=3, DEX=3, CON=3,
        INT=3, WIS=3, CHA=3
    )

    classes = valid_classes_for_race(abilities, "human")

    assert classes == []


# --- Derived Stat Tests ---

def test_level_one_attack_bonus_is_plus_one():
    """Level 1 characters should have +1 attack bonus."""
    assert level_one_attack_bonus() == 1


def test_calculate_ac_base_11_plus_dex():
    """AC should be 11 + DEX modifier (no armor)."""
    dex_score = 16
    dex_modifier = ability_modifier(dex_score)
    expected_ac = 11 + dex_modifier
    assert calculate_armor_class(dex_modifier) == expected_ac


def test_starting_money_is_multiple_of_10():
    """Starting money should always be multiple of 10."""
    moc = CustomRandomMoc()
    moc.randint_returns(4)  # each die returns 4
    rng = DiceRoller(moc)
    money = starting_money(rng)
    assert money % 10 == 0
    assert 30 <= money <= 180


def test_roll_hit_points_applies_con_modifier():
    """HP should include CON modifier."""
    moc = CustomRandomMoc()
    moc.randint_returns(5)
    rng = DiceRoller(moc)
    con_modifier = 2
    expected_hp = 5 + con_modifier
    hp = roll_hit_points("fighter", "human", con_modifier, rng)
    assert hp == expected_hp


def test_saving_throws_include_race_bonuses():
    """Saving throws must reflect racial bonuses."""
    race_name = "dwarf"
    class_name = "fighter"
    base_saves = CLASSES[class_name]["saving_throws"]
    race_mods = RACES[race_name]["saving_throw_modifiers"]
    expected = {
        save: base_saves[save] + race_mods.get(save, 0)
        for save in base_saves
    }
    assert calculate_saving_throws(class_name, race_name) == expected


def test_roll_hit_points_respects_racial_hit_die_cap():
    """
    Elf fighters should be capped at d6 even though fighters normally use d8.
    """

    # Force die to return 8 (max of d8)
    moc = CustomRandomMoc()
    moc.randint_returns(6)
    rng = DiceRoller(moc)

    con_modifier = 0

    # Fighter normally rolls d8, but elf cap is d6
    hp = roll_hit_points("fighter", "elf", con_modifier, rng)

    # The dice type used must be a d6
    assert moc.dice_type == 6


def test_roll_hit_points_no_racial_cap():
    """
    Human fighters should roll full d8.
    """

    moc = CustomRandomMoc()
    moc.randint_returns(8)
    rng = DiceRoller(moc)

    hp = roll_hit_points("fighter", "human", 0, rng)

    assert hp == 8


def test_roll_hit_points_minimum_one_hp():
    """
    Hit points should never drop below 1 at level 1,
    even with a negative Constitution modifier.
    """

    # Force minimum die roll of 1
    moc = CustomRandomMoc()
    moc.randint_returns(1)
    rng = DiceRoller(moc)

    # Extreme negative CON modifier
    con_modifier = -3

    hp = roll_hit_points("magic-user", "human", con_modifier, rng)

    # 1 - 3 would be -2 without clamp
    assert hp == 1


# --- Factory Test ---

def test_generate_character_integration():
    """
    Integration test for full character generation pipeline.
    Verifies that all derived stats are populated correctly
    and basic invariants hold.
    """

    # Force predictable dice behavior:
    # - Ability rolls: 10 for all six stats
    # - HP roll: 4
    # - Starting money roll (3d6): 9
    moc = CustomRandomMoc()
    moc.randint_sequence([
        5, 4, 1, # CHA 
        5, 4, 1, # CON
        5, 4, 1, # DEX
        5, 4, 1, # INT
        5, 4, 1, # STR
        5, 4, 1, # WIS
        4,       # HP 
        9,       # gp
    ])
    rng = DiceRoller(moc)

    character = generate_character(
        race="human",
        class_name="fighter",
        rng=rng,
        name="Test Character",
    )

    # --- Structural assertions ---
    assert character.name == "Test Character"
    assert character.race == "human"
    assert character.class_name == "fighter"
    assert character.level == 1
    assert character.inventory == []

    # --- Ability assertions ---
    for ability in ABILITY_ROLL_ORDER:
        assert getattr(character.abilities, ability) == 10
        assert character.ability_mods[ability] == 0

    # --- Derived stats ---
    assert character.attack_bonus == 1
    assert character.ac == 11  # base 11 + DEX mod 0
    assert character.hp == 4   # rolled 4 + CON mod 0
    assert character.money_gp == 90  # 9 * 10

    # --- Saving throws ---
    base_saves = CLASSES["fighter"]["saving_throws"]
    assert character.saving_throws == calculate_saving_throws("fighter", "human")
