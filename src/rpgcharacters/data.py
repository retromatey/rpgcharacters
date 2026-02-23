class Race:
    name: str
    restrictions: dict
    saving_throw_bonuses: dict
    special_abilities: list

class Class:
    name: str
    hit_die: int
    prime_requisite: str
    xp_to_next: int
    armor_allowed: list
    weapons_allowed: list
