from __future__ import annotations

from typing import Final, Literal, TypedDict

ClassName = Literal["cleric", "fighter", "magic-user", "thief"]
AbilityName = Literal["CHA", "CON", "DEX", "INT", "STR", "WIS"]
SavingThrowName = Literal[
    "death_ray_or_poison",
    "magic_wands",
    "paralysis_or_petrify",
    "dragon_breath",
    "spells",
]

class ClassData(TypedDict):
    prime_requisite: AbilityName
    min_prime: int
    hit_die: int
    saving_throws: dict[SavingThrowName, int] # e.g. {"spells": 15}

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
