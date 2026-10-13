# mazegen

A Python 3.10+ maze generator using only the standard library.

Install the wheel with `python3 -m pip install mazegen-1.0.0-py3-none-any.whl`.

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20, height=15,
    entry=(0, 0), exit=(19, 14),
    perfect=False, seed=42,
)
grid = maze.generate()
print(maze.solve())
print(grid[0][0])
print(maze.warning)
```

Coordinates are `(x, y)`, starting at the top left. Access walls with
`grid[y][x]`. Each integer uses North=1, East=2, South=4, West=8;
a set bit means a closed wall. `solve()` returns a shortest route as NESW.
`blocked` contains the fully closed cells forming 42. Treat the returned grid
as read-only: changing it can invalidate connectivity and the solution.

`perfect=True` creates a spanning tree. The default `False` adds passages,
requires at least two independent cycles, and allows at most two dead ends.
Both modes retain external walls and forbid completely open 3x3 areas.

Identical parameters and seed reproduce the same first maze on the same Python
runtime. Calling `generate()` again advances this instance's random state.
Two instances with the same seed also reproduce the same generation sequence.
Different seeds can produce the same maze on tiny grids; uniqueness is not
promised. `seed=None` uses Python's default random seeding.

Dimensions must be positive integers with at most 100000 cells. Endpoints must
be distinct and in bounds. Non-perfect mode needs at least 2x3 or 3x2 cells.
The 9x7 digit design needs an 11x9 grid including its surrounding corridor;
on-fitting grids omit 42 and expose an error message in `warning`. The caller
must display that warning. When it fits, placement avoids endpoints and, in
non-perfect mode, `(width // 2, height // 2)`. If no placement fits these
constraints, generation raises `ValueError` instead of silently dropping 42.
Generation also raises `ValueError` if the board cannot meet its constraints
within 50 attempts. Calling `solve()` before generation raises `ValueError`.
Catch these exceptions at the boundary of your own application.

The module has no terminal or file-writing dependency. `degree((x, y))` counts
passages of a generated cell; `neighbors((x, y))` returns non-pattern neighbors
as `(point, wall_bit, opposite_bit, direction)` tuples. Pass valid in-bounds
coordinates to these helpers.

Build from the project sources: install `requirements-dev.txt`, then run
`make package`. The generated archive includes this documentation and the
MIT license. See the project root LICENSE.md for reuse and distribution terms.
