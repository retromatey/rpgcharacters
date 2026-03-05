[![CI](https://github.com/retromatey/rpgcharacters/actions/workflows/ci.yml/badge.svg)](https://github.com/retromatey/rpgcharacters/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/retromatey/rpgcharacters/branch/main/graph/badge.svg)](https://codecov.io/gh/retromatey/rpgcharacters)
[![GitHub release](https://img.shields.io/github/v/release/retromatey/rpgcharacters)](https://github.com/retromatey/rpgcharacters/releases)
![Python](https://img.shields.io/badge/python-3.14+-blue.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

# rpgcharacters

A Python library + CLI for generating **Basic Fantasy RPG** characters
(race/class validation, ability rolls, derived stats, and JSON output).

Supports both interactive character creation and automated generation for
scripting and testing.

---

## What this project does

- Generates a level 1 character for the Basic Fantasy RPG game
- Rolls ability scores and calculates modifiers
- Validates race/class options based on ability requirements
- Computes derived stats (HP, AC, attack bonus, saving throws, starting money)
- Generates a complete character object
- Outputs JSON (stdout or file)
- Supports deterministic generation via `--seed` (nice for testing and “cloning”
  characters)

---

## Quick Start

Generate a random Basic Fantasy RPG character:

```bash
$ rpgcharacters --non-interactive
```

Example output:

```bash
{
  "name": null,
  "race": "human",
  "class": "magic-user",
  "level": 1,
  "abilities": {
    "CHA": 12,
    "CON": 15,
    "DEX": 9,
    "INT": 10,
    "STR": 12,
    "WIS": 7
  },
  "ability_mods": {
    "CHA": 0,
    "CON": 1,
    "DEX": 0,
    "INT": 0,
    "STR": 0,
    "WIS": -1
  },
  "hp": 4,
  "ac": 11,
  "attack_bonus": 1,
  "saving_throws": {
    "death_ray_or_poison": 13,
    "magic_wands": 14,
    "paralysis_or_petrify": 13,
    "dragon_breath": 16,
    "spells": 15
  },
  "money_gp": 80,
  "inventory": []
}
```

---

## Example

```console
$ rpgcharacters --non-interactive --seed 7654321
{
  "name": null,
  "race": "dwarf",
  "class": "fighter",
  "level": 1,
  "abilities": {
    "CHA": 12,
    "CON": 9,
    "DEX": 12,
    "INT": 14,
    "STR": 16,
    "WIS": 11
  },
  "ability_mods": {
    "CHA": 0,
    "CON": 0,
    "DEX": 0,
    "INT": 1,
    "STR": 2,
    "WIS": 0
  },
  "hp": 8,
  "ac": 11,
  "attack_bonus": 1,
  "saving_throws": {
    "death_ray_or_poison": 8,
    "magic_wands": 9,
    "paralysis_or_petrify": 10,
    "dragon_breath": 12,
    "spells": 13
  },
  "money_gp": 70,
  "inventory": []
}
```

---

## How to install

### Install the release build

Install the .whl from latest [release](https://github.com/retromatey/rpgcharacters/releases):
**NOTE**: Replace `v0.1.0` with the latest release version if needed.

```bash
pip install https://github.com/retromatey/rpgcharacters/releases/download/v0.1.0/rpgcharacters-0.1.0-py3-none-any.whl
```

### Clone for development

```bash
git clone https://github.com/retromatey/rpgcharacters.git
cd rpgcharacters
pip install -e .[dev]
```

Run the following commands to check the health of the project:

```bash
ruff check .
mypy src
pytest --cov=rpgcharacters --cov-report=term-missing
python -m build
```

---

## Usage

### CLI

Run the `rpgcharacters --help` command to view options.

```bash
usage: rpgcharacters [-h] [--version] [--race RACE] [--class CLASS_NAME] [--name NAME]
                     [--json] [--output OUTPUT] [--seed SEED] [--non-interactive] [--verbose]

Basic Fantasy Character Generator CLI

options:
  -h, --help          show this help message and exit
  --version           show program's version number and exit
  --race RACE         Specify character race.
  --class CLASS_NAME  Specify character class.
  --name NAME         Specify character name.
  --json              Print character JSON to stdout.
  --output OUTPUT     Write character JSON to FILE (non-interactive mode only).
  --seed SEED         Use deterministic seed for random generation.
  --non-interactive   Run in non-interactive mode.
  --verbose           Print detailed execution steps (non-interactive mode only).
```

The CLI app operates in two different modes in the terminal:
- Interactive mode
- Non-interactive mode

**Interactive mode** enables the user to pick the character's race and class
based the rolled ability scores. The user also has the opportunity to name the
character and save the character's stats to a file.

**Non-interactive mode** will automatically generate a character without the
need for any user interaction. Different arguements can be passed to the CLI
tool to specify options, if the dice rolls and rules allow. The tool will output
the json stats of the character however, the stats can be saved to a file if
desired.  

#### Interactive mode example

Enter the `rpgcharacters` command to start interactive mode.

```bash
$ rpgcharacters 
```

Sample output:


```bash
========================================
 Basic Fantasy Character Generator
========================================

Rolling abilities...
CHA:  7 (-1)
CON: 18 (+3)
DEX:  6 (-1)
INT: 10 (+0)
STR: 16 (+2)
WIS: 16 (+2)
Accept these rolls? (y/n): y

Available Races:
  1) Dwarf
  2) Human

Choose a race [1-2]: 2
Available Classes:
  1) Cleric
  2) Fighter
  3) Magic-User

Choose a class [1-3]: 2
Character name (optional): Vey Vale
========================================
 Vey Vale the Human Fighter (Level 1)
========================================

HP: 6
AC: 10
Attack Bonus: +1
Money: 110 gp

Abilities:
CHA:  7 (-1)
CON: 18 (+3)
DEX:  6 (-1)
INT: 10 (+0)
STR: 16 (+2)
WIS: 16 (+2)

Saving Throws:
  Death Ray or Poison: 12
  Dragon Breath: 15
  Magic Wands: 13
  Paralysis or Petrify: 14
  Spells: 17

Save character as JSON file? (y/n): y
Enter filename [Vey Vale.json]: vey_vale.json
Character saved to ./vey_vale.json

Generate another character? (y/n): n
```

#### Non-interactive mode example - generate a random character

Enter the `rpgcharacters --non-interactive` command to generate a random
character.

```bash
$ rpgcharacters --non-interactive
```

Sample output:

```bash
{
  "name": null,
  "race": "human",
  "class": "magic-user",
  "level": 1,
  "abilities": {
    "CHA": 12,
    "CON": 15,
    "DEX": 9,
    "INT": 10,
    "STR": 12,
    "WIS": 7
  },
  "ability_mods": {
    "CHA": 0,
    "CON": 1,
    "DEX": 0,
    "INT": 0,
    "STR": 0,
    "WIS": -1
  },
  "hp": 4,
  "ac": 11,
  "attack_bonus": 1,
  "saving_throws": {
    "death_ray_or_poison": 13,
    "magic_wands": 14,
    "paralysis_or_petrify": 13,
    "dragon_breath": 16,
    "spells": 15
  },
  "money_gp": 80,
  "inventory": []
}
```

#### Non-interactive mode example - generate a deterministic character

Using the `--seed` argument will generate the same character.  This can be
helpful if a known seed value generates a character with desirable stats (or for
testing).

```bash
$ rpgcharacters --non-interactive --seed 7654321
```

Sample output: 

```bash
{
  "name": null,
  "race": "dwarf",
  "class": "fighter",
  "level": 1,
  "abilities": {
    "CHA": 12,
    "CON": 9,
    "DEX": 12,
    "INT": 14,
    "STR": 16,
    "WIS": 11
  },
  "ability_mods": {
    "CHA": 0,
    "CON": 0,
    "DEX": 0,
    "INT": 1,
    "STR": 2,
    "WIS": 0
  },
  "hp": 8,
  "ac": 11,
  "attack_bonus": 1,
  "saving_throws": {
    "death_ray_or_poison": 8,
    "magic_wands": 9,
    "paralysis_or_petrify": 10,
    "dragon_breath": 12,
    "spells": 13
  },
  "money_gp": 70,
  "inventory": []
}
```

---

### Library

Minimal Python code example.

```python
from diceroller.core import DiceRoller
from rpgcharacters.character_generator import generate_character

rng = DiceRoller() # random seed
character = generate_character(race="human", class_name="fighter", rng=rng, name="Vey Vale")
print(character.to_dict()) # JSON-ready dictionary
```

---

## License

Copyright Jason Tennant, 2026.

Distributed under the terms of the MIT license, rpgcharacters is free and open
source software.

---

## Credits / Legal

Basic Fantasy RPG is an open tabletop RPG. This project is a fan-made utility
and is not affiliated with the original authors/publishers.
