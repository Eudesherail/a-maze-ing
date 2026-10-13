# Subject v2.3 verification report

Checked on 2026-10-13 with Python 3.12.14, flake8 7.4.1, mypy 2.4.0,
build 1.6.1 and setuptools 84.0.0. This report distinguishes measured behavior
from remaining human confirmation; it does not guarantee a grade.

| Subject requirement | Implementation and evidence | Status |
| --- | --- | --- |
| Python 3.10+ | Python 3.12 runtime tests; mypy targets 3.10 | Passed on 3.12; 3.10 runtime not separately available/tested |
| flake8 | `make lint` executes `flake8 .` | Passed |
| Required mypy flags | Exact subject flags in `make lint` | Passed, 5 source files |
| Optional strict typing | `make lint-strict` | Passed, 5 source files |
| Type hints and docstrings | All source functions/classes annotated and documented | Reviewed |
| Resource/error handling | File context managers, atomic output, CLI exception boundary | Invalid-input and I/O checks passed |
| Makefile rules | install, run, debug, clean, lint; strict and package added | All exercised |
| Exact launch/argument format | `python3 a_maze_ing.py config.txt` | Valid/missing/excess arguments tested |
| Config and default config | Six required keys, optional seed, comment/blank handling | Valid and malformed cases tested |
| Randomness/seed | Local Random instance; repeatable sequence | Equal seeds repeat; regeneration advances |
| Wall representation | N=1, E=2, S=4, W=8 | All borders/shared walls checked independently |
| Endpoints | Different, in-bounds and not pattern cells | Invalid and interior endpoints tested |
| Full connectivity | DFS over all non-pattern cells | Independent BFS verified |
| No fully open 3x3 area | Local window check before opening extra walls | All 3x3 windows scanned independently |
| Visible 42 | Fully closed 9x7 cell design, with surrounding corridor | Shape/render inspected; closed cells tested |
| Too-small pattern | Error message, omitted pattern | Thin/small mazes checked |
| Perfect mode | Connected tree, edges = vertices - 1 | 300 mode/size/seed cases plus edge tests |
| Non-perfect mode | At least two independent cycles; at most two dead ends | 300 mode/size/seed cases plus edge tests |
| Corners and center open | Placement excludes corners and non-perfect center | Checked in every non-perfect case |
| Hex output and shortest path | Row lengths, digits, blank separator, coordinates, NESW, final newline | Byte-level output and independent shortest-distance checks passed |
| Interactive visualization | Regenerate, path toggle, wall colour, quit | Piped input and ANSI pseudo-terminal tests passed |
| Reusable unique generator class | `mazegen.MazeGenerator`, no app imports | Fresh-venv wheel import/generate/solve passed |
| Root installable artifact | Root wheel and tar.gz | Standard build and package-content checks passed |
| Rebuild inputs | pyproject, sources, package documentation and license | Wheel rebuilt from source archive without network |
| License permits reuse/distribution | Root MIT LICENSE.md and packaged license | Artifact contents checked |
| README first line and required sections | Team logins, Description, Instructions, Resources, config, algorithm, reuse | Present |
| Actual team roles/planning/reflection | Explicit confirmation placeholders and factual AI implementation notes | Team confirmation still required |
| AI disclosure | README lists AI-generated areas and review responsibility | Present; student/peer review not claimed |
| Submission hygiene | Gitignore excludes caches, venv, build directories and maze output | Submission file list reviewed |

## Test coverage

The development suite uses Python's standard-library unittest and lives outside
the repository, as the subject says test programs are not submitted/graded.
Six test groups passed, including **600 generation cases**: both modes, ten
sizes, and thirty seeds. Sizes range from 2x3 to 30x20. Additional checks:

- 160 valid combinations of interior/corner endpoints, mode, size and seed.
- 20 expected rejections where endpoints conflict with every placement of the
  chosen 42 shape in an 11x9 grid; no false success or silent pattern removal.
- Thin perfect grids (1x2, 2x1, 1x100, 100x1) and a 2x2 perfect grid.
- A 400x250 non-perfect grid (100000 cells), including full invariant checks.
- Negative/zero/oversize dimensions, equal/out-of-bounds endpoints, impossible
  non-perfect grids, solve-before-generation, invalid/duplicate/missing keys,
  invalid coordinates/boolean/numbers, missing files, unavailable output parent,
  and prevention of overwriting the configuration.
- Identical seeded sequences, differing regeneration, output formatting,
  shortest-path length and actual route traversal, and wall-preserving rendering.
- ANSI colour changes, path show/hide, regenerated output replacement and
  Ctrl-C in a pseudo-terminal; normal quit and invalid commands via piped input.
- Wheel installation in a separate virtual environment, isolated import outside
  the source tree, packaged documentation/license, and rebuilding from tar.gz.
- Makefile install with already installed dependencies and networking disabled,
  run/debug, lint/strict, package, and clean in a disposable fixture.

An early digit design caused three forced dead ends. It was replaced with wider
spacing and the tests rerun. Initial lint/type issues were corrected before the
final successful checks. A Makefile install probe initially selected the base
Python by resolving the virtualenv symlink; the probe was corrected to use the
activated environment, and install passed. This was a validation setup issue,
not a change to the install rule.

## Limits and remaining work

The subject mentions `maze_analyzer.py`, but it was not present in the supplied
attachment. Its official results and Moulinette/peer-evaluation results are
therefore **not verified**. Independent graph/wall/path tests were used instead.
The implementation permits at most two dead ends; zero-dead-end bonus is not
claimed. It uses one algorithm and does not claim animation or other bonuses.

The pattern threshold is specific to the chosen 9x7 design plus margin. Invalid
endpoint placement is reported rather than silently omitting a fitting pattern.
The application caps grids at 100000 cells and regeneration attempts at 50;
these practical limits are documented in README and the package usage notes.
Cross-version random sequence identity is not promised.

Both students still need to confirm actual roles and planning, review and
understand the code, and obtain peer review. README intentionally does not
invent this information. These human sections prevent an honest claim of
unconditional, fully completed subject compliance today.
