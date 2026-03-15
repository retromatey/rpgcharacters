"""Define Basic Fantasy races and race-based character constraints."""

from __future__ import annotations

from typing import Final, Literal, TypedDict

from rpgcharacters.classes import ClassName, SavingThrowName

RaceName = Literal["dwarf", "elf", "halfling", "human"]
"""Supported race identifiers."""


class RaceData(TypedDict):
    """Race-based restrictions and modifiers used during character creation."""

    ability_min: dict[str, int]  # e.g. {"CON": 9}
    ability_max: dict[str, int]  # e.g. {"CHA": 17}
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
