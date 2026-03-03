from __future__ import annotations

from typing import Final, Literal, TypedDict

ArmorName = Literal["none", "leather", "chain_mail", "plate_mail"]

class ArmorData(TypedDict):
    base_ac: int
    weight: int
    cost_gp: int
    type_: str

ARMOR: Final[dict[ArmorName, ArmorData]] = {
    "none": {
        "base_ac": 11,
        "weight": 0,
        "cost_gp": 0,
        "type_": "none",
    },
    "leather": {
        "base_ac": 13,
        "weight": 15,
        "cost_gp": 20,
        "type_": "light",
    },
    "chain_mail": {
        "base_ac": 15,
        "weight": 40,
        "cost_gp": 60,
        "type_": "metal",
    },
    "plate_mail": {
        "base_ac": 17,
        "weight": 50,
        "cost_gp": 300,
        "type_": "metal",
    },
}

ShieldName = Literal["shield"]

class ShieldData(TypedDict, total=False):
    ac_bonus: int
    weight: int
    cost_gp: int

SHIELDS = {
    "shield": {
        "ac_bonus": 1,
        "weight": 5,
        "cost_gp": 7,
    }
}
