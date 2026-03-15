# CLI Reference

The `rpgcharacters` command provides a command-line interface for generating
Basic Fantasy RPG characters.

The CLI supports two operating modes:

- **Interactive mode** – guided character creation in the terminal
- **Non-interactive mode** – automatic character generation suitable for
  scripting or automation

---

## Command Help

The CLI arguments can be viewed with:

```bash
rpgcharacters --help
```

Example output:

```bash
{{ run("rpgcharacters --help") }}
```

---

## Interactive Mode

Running the command with no arguments launches the interactive character
creation wizard.

```bash
rpgcharacters
```

The wizard will guide you through:

1. Rolling ability scores
2. Selecting a valid race
3. Selecting a valid class
4. Optionally naming the character
5. Optionally saving the character to a JSON file

Example interaction:

```console
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
```

---

## Non-Interactive Mode

Non-interactive mode generates a character automatically without prompting the
user.

```bash
rpgcharacters --non-interactive
```

Example output:

```json
{
  "race": "human",
  "class": "magic-user",
  "level": 1
}
```

This mode is useful for:

- scripts
- automated tools
- testing
- generating large numbers of characters

---

## Deterministic Generation

A deterministic character can be generated using a random seed.

=== "CLI"

    ```bash
    rpgcharacters --non-interactive --seed 42
    ```

=== "Python Equivalent"

    ```python
    rng = DiceRoller(seed=42)
    ```

!!! tip
    Using a seed guarantees the same character is generated every time.

This is useful for:

- debugging
- tests
- reproducible examples

---

## Saving Character Output

Character data can be written directly to a file.

```bash
rpgcharacters --non-interactive --output character.json
```

The file will contain the generated character in JSON format.

---

## Specifying Character Options

Some attributes can be provided directly via command line arguments.

Example:

```bash
rpgcharacters --non-interactive --race dwarf --class fighter
```

If the specified race or class violates ability score requirements, the
generator will exit with an error.

---

## Verbose Mode

Verbose mode prints detailed execution information.

```bash
rpgcharacters --non-interactive --verbose
```

This can help diagnose validation failures or observe how characters are
generated internally.

---

## JSON Output

JSON output can be printed directly to standard output.

```bash
rpgcharacters --non-interactive --json
```

This is useful for piping output into other tools.

Example:

```bash
rpgcharacters --non-interactive --json | jq
```
