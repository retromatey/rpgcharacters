# Character Generation

The `rpgcharacters` generator creates level-1 characters using rules from the
**Basic Fantasy Role-Playing Game**.

The generator automates the typical character creation steps:

1. Roll ability scores
2. Validate race restrictions
3. Validate class requirements
4. Calculate derived statistics
5. Generate starting money

---

## Ability Scores

Ability scores are rolled using **3d6** for each ability:

```
CHA CON DEX INT STR WIS
```

Each ability receives a modifier based on the Basic Fantasy rules.

| Score | Modifier |
|-------|----------|
| 3     | -3       |
| 4–5   | -2       |
| 6–8   | -1       |
| 9–12  | 0        |
| 13–15 | +1       |
| 16–17 | +2       |
| 18    | +3       |

These modifiers are used when calculating several derived statistics such as hit
points and armor class.

---

## Race Restrictions

Some races have **minimum or maximum ability score requirements**.

Examples:

| Race     | Requirement |
|----------|-------------|
| Dwarf    | CON ≥ 9     |
| Elf      | INT ≥ 9     |
| Halfling | DEX ≥ 9     |

Some races also impose **maximum limits** on certain abilities.

Example:

| Race  | Restriction |
|-------|-------------|
| Dwarf | CHA ≤ 17    |

If a character’s rolled ability scores do not satisfy a race’s requirements,
that race will not be available as an option.

---

## Class Requirements

Classes have **prime requisite abilities** that must meet minimum values.

Examples:

| Class      | Prime Requisite |
|------------|-----------------|
| Cleric     | WIS ≥ 9         |
| Fighter    | STR ≥ 9         |
| Magic-User | INT ≥ 9         |
| Thief      | DEX ≥ 9         |

If the ability score requirement is not met, the class cannot be selected.

---

## Hit Points

Hit points are determined by:

```
1d(hit_die) + CON modifier
```

Each class has its own hit die:

| Class      | Hit Die |
|------------|---------|
| Cleric     | d6      |
| Fighter    | d8      |
| Magic-User | d4      |
| Thief      | d4      |

Some races impose a **maximum hit die limit**, which may reduce the effective
hit die used during character generation.

A minimum of **1 hit point** is always enforced.

---

## Armor Class

The generator calculates a character’s starting **Armor Class (AC)** assuming no
armor is equipped.

```
AC = base_ac + DEX modifier
```

The base AC for an unarmored character is **11**.

---

## Attack Bonus

All level-1 characters begin with a fixed attack bonus:

```
Attack Bonus = +1
```

---

## Saving Throws

Saving throws are determined by the character’s **class**, with possible
modifiers applied by the **race**.

Saving throw categories include:

- Death Ray or Poison
- Magic Wands
- Paralysis or Petrify
- Dragon Breath
- Spells

Races may provide bonuses that reduce the required saving throw number.

Example:

- Dwarves receive strong bonuses against many saving throws.

---

## Starting Money

Starting money is rolled using the Basic Fantasy rule:

```
3d6 × 10 gp
```

The result determines how much gold the character begins with.

---

## Deterministic Generation

Character generation can be made **deterministic** using a seed value.

=== "CLI"

    ```bash
    rpgcharacters --non-interactive --seed 42
    ```

=== "Python"

    ```python
    rng = DiceRoller(seed=42)
    ```

!!! tip
    Seeds are useful for testing, debugging, or reproducing a previously
    generated character.

---

## Generated Character Data

The generator returns a complete character record including:

- ability scores
- ability modifiers
- hit points
- armor class
- attack bonus
- saving throws
- starting money
- inventory
- race and class

In Python, this is represented by a `Character` object which can easily be
converted to JSON using:

```python
character.to_dict()
```
