import json
from typing import List, Optional

from diceroller.core import DiceRoller

from rpgcharacters.character_generator import (
    ABILITY_ROLL_ORDER,
    AbilityScores,
    Character,
    calculate_ability_modifiers,
    generate_character,
    roll_abilities,
    valid_classes_for_race,
    valid_races_for_abilities,
)


class RestartFlow(Exception):
    pass


INVALID_SELECTION_MESSAGE = "Invalid selection. Please try again."


def print_header() -> None:
    print("========================================")
    print(" Basic Fantasy Character Generator")
    print("========================================")
    print()


def format_modifier(value: int) -> str:
    return f"{value:+d}"


def run_ability_phase(rng: DiceRoller) -> AbilityScores:
    while True:
        print("Rolling abilities...")
        abilities = roll_abilities(rng)
        modifiers = calculate_ability_modifiers(abilities)

        for ability in ABILITY_ROLL_ORDER:
            score = getattr(abilities, ability)
            modifier = modifiers[ability]
            print(f"{ability}: {score:2d} ({format_modifier(modifier)})")

        selection = prompt_yes_no("Accept these rolls? (y/n): ")
        if selection:
            print()
            return abilities
        print()


def select_from_list(items: List[str], prompt: str) -> str:
    while True:
        choice = input(prompt).strip()
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(items):
                return items[index - 1]
        print(INVALID_SELECTION_MESSAGE)
        print()


def select_race(abilities: AbilityScores) -> str:
    races = valid_races_for_abilities(abilities)
    if not races:
        print("No valid races available for these ability scores.")
        print("Re-rolling abilities...")
        print()
        raise RestartFlow

    races = sorted(races)
    print("Available Races:")
    for idx, race in enumerate(races, start=1):
        print(f"  {idx}) {race.title()}")
    print()
    selection = select_from_list(races, f"Choose a race [1-{len(races)}]: ")
    return selection


def select_class(abilities: AbilityScores, race: str) -> str:
    classes = valid_classes_for_race(abilities, race)
    if not classes:
        print("No valid classes available for this race.")
        print("Returning to ability roll.")
        print()
        raise RestartFlow

    classes = sorted(classes)
    print("Available Classes:")
    for idx, cls in enumerate(classes, start=1):
        print(f"  {idx}) {cls.title()}")
    print()
    selection = select_from_list(classes, f"Choose a class [1-{len(classes)}]: ")
    return selection


def prompt_name() -> Optional[str]:
    name = input("Character name (optional): ").strip()
    return name or None


def print_core_stats(character: Character) -> None:
    print(f"HP: {character.hp}")
    print(f"AC: {character.ac}")
    print(f"Attack Bonus: {character.attack_bonus:+d}")
    print(f"Money: {character.money_gp} gp")
    print()


def print_abilities(character: Character) -> None:
    print("Abilities:")
    for ability in ABILITY_ROLL_ORDER:
        score = getattr(character.abilities, ability)
        mod = character.ability_mods[ability]
        print(f"{ability}: {score:2d} ({format_modifier(mod)})")
    print()


def format_saving_throw_name(name: str) -> str:
    words = name.replace("_", " ").split()
    return " ".join(word.title() if word.lower() != "or" else "or" for word in words)


def print_saving_throws(character: Character) -> None:
    print("Saving Throws:")
    names = sorted(character.saving_throws)
    for name in names:
        display = format_saving_throw_name(name)
        value = character.saving_throws[name]
        print(f"  {display}: {value:2d}")
    print()


def print_character_summary(character: Character) -> None:
    race_title = character.race.title()
    class_title = character.class_name.title()
    header_name = (
        f" {character.name} the {race_title} {class_title} (Level {character.level})"
        if character.name
        else f" {race_title} {class_title} (Level {character.level})"
    )
    print("========================================")
    print(header_name)
    print("========================================")
    print()
    print_core_stats(character)
    print_abilities(character)
    print_saving_throws(character)


def prompt_yes_no(prompt: str) -> bool:
    while True:
        selection = input(prompt).strip().lower()
        if selection == "y":
            return True
        if selection == "n":
            return False
        print(INVALID_SELECTION_MESSAGE)
        print()


def maybe_save_json(character: Character) -> None:
    if not prompt_yes_no("Save character as JSON file? (y/n): "):
        return

    default_name = f"{character.name}.json" if character.name else "character.json"
    filename_prompt = f"Enter filename [{default_name}]: "
    filename = input(filename_prompt).strip() or default_name
    if not filename.endswith(".json"):
        filename += ".json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(character.to_dict(), file, indent=2)

    print(f"Character saved to ./{filename}")
    print()


def main() -> None:
    rng = DiceRoller()
    while True:
        try:
            print_header()
            abilities = run_ability_phase(rng)
            race = select_race(abilities)
            class_name = select_class(abilities, race)
            name = prompt_name()
            character = generate_character(
                race=race,
                class_name=class_name,
                rng=rng,
                name=name,
                abilities=abilities,
            )
            print_character_summary(character)
            maybe_save_json(character)
            if not prompt_yes_no("Generate another character? (y/n): "):
                break
        except RestartFlow:
            continue
        except ValueError as exc:
            print(str(exc))
            print()
            continue


if __name__ == "__main__":
    main()
