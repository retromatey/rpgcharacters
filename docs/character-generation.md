# Character Generation

## Generate a Character

=== "CLI"

    ```bash
    rpgcharacters --non-interactive --json --seed 42
    ```

=== "Python"

    ```python
    from diceroller import DiceRoller
    from rpgcharacters.character_generator import generate_character

    rng = DiceRoller(seed=42)

    character = generate_character(
        race="human",
        class_name="fighter",
        rng=rng,
    )

    print(character)
    ```
