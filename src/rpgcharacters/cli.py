from diceroller.core import DiceRoller
from rpgcharacters.character_generator import generate_character

def main():
    print("Basic Fantasy Character Generator\n")

    race = input("Choose race (human, dwarf, elf, halfling): ").strip().lower()
    class_name = input("Choose class (fighter, cleric, magic-user, thief): ").strip().lower()
    name = input("Character name (optional): ").strip() or None

    rng = DiceRoller()

    try:
        character = generate_character(race, class_name, rng, name)
    except ValueError as e:
        print(f"\nError: {e}")
        return

    # print_character(character)
    print(character)

if __name__ == "__main__":
    main()
