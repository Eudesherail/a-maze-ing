*This project has been created as part of the 42 curriculum by emsevind, mde-andr.*

# A-Maze-ing

## Description

A small Python maze generator based on subject version 2.3. It reads a text
configuration, generates a perfect maze or a connected board with multiple
loops, writes hexadecimal walls and a shortest path, and displays an
interactive ASCII maze. Fully closed cells draw 42 where the dimensions allow
our digit design. Runtime code uses only Python's standard library.

## Instructions

Use **Python 3.10 or newer**. Check `python3 --version` first; the default
Python on some Macs is older. From the project directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
make install
python3 a_maze_ing.py config.txt
```

Enter a letter followed by Enter:

- `r`: generate another maze and replace the output file.
- `p`: show or hide a shortest path.
- `c`: cycle wall colours in a terminal supporting ANSI colours.
- `q`: quit. Ctrl-C and end-of-input also exit normally.

`E` is the entry, `X` the exit, `###` a closed pattern cell, and `.` the path.
Redirected output is plain text. Large mazes may require a wider terminal or
scrolling; no graphical dependency is needed. Regeneration advances the seeded
random sequence, so restarting with the same seed reproduces it.

Other commands: `make run`, `make debug` (pdb), `make lint`,
`make lint-strict`, `make clean`, and `make package`.
`PYTHON` and `CONFIG` can be overridden, for example
`make run PYTHON=python3.12 CONFIG=config.txt`.
Activate the virtual environment before linting so its tools are on PATH.
`make clean` removes caches and build directories but preserves the root
package archives and maze output. Lint uses the exact mandatory subject flags;
strict lint adds `mypy . --strict`.

## Configuration

One `KEY=VALUE` pair per line; blank lines and lines beginning with `#` after
whitespace are ignored. Surrounding whitespace is allowed. Unknown keys,
duplicates, empty values and missing mandatory keys are errors. Inline comments
are not supported. All six subject keys remain mandatory, including PERFECT;
the supplied configuration and generator API default to non-perfect mode.

```ini
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

| Key | Meaning |
| --- | --- |
| WIDTH, HEIGHT | Positive integer dimensions; at most 100000 cells total |
| ENTRY, EXIT | Distinct zero-based `x,y` coordinates inside the grid |
| OUTPUT_FILE | UTF-8 output path, relative to the current working directory |
| PERFECT | `True` or `False`, case-insensitive |
| SEED | Optional integer; omit for a new random sequence |

The output parent directory must already exist. The configuration cannot be
used as the output file. The program replaces the output only after preparing
a complete result. File errors, invalid settings, unsupported dimensions and
interruption receive readable messages rather than an unhandled traceback.

The 42 design is 9x7 cells plus a surrounding corridor, so it needs at least
11x9. Smaller grids print an error explaining pattern omission and still run
if their other parameters are possible. When the pattern fits, the program
moves it to avoid entry/exit and the non-perfect center. If no such placement
exists it reports an error. Non-perfect grids require at least 2x3 or 3x2;
perfect grids can be a single row or column with distinct endpoints.
For even dimensions, center means `(WIDTH // 2, HEIGHT // 2)`.

## Algorithms and choices

Generation uses **iterative randomized depth-first search (backtracking)**.
Start with all walls closed, place the 42, then visit an unvisited neighbor,
opening both sides of the wall. A stack remembers the path. If a cell has no
unvisited neighbor, remove it from the stack. Each new cell adds exactly one
edge, creating a connected tree without loops. An explicit stack avoids the
recursion limit and keeps the steps easy to trace.

For non-perfect mode, visit dead ends in random order and open an additional
wall where possible. Every added passage is checked against fully open 3x3
areas. Add more passages if needed to reach two independent cycles. Accept
only boards with at most two dead ends; retry up to 50 times otherwise. The
pattern and its margin keep the four corners and center traversable. Zero
dead ends often occur but are **not guaranteed or claimed as a bonus**.

The solver uses **breadth-first search** with a queue and parent pointers.
It finds a shortest path because every passage has equal cost. Parent pointers
let us reconstruct the route without storing whole paths for every cell.

The design uses one generator class, ordinary lists/sets, loops, and small
helpers. No plugin framework, inheritance hierarchy or external runtime
library is used. See EVALUATION.md for a code-reading guide.

## Output format

Rows contain one uppercase hexadecimal digit per cell. Closed wall bits are
North=1, East=2, South=4, West=8. Neighboring cells agree on shared walls;
external borders stay closed. After the rows comes one blank line, then entry
`x,y`, exit `x,y`, and a shortest path using `N`, `E`, `S`, `W`, each on its own
line. Every line ends with a newline.

## Reusable generator and packaging

Only the `mazegen` package is reusable; application configuration, file output,
and terminal rendering stay separate. Install the root wheel with:

```sh
python3 -m pip install mazegen-1.0.0-py3-none-any.whl
```

```python
from mazegen import MazeGenerator

maze = MazeGenerator(20, 15, (0, 0), (19, 14), perfect=False, seed=42)
grid = maze.generate()       # grid[y][x], integer wall bits
route = maze.solve()         # shortest NESW string
print(grid[0][0], route)
if maze.warning:
    print(maze.warning)
```

Use `perfect=True` for a tree. Identical inputs and seed reproduce the first
maze on the same Python runtime. Repeated `generate()` calls advance local
random state. Read `maze.blocked` for the pattern coordinates; treat `grid` as
read-only. Invalid parameters and solve-before-generate raise `ValueError`.
Full API notes are in `mazegen/USAGE.md`, also included in the wheel.

`make install` installs build tools; `make package` creates a wheel and source
archive at the repository root. Both can be installed by pip. `pyproject.toml`
and package sources allow rebuilding during evaluation. The MIT license in
LICENSE.md explicitly allows reuse and distribution; it is included in the
built package. The private development tests and virtual environment are not
part of the submission, following the subject's test-program guidance.

## Team and project management

- **emsevind:** team member; actual responsibilities and contributions must be
  confirmed by the team before evaluation.
- **mde-andr:** team member; actual responsibilities and contributions must be
  confirmed by the team before evaluation.

No division of work, dates or student-authored contributions are invented here.
The team's original planning and its evolution have not been supplied; add
that factual account before evaluation.

For this AI-assisted implementation, the actual sequence was subject review,
generator, terminal/config/output code, independent tests, packaging and
validation. An initial narrower 42 forced three dead ends; testing identified
this and led to wider spacing. Separating generator and display made the
checks easier. What remains to improve is the team's own review, documented
role split, and practice explaining/modifying the code. These are pending
human tasks, not completed peer review.

Tools used: Python, standard-library unittest, flake8, mypy, setuptools/build,
Git, GitHub CLI and Codex. See COMPLIANCE.md for measured checks and limitations.

## Resources

- [Python tutorial](https://docs.python.org/3/tutorial/)
- [Python random module](https://docs.python.org/3/library/random.html)
- [Python deque](https://docs.python.org/3/library/collections.html#collections.deque)
- [Python packaging tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [PEP 257 docstrings](https://peps.python.org/pep-0257/)
- [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Maze generation algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- The provided A-Maze-ing subject, version 2.3.

AI use: Codex generated the initial Python implementation, configuration,
Makefile, packaging files, documentation and independent test scripts; it ran
checks and corrected issues. These files are AI-assisted work, not a claim
that either student wrote a particular portion. Both students must review,
understand and take responsibility for the submitted code. Team roles,
planning history and peer review require their confirmation.
