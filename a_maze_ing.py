"""Command-line entry point for A-Maze-ing."""

import os
from pathlib import Path
import sys
import tempfile

from configuration import read_config
from display import render
from mazegen import MazeGenerator


def write_maze(maze: MazeGenerator, filename: Path) -> None:
    """Atomically save hexadecimal walls, endpoints and the shortest path."""
    lines = [''.join(format(cell, 'X') for cell in row) for row in maze.grid]
    lines.extend(['', f'{maze.entry[0]},{maze.entry[1]}',
                  f'{maze.exit[0]},{maze.exit[1]}', maze.solve()])
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                         dir=filename.parent, delete=False,
                                         newline='\n') as stream:
            temporary = Path(stream.name)
            stream.write('\n'.join(lines) + '\n')
        os.replace(temporary, filename)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main() -> int:
    """Generate, save and interact with one configured maze."""
    if len(sys.argv) != 2:
        print('Usage: python3 a_maze_ing.py config.txt', file=sys.stderr)
        return 1
    try:
        config = read_config(sys.argv[1])
        maze = MazeGenerator(config.width, config.height, config.entry,
                             config.exit, config.perfect, config.seed)
        maze.generate()
        write_maze(maze, config.output_file)
        show_path = False
        colour = 0
        ansi = sys.stdout.isatty() and os.environ.get('TERM') != 'dumb'
        while True:
            if ansi:
                print('\033[2J\033[H', end='')
            print(render(maze, show_path, colour, ansi))
            if maze.warning:
                print(maze.warning, file=sys.stderr)
            print('E: entry | X: exit | ###: 42 | .: shortest path')
            print('[r] regenerate  [p] show/hide path  '
                  '[c] wall colour  [q] quit')
            try:
                command = input('Choice (then Enter): ').strip().lower()
            except EOFError:
                return 0
            if command == 'q':
                return 0
            if command == 'r':
                maze.generate()
                write_maze(maze, config.output_file)
            elif command == 'p':
                show_path = not show_path
            elif command == 'c':
                colour += 1
            else:
                print('Choose r, p, c or q.')
    except KeyboardInterrupt:
        print('\nGoodbye.')
        return 0
    except (OSError, ValueError, UnicodeError, MemoryError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
