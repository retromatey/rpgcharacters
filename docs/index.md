# rpgcharacters

A Python library and CLI for generating **Basic Fantasy RPG** characters.

This project implements the core character creation rules from the Basic Fantasy
tabletop RPG, allowing characters to be generated either interactively in the
terminal or programmatically in Python.

The generator includes:

- 3d6 ability score rolling
- race and class validation
- derived character statistics
- saving throws
- starting money
- deterministic generation using a random seed

The project is useful for:

- generating characters quickly during gameplay
- scripting character creation
- automated testing of character builds
- building additional tools around Basic Fantasy RPG

---

## Quick Example

=== "CLI"

    ```bash
    rpgcharacters --non-interactive --seed 42
    ```

=== "Python"

    ```python
    from diceroller.core import DiceRoller
    from rpgcharacters.character_generator import generate_character

    rng = DiceRoller(seed=42)

    character = generate_character(
        race="human",
        class_name="fighter",
        rng=rng,
        name="Vey Vale",
    )

    print(character.to_dict())
    ```

---

## Features

- Interactive terminal character generator
- Fully scriptable Python API
- Deterministic character generation using `--seed`
- JSON output for easy integration with other tools
- Built-in validation for race and class rules
- Clean Python data models for characters and ability scores

---

## Project Structure

The project is organized into a few core modules:

| Module                | Purpose                            |
|-----------------------|------------------------------------|
| `character_generator` | Core character creation logic      |
| `classes`             | Class rules and level-1 statistics |
| `races`               | Race restrictions and modifiers    |
| `equipment`           | Armor and equipment data           |

See the **API Reference** section for full documentation.

---

## Next Steps

- See **Getting Started** to install the project
- See **CLI Reference** for command line usage
- See **Character Generation** to understand the rules implemented
- See **API Reference** for the Python interface

---

## License

This project is distributed under the **MIT License**.

Basic Fantasy RPG is an open tabletop RPG.  
This project is a fan-made utility and is not affiliated with the original
authors or publishers.
