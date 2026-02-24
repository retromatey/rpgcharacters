CLI SPECIFICATION — Basic Fantasy Character Generator (Polished Interactive Version)

OVERVIEW
--------
Implement a polished interactive CLI in rpgcharacters/cli.py that orchestrates
character generation using existing engine functions. The CLI must NOT duplicate
rules logic. It must only call engine-layer helpers.

Use:
- roll_abilities
- valid_races_for_abilities
- valid_classes_for_race
- generate_character
- Character.to_dict() (already implemented)

No game logic may exist in the CLI.


ENTRY POINT
-----------
def main() -> None

main() must:
- Instantiate DiceRoller()
- Run a restartable interactive loop
- Catch RestartFlow exception and restart
- Catch ValueError from engine and restart flow
- Exit only when user chooses not to generate another character


FLOW STRUCTURE
--------------

1) HEADER DISPLAY

Print exactly:

========================================
 Basic Fantasy Character Generator
========================================

(blank line)


2) ABILITY PHASE

Function:
def run_ability_phase(rng: DiceRoller) -> AbilityScores

Behavior:
- Print: "Rolling abilities..."
- Roll abilities
- Compute ability modifiers
- Display abilities formatted as:

STR: 10 (+0)
DEX:  8 (-1)
CON: 14 (+1)
INT: 12 (+0)
WIS:  9 (+0)
CHA: 16 (+2)

Formatting rules:
- Abilities shown in ABILITY_ROLL_ORDER
- Ability name uppercase (3 chars)
- Colon + space
- Score right-aligned width 2
- Modifier always shows sign
- Modifier wrapped in parentheses
- One per line
- No blank lines between entries

Then prompt:
Accept these rolls? (y/n):

If:
- y → return abilities
- n → reroll (repeat phase)
- invalid → print:
  Invalid selection. Please try again.
  (blank line)
  and re-prompt


3) RACE SELECTION

Function:
def select_race(abilities: AbilityScores) -> str

Behavior:
- Call valid_races_for_abilities
- If empty:
  Print:
    No valid races available for these ability scores.
    Re-rolling abilities...
  Raise RestartFlow

- Otherwise:
  Sort races alphabetically
  Display:

Available Races:
  1) Dwarf
  2) Elf
  3) Halfling
  4) Human

(blank line)

Prompt:
Choose a race [1-N]:

- Must enter numeric selection
- Invalid → print:
  Invalid selection. Please try again.
  (blank line)
  and re-prompt

Return lowercase race string.


4) CLASS SELECTION

Function:
def select_class(abilities: AbilityScores, race: str) -> str

Behavior:
- Call valid_classes_for_race
- If empty:
  Print:
    No valid classes available for this race.
    Returning to ability roll.
  Raise RestartFlow

- Otherwise:
  Sort classes alphabetically
  Display:

Available Classes:
  1) Cleric
  2) Fighter
  3) Magic-User
  4) Thief

(blank line)

Prompt:
Choose a class [1-N]:

- Same validation behavior as race selection
- Return lowercase class string


5) NAME PROMPT

Function:
def prompt_name() -> Optional[str]

Prompt:
Character name (optional):

- Strip input
- Empty → return None
- Otherwise return string


6) CHARACTER GENERATION

Call:

generate_character(
    race=race,
    class_name=class_name,
    rng=rng,
    name=name,
    abilities=abilities
)

Wrap in try/except:
- ValueError → print error, restart flow


7) CHARACTER SUMMARY DISPLAY

Function:
def print_character_summary(character: Character) -> None

Header format:

========================================
 Aric the Human Fighter (Level 1)
========================================

If no name:

========================================
 Human Fighter (Level 1)
========================================

(blank line)

Core stats block:

HP: 4
AC: 11
Attack Bonus: +1
Money: 90 gp

(blank line)

Abilities section:

Abilities:
STR: 10 (+0)
DEX:  8 (-1)
...

(blank line)

Saving Throws section:

Saving Throws:
  Death Ray or Poison: 12
  Dragon Breath: 15
  Magic Wands: 13
  Paralysis or Petrify: 14
  Spells: 17

Rules:
- Saving throws sorted alphabetically
- Two space indent
- Value right-aligned width 2
- No blank lines between entries
- Blank line after section


8) JSON SAVE PROMPT

Function:
def maybe_save_json(character: Character) -> None

Prompt:
Save character as JSON file? (y/n):

If y:
- Default filename:
  - If name exists → "<name>.json"
  - Else → "character.json"
- Prompt:
  Enter filename [default.json]:
- Empty input → use default
- Save using:
  json.dump(character.to_dict(), file, indent=2)
- Print:
  Character saved to ./filename.json
  (blank line)

If n:
- Do nothing


9) RESTART PROMPT

Prompt:
Generate another character? (y/n):

If y:
- Restart entire flow

If n:
- Exit cleanly (no goodbye message)


ARCHITECTURAL RULES
-------------------
- No rule duplication in CLI
- No direct table access
- No color output
- No third-party libraries
- No global mutable state
- All formatting isolated to helper functions
- Sorting done in CLI
- All numeric selection via index


INTERNAL EXCEPTION

class RestartFlow(Exception):
    pass


END SPEC
