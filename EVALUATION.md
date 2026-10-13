# Reading and explaining the project

Read in this order:

1. `config.txt` and `configuration.py`: strings become validated settings.
2. `mazegen/generator.py`: cells, shared walls, generation and solving.
3. `a_maze_ing.py`: generate, save, then process commands.
4. `display.py`: turn wall bits into printable characters.
5. `pyproject.toml`, `Makefile` and `mazegen/USAGE.md`: reuse and build.

## Wall example

A cell with value 11 has bits 1 + 2 + 8: north, east and west are closed.
Only south is open. To join it to the cell below, remove south's bit 4 from
this cell and north's bit 1 from the lower cell. `value & ~bit` clears a bit;
`value & bit` tests it. Both cells must agree on a shared wall.

## Questions both team members should be able to answer

- Why does adding one new cell at a time produce no cycles?
- Why does the generator use a stack and the solver a queue?
- Why are pattern cells excluded when checking connectivity?
- Why does each extra passage in a connected tree add one independent cycle?
- Why is one extra passage insufficient in non-perfect mode?
- How does checking 3x3 windows stop wide open areas?
- Why does BFS find a shortest path, and how are parent pointers used?
- Why does another call to generate produce a new maze with a fixed seed?
- Which errors are caught by the application, and which does the API raise?
- What is inside the wheel, and how can another project import it?

## Small practice modifications

Try these locally, then restore or review your changes:

- Add a fifth wall colour.
- Display the solution length below the maze.
- Change the default seed and compare two output files.
- Change the loop threshold from two to three and explain tiny-grid failures.
- Add a command which prints the number of dead ends.

## Honest completion checklist

Confirm the team role descriptions and actual project planning in README.
Run the required tools in a fresh virtual environment and rebuild the package.
Explain the algorithm on paper with a 3x3 grid. Have a peer review the result.
The automated report is evidence about checked behavior, not a promise of a
42 grade, complete coverage of all inputs, or proof of student understanding.
