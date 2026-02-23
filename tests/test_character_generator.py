import pytest
from dataclasses import fields
from typing import override

from diceroller.core import DiceRoller, CustomRandom
from rpgcharacters.character_generator import (
    AbilityScores,
    ability_modifier,
    calculate_ability_modifiers,
    #calculate_armor_class,
    #calculate_saving_throws,
    #generate_character,
    #level_one_attack_bonus,
    roll_abilities,
    #roll_hit_points,
    #starting_money,
    validate_class,
    validate_race,
)

class CustomRandomMoc(CustomRandom):
    def __init__(self):
        self.randint_return_value = 0

    def randint_returns(self, value: int):
        self.randint_return_value = value

    @override
    def randint(self, start: int, end: int) -> int:
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


## --- Derived Stat Tests ---
#
#def test_level_one_attack_bonus_is_plus_one():
#    """Level 1 characters should have +1 attack bonus."""
#    raise NotImplementedError
#
#
#def test_calculate_ac_base_11_plus_dex():
#    """AC should be 11 + DEX modifier (no armor)."""
#    raise NotImplementedError
#
#
#def test_starting_money_is_multiple_of_10():
#    """Starting money should always be multiple of 10."""
#    raise NotImplementedError
#
#
#def test_roll_hit_points_applies_con_modifier():
#    """HP should include CON modifier."""
#    raise NotImplementedError
#
#
#def test_saving_throws_include_race_bonuses():
#    """Saving throws must reflect racial bonuses."""
#    raise NotImplementedError
#
#
## --- Factory Test ---
#
#def test_generate_character_returns_valid_character_object():
#    """Full roll-first generation returns valid Character instance."""
#    raise NotImplementedError
