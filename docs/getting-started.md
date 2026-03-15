# Getting Started

This guide will help you install **rpgcharacters** and generate your first Basic
Fantasy RPG character.

---

## Install

The easiest way to install the project is from a release build hosted on GitHub.

```bash
pip install https://github.com/retromatey/rpgcharacters/releases/download/v0.1.0/rpgcharacters-0.1.0-py3-none-any.whl
```

!!! note
    Replace `v0.1.0` with the latest version from the
    [GitHub releases page](https://github.com/retromatey/rpgcharacters/releases).

---

## Verify Installation

After installation, confirm the CLI is available:

```bash
rpgcharacters --help
```

You should see the command line usage information printed to the terminal.

---

## Generate Your First Character

=== "CLI"

    Generate a random character:

    ```bash
    rpgcharacters --non-interactive
    ```

=== "Python"

    ```python
    from diceroller.core import DiceRoller
    from rpgcharacters.character_generator import generate_character

    rng = DiceRoller()

    character = generate_character(
        race="human",
        class_name="fighter",
        rng=rng,
    )

    print(character.to_dict())
    ```

---

## Deterministic Character Generation

You can generate the **same character repeatedly** by providing a seed value.

=== "CLI"

    ```bash
    rpgcharacters --non-interactive --seed 42
    ```

=== "Python"

    ```python
    from diceroller.core import DiceRoller

    rng = DiceRoller(seed=42)
    ```

!!! tip
    Seeds are useful for testing, reproducible examples, or cloning a character
    that was previously generated.

---

## Development Installation

If you want to work on the project locally:

```bash
git clone https://github.com/retromatey/rpgcharacters.git
cd rpgcharacters
pip install -e .[dev]
```

This installs the package in **editable mode**, allowing changes to the source
code to immediately affect the installed package.

---

## Verify Project Health

Run the following commands to check the health of the project:

```bash
ruff check .
mypy src
pytest --cov=rpgcharacters --cov-report=term-missing
python -m build
```

---

## Next Steps

- See **Character Generation** to understand how characters are created.
- See **CLI Reference** for all command-line options.
- See **API Reference** for the full Python interface.
