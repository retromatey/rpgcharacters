import pytest
from dataclasses import fields
from typing import override

from diceroller.core import DiceRoller, CustomRandom
from rpgcharacters.character_generator import (
    roll_abilities,
    ability_modifier,
    calculate_ability_modifiers,
    validate_race,
    validate_class,
    roll_hit_points,
    calculate_armor_class,
    starting_money,
    level_one_attack_bonus,
    calculate_saving_throws,
    generate_character,
    AbilityScores,
)

class CustomRandomMoc(CustomRandom):
    def __init__(self):
        self.randint_return_value = 0

    def randint_returns(self, value: int):
        self.randint_return_value = value

    @override
    def randint(self, start: int, end: int) -> int:
        return self.randint_return_value



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


## --- Validation Tests ---
#
#def test_dwarf_requires_con_9_or_higher():
#    """Dwarves must have CON >= 9."""
#    raise NotImplementedError
#
#
#def test_elf_requires_int_9_or_higher():
#    """Elves must have INT >= 9."""
#    raise NotImplementedError
#
#
#def test_magic_user_requires_int_9_or_higher():
#    """Magic-Users must have INT >= 9."""
#    raise NotImplementedError
#
#
#def test_invalid_race_class_combo_returns_error():
#    """Invalid race/class combinations should produce validation errors."""
#    raise NotImplementedError
#
#
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
