"""
Basic Fantasy RPG character generation package.

This package provides tools for generating level-1 characters using Basic
Fantasy rules, including ability rolling, race and class validation, and derived
combat statistics.
"""

from .character_generator import (
    AbilityScores,
    Character,
    generate_character,
    roll_abilities,
)
from .classes import ClassName
from .races import RaceName

__all__ = [
    "AbilityScores",
    "Character",
    "ClassName",
    "RaceName",
    "generate_character",
    "roll_abilities",
]
