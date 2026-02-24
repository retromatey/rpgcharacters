import argparse
import json
import random
import sys
from typing import List, Optional

from diceroller.core import CustomRandom, DiceRoller

from rpgcharacters.character_generator import (
    ABILITY_ROLL_ORDER,
    AbilityScores,
    Character,
    calculate_ability_modifiers,
    generate_character,
    roll_abilities,
    valid_classes_for_race,
    valid_races_for_abilities,
    validate_class,
    validate_race,
)


class RestartFlow(Exception):
    pass


class SeededRandom(CustomRandom):
    def __init__(self, seed: int):
        self._rnd = random.Random(seed)

    def randint(self, start: int, end: int) -> int:
        return self._rnd.randint(start, end)


def create_dice_roller(seed: Optional[int]) -> DiceRoller:
    if seed is None:
        return DiceRoller()
    return DiceRoller(SeededRandom(seed))


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

        if prompt_yes_no("Accept these rolls? (y/n): "):
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
    return select_from_list(races, f"Choose a race [1-{len(races)}]: ")


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
    return select_from_list(classes, f"Choose a class [1-{len(classes)}]: ")


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
    for saving_throw in sorted(character.saving_throws):
        display = format_saving_throw_name(saving_throw)
        value = character.saving_throws[saving_throw]
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="rpgcharacters",
        description="Basic Fantasy Character Generator CLI",
    )
    parser.add_argument("--race", help="Specify character race.")
    parser.add_argument(
        "--class",
        dest="class_name",
        help="Specify character class.",
    )
    parser.add_argument("--name", help="Specify character name.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print character JSON to stdout.",
    )
    parser.add_argument(
        "--output",
        help="Write character JSON to FILE (non-interactive mode only).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Use deterministic seed for random generation.",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run in non-interactive mode.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed execution steps (non-interactive mode only).",
    )
    return parser.parse_args()


def should_use_noninteractive(args: argparse.Namespace) -> bool:
    return any(
        [
            args.non_interactive,
            args.race is not None,
            args.class_name is not None,
            args.json,
            args.output is not None,
            args.seed is not None,
            args.verbose,
        ]
    )


def run_interactive(args: argparse.Namespace, rng: DiceRoller) -> None:
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
            if args.json:
                print(json.dumps(character.to_dict(), indent=2))
                print()
            else:
                maybe_save_json(character)
            if not prompt_yes_no("Generate another character? (y/n): "):
                break
        except RestartFlow:
            continue
        except ValueError as exc:
            print(str(exc))
            print()
            continue


def verbose_print(message: str, args: argparse.Namespace) -> None:
    if args.verbose:
        print(f"[verbose] {message}")


def exit_with_error(message: str, args: argparse.Namespace) -> None:
    prefix = "[verbose] " if args.verbose else ""
    print(f"{prefix}{message}", file=sys.stderr)
    sys.exit(2)


def resolve_race(args: argparse.Namespace, abilities: AbilityScores) -> str:
    candidate = args.race.lower() if args.race else None
    valid = sorted(valid_races_for_abilities(abilities))
    if candidate:
        errors = validate_race(abilities, candidate)
        if errors:
            exit_with_error("; ".join(errors), args)
        return candidate
    if not valid:
        exit_with_error("No valid races available for these ability scores.", args)
    selection = valid[0]
    verbose_print(f"Auto-selected race: {selection}", args)
    return selection


def resolve_class(args: argparse.Namespace, abilities: AbilityScores, race: str) -> str:
    candidate = args.class_name.lower() if args.class_name else None
    valid = sorted(valid_classes_for_race(abilities, race))
    if candidate:
        errors = validate_class(abilities, race, candidate)
        if errors:
            exit_with_error("; ".join(errors), args)
        return candidate
    if not valid:
        exit_with_error("No valid classes available for this race.", args)
    selection = valid[0]
    verbose_print(f"Auto-selected class: {selection}", args)
    return selection


def format_verbose_abilities(abilities: AbilityScores) -> str:
    return ", ".join(
        f"{ability}={getattr(abilities, ability)}" for ability in ABILITY_ROLL_ORDER
    )


def run_noninteractive(args: argparse.Namespace, rng: DiceRoller) -> None:
    if args.verbose and args.seed is not None:
        verbose_print(f"Using seed: {args.seed}", args)
    verbose_print("Rolling abilities...", args)
    abilities = roll_abilities(rng)
    if args.verbose:
        print(f"[verbose] Abilities: {format_verbose_abilities(abilities)}")

    race = resolve_race(args, abilities)
    class_name = resolve_class(args, abilities, race)

    character = generate_character(
        race=race,
        class_name=class_name,
        rng=rng,
        name=args.name,
        abilities=abilities,
    )

    payload = json.dumps(character.to_dict(), indent=2)
    if args.output:
        verbose_print(f"Writing JSON to ./{args.output}", args)
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(payload)
    else:
        print(payload)


def main() -> None:
    args = parse_args()
    rng = create_dice_roller(args.seed)
    if should_use_noninteractive(args):
        run_noninteractive(args, rng)
        return
    run_interactive(args, rng)


if __name__ == "__main__":
    main()
