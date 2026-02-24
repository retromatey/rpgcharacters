CLI SPECIFICATION — Dual-Mode Basic Fantasy Character Generator

OVERVIEW
--------
Implement a dual-mode CLI in rpgcharacters/cli.py supporting:

1) Interactive mode (default)
2) Non-interactive mode (triggered by flags)

No game logic duplication is allowed. All rules must call into engine layer.

Use:
- roll_abilities
- valid_races_for_abilities
- valid_classes_for_race
- generate_character
- Character.to_dict()

Exit codes:
- Success: exit(0)
- Argument/validation error in non-interactive mode: exit(2)


============================================================
ARGUMENT PARSING
============================================================

Use argparse:

parser = argparse.ArgumentParser(
    prog="rpgcharacters",
    description="Basic Fantasy Character Generator CLI",
)

Arguments:

--race RACE
    Specify character race (e.g., human, dwarf, elf, halfling).

--class CLASS
    dest="class_name"
    Specify character class (e.g., fighter, cleric, magic-user, thief).

--name NAME
    Specify character name.

--json
    Print character JSON to stdout.

--output FILE
    Write character JSON to FILE (non-interactive mode only).

--seed INT
    Use deterministic seed for random generation.

--non-interactive
    Run in non-interactive mode.

--verbose
    Print detailed execution steps (non-interactive mode only).

Do NOT validate race/class at argparse level.


============================================================
MODE RESOLUTION
============================================================

Non-interactive mode activates if ANY of:
- --non-interactive
- --race
- --class
- --json
- --output
- --seed
- --verbose

Otherwise → interactive mode.


============================================================
INTERACTIVE MODE
============================================================

Behavior:
- Same as existing polished CLI.
- Prompts for reroll, race selection, class selection, name.
- Restarts on validation errors.
- Displays human-readable summary.
- Prompts for JSON save.

Special flag handling:
- --seed: initialize deterministic RNG.
- --json: skip save prompt and print JSON to stdout.
- --output: ignored.
- --verbose: ignored.

Never prefix output with [verbose] in interactive mode.


============================================================
NON-INTERACTIVE MODE
============================================================

1) Initialize RNG:
   - If --seed provided:
       deterministic behavior
       if verbose: print "[verbose] Using seed: <seed>"
   - Else:
       normal RNG

2) Roll abilities.
   If verbose:
       print "[verbose] Rolling abilities..."
       print "[verbose] Abilities: STR=10, DEX=8, ..."

3) Resolve race:
   - If --race provided:
       normalize lowercase
       validate against rolled abilities
       if invalid:
           print error to stderr
           if verbose: prefix with "[verbose] "
           exit(2)
   - Else:
       select first valid race alphabetically
       if verbose:
           print "[verbose] Auto-selected race: <race>"

4) Resolve class:
   - Same logic as race
   - Auto-select first valid class alphabetically if not provided
   - If invalid → stderr + exit(2)

5) Generate character.

6) Output:

   If --output provided:
       Write JSON to file only.
       If verbose:
           print "[verbose] Writing JSON to ./<file>"
       Do NOT print JSON to stdout.

   Else:
       Print JSON to stdout.

   JSON must be:
       json.dumps(character.to_dict(), indent=2)

7) Exit(0)


============================================================
VERBOSE RULES
============================================================

- Only active in non-interactive mode.
- All verbose lines prefixed with:
      [verbose] 
- JSON output must NEVER be prefixed.
- Errors in verbose mode:
      printed to stderr
      prefixed with "[verbose] "


============================================================
ARCHITECTURE REQUIREMENTS
============================================================

- Keep run_interactive() and run_noninteractive(args) separate.
- No rule duplication.
- No direct table access.
- No global mutable state.
- No third-party libraries.
- Sorting handled in CLI layer.
- Race/class normalization to lowercase before engine calls.
- Identical seed + flags must produce identical character.


============================================================
END SPEC
============================================================
