## Purpose

This file gives compact, actionable guidance to an AI coding agent (Copilot/GPT-style) working in this repository. Focus is on the repo's architecture, developer workflows, project-specific patterns, and concrete examples taken from source files.

## Big-picture architecture

- **Two main domains**: `game_engine/` (game logic + AI) and `hardware_interface/` (MicroPython LED control). The top-level `main.py` exists but is currently empty.
- **Runtime split**: `game_engine` is standard CPython code (intended to run locally). `hardware_interface/LED_matrix_control.py` targets MicroPython on a microcontroller (uses `machine.Pin`, `utime`). Do not run MicroPython code under CPython without mocking or adaptation.

## Key files (examples)

- `game_engine/game.py`: single `Game` class that models a small board game (appears to be tic-tac-toe). Note: the file contains several bugs/oddities (see "Code smells / gotchas"). Use this file to understand expected data shapes and method names such as `perform_move`, `simulate_move`, `is_won`.
- `game_engine/ai.py`: currently empty — the canonical place for AI logic.
- `hardware_interface/LED_matrix_control.py`: MicroPython code that controls a 3x3 bi-color LED matrix. Public function: `update_matrix(matrix: list[list[int]])` where values mean: `0=off`, `1=red`, `2=green`, `3=amber`.

## Developer workflows (discoverable here)

- Local Python environment: README.md recommends using a venv and installing requirements. Example commands (PowerShell):

```
python -m venv .\venv
.\venv\Scripts\activate
pip install -r requirements-dev.txt
```

- Microcontroller testing: `hardware_interface/LED_matrix_control.py` expects MicroPython. Use the project's MicroPico vREPL terminal (or a tool like `rshell`/`ampy`/Thonny) to copy and run this file on the device. Do not import `machine` on normal CPython.

## Project-specific conventions & patterns

- Mixed target environments: some modules are for CPython, others for MicroPython. When editing or adding code, annotate or gate imports (e.g., try/except ImportError or add clear module-level comments) and add tests/mocks for hardware-specific code.
- LED matrix mapping: `col_pins` is an interleaved list of pins; note how red/green are indexed:

  - `green_pin = col_pins[j*2]`
  - `red_pin   = col_pins[j*2+1]`

  The file also documents that the LEDs are common-anode, so setting a pin `low()` turns it on.

- API surface to call: use `update_matrix(matrix)` with a 3x3 list of integers 0..3. The function validates dimensions and raises on invalid value.

## Code smells / gotchas for an AI agent to be aware of

- `game_engine/game.py` contains multiple defects that will confuse naive edits. Examples (do not blindly refactor without tests):
  - `self.board:list[str] = self.__init_board()` creates 8 empty strings but the logic later expects 9 cells (0..8).
  - `empty_space` iterates `for i in range(len(self.board)-1):` and tests `if i == "":` (should be checking `self.board[i]`), and returns indexes incorrectly typed.
  - `is_won` checks players with `if player != "x" or player != "o":` which always raises — should be `and`.

  When working in `game_engine`, create small unit tests or add runtime assertions before changing shared logic.

## Integration points & testing suggestions

- Hardware integration: changes to `hardware_interface/LED_matrix_control.py` should be tested on-device. To avoid constant flashing during development, extract logic that maps integers -> pin states into a pure function and unit test that mapping under CPython.
- AI/game development: `game_engine/ai.py` is the place to implement decision logic; import `Game` from `game_engine.game` and use `simulate_move`/`is_won` (first fix the game logic defects or write test harnesses that capture current behaviour).

## Example snippets (copy-paste safe)

- Valid 3x3 matrix for `update_matrix`:

```
from hardware_interface.LED_matrix_control import update_matrix

image = [
  [1,2,1],
  [0,3,0],
  [1,2,1]
]
update_matrix(image)
```

- Recommended MicroPython guard when editing hardware files:

```
try:
    from machine import Pin
except ImportError:
    # Running under CPython: provide a mock or skip hardware calls
    Pin = None
```

## What to fix first (prioritized)

- Add unit tests for `game_engine/game.py` to capture current behaviour and then fix the bugs listed above.
- Add a short README or script describing how to flash/run `hardware_interface/LED_matrix_control.py` on the MicroPico (device-specific steps are not in the repo).

## Where to ask for clarification

- If the intended board size or rules in `game_engine/game.py` are uncertain, open an issue or ask the repository owner. Changes to pin mappings should be verified against the physical board wiring.

---

If any section is unclear or you want me to expand examples (e.g., mock harness for `machine.Pin` or unit tests for `Game`), tell me which area to expand and I will update this file accordingly.
