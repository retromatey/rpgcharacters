"""
Basic Fantasy race definitions and racial rule modifiers.

This module defines the supported races along with ability score restrictions,
allowed classes, saving throw modifiers, and racial hit-die limits used during
character generation.
"""

from __future__ import annotations

from typing import Final, Literal, TypedDict

from rpgcharacters.classes import AbilityName, ClassName, SavingThrowName

RaceName = Literal["dwarf", "elf", "halfling", "human"]
"""Canonical lowercase identifiers for supported character races."""


class RaceData(TypedDict):
    """Structured rule data describing racial modifiers and restrictions.

    Attributes:
        ability_min: Minimum ability score requirements for the race.
        ability_max: Maximum ability score limits for the race.
        allowed_classes: Classes available to the race.
        saving_throw_modifiers: Racial adjustments applied to saving throws.
        hit_die_max: Optional cap on the class hit die size.
    """

    ability_min: dict[AbilityName, int]  # e.g. {"CON": 9}
    ability_max: dict[AbilityName, int]  # e.g. {"CHA": 17}
    allowed_classes: list[ClassName]
    saving_throw_modifiers: dict[SavingThrowName, int]  # e.g. {"magic_wands": -4}
    hit_die_max: int | None


RACES: Final[dict[RaceName, RaceData]] = {
    "dwarf": {
        "ability_min": {
            "CON": 9,
        },
        "ability_max": {
            "CHA": 17,
        },
        "allowed_classes": [
            "cleric",
            "fighter",
            "thief",
        ],
        "saving_throw_modifiers": {
            # Negative values improve saving throws (lower is better)
            "death_ray_or_poison": -4,
            "magic_wands": -4,
            "paralysis_or_petrify": -4,
            "dragon_breath": -3,
            "spells": -4,
        },
        "hit_die_max": None,
    },

    "elf": {
        "ability_min": {
            "INT": 9,
        },
        "ability_max": {
            "CON": 17,
        },
        "allowed_classes": [
            "cleric",
            "fighter",
            "magic-user",
            "thief",
        ],
        "saving_throw_modifiers": {
            # Negative values improve saving throws (lower is better)
            "magic_wands": -2,
            "paralysis_or_petrify": -1,
            "spells": -2,
        },
        "hit_die_max": 6,
    },

    "halfling": {
        "ability_min": {
            "DEX": 9,
        },
        "ability_max": {
            "STR": 17,
        },
        "allowed_classes": [
            "cleric",
            "fighter",
            "thief",
        ],
        "saving_throw_modifiers": {
            # Negative values improve saving throws (lower is better)
            "death_ray_or_poison": -4,
            "magic_wands": -4,
            "paralysis_or_petrify": -4,
            "dragon_breath": -3,
            "spells": -4,
        },
        "hit_die_max": 6,
    },

    "human": {
        "ability_min": {},
        "ability_max": {},
        "allowed_classes": [
            "cleric",
            "fighter",
            "magic-user",
            "thief",
        ],
        "saving_throw_modifiers": {},
        "hit_die_max": None,
    },
}
