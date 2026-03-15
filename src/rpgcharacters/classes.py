"""
Basic Fantasy class definitions and level-1 rules data.

This module defines the supported character classes along with their prime
requisites, minimum ability requirements, hit dice, and base saving throws used
during character generation.
"""

from __future__ import annotations

from typing import Final, Literal, TypedDict

ClassName = Literal["cleric", "fighter", "magic-user", "thief"]
"""Canonical lowercase identifiers for supported character classes."""

AbilityName = Literal["CHA", "CON", "DEX", "INT", "STR", "WIS"]
"""Ability score identifiers used throughout the rules system."""

SavingThrowName = Literal[
    "death_ray_or_poison",
    "magic_wands",
    "paralysis_or_petrify",
    "dragon_breath",
    "spells",
]
"""Names of saving throw categories used by Basic Fantasy."""


class ClassData(TypedDict):
    """Structured rule data describing a character class.

    Attributes:
        prime_requisite: Ability score required for the class.
        min_prime: Minimum value required for the prime requisite.
        hit_die: Hit die size used to roll level-1 hit points.
        saving_throws: Base level-1 saving throw values for the class.
    """

    prime_requisite: AbilityName
    min_prime: int
    hit_die: int
    saving_throws: dict[SavingThrowName, int]  # e.g. {"spells": 15}


CLASSES: Final[dict[ClassName, ClassData]] = {
    "cleric": {
        "prime_requisite": "WIS",
        "min_prime": 9,
        "hit_die": 6,
        "saving_throws": {
            "death_ray_or_poison": 11,
            "magic_wands": 12,
            "paralysis_or_petrify": 14,
            "dragon_breath": 16,
            "spells": 15,
        },
    },
    "fighter": {
        "prime_requisite": "STR",
        "min_prime": 9,
        "hit_die": 8,
        "saving_throws": {
            "death_ray_or_poison": 12,
            "magic_wands": 13,
            "paralysis_or_petrify": 14,
            "dragon_breath": 15,
            "spells": 17,
        },
    },
    "magic-user": {
        "prime_requisite": "INT",
        "min_prime": 9,
        "hit_die": 4,
        "saving_throws": {
            "death_ray_or_poison": 13,
            "magic_wands": 14,
            "paralysis_or_petrify": 13,
            "dragon_breath": 16,
            "spells": 15,
        },
    },
    "thief": {
        "prime_requisite": "DEX",
        "min_prime": 9,
        "hit_die": 4,
        "saving_throws": {
            "death_ray_or_poison": 13,
            "magic_wands": 14,
            "paralysis_or_petrify": 13,
            "dragon_breath": 16,
            "spells": 15,
        },
    },
}
