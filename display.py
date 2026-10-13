"""ASCII terminal rendering with optional ANSI wall colours."""

from mazegen import MazeGenerator

COLOURS = ('\033[37m', '\033[36m', '\033[33m', '\033[35m')


def render(maze: MazeGenerator, show_path: bool = False,
           colour: int = 0, ansi: bool = False) -> str:
    """Return a maze showing walls, closed 42 cells, endpoints and path."""
    canvas = [[' '] * (maze.width * 4 + 1)
              for _ in range(maze.height * 2 + 1)]
    for y, row in enumerate(maze.grid):
        for x, walls in enumerate(row):
            top, left = y * 2, x * 4
            for dy in (0, 2):
                for dx in (0, 4):
                    canvas[top + dy][left + dx] = '+'
            for bit, dy in ((1, 0), (4, 2)):
                if walls & bit:
                    canvas[top + dy][left + 1:left + 4] = '---'
            if walls & 8:
                canvas[top + 1][left] = '|'
            if walls & 2:
                canvas[top + 1][left + 4] = '|'
            if (x, y) in maze.blocked:
                canvas[top + 1][left + 1:left + 4] = '###'
    if show_path:
        x, y = maze.entry
        steps = {'N': (0, -1), 'E': (1, 0),
                 'S': (0, 1), 'W': (-1, 0)}
        for direction in maze.solve():
            dx, dy = steps[direction]
            for offset in range(1, (4 if dx else 2) + 1):
                canvas[y * 2 + 1 + dy * offset][x * 4 + 2 + dx * offset] = '.'
            x, y = x + dx, y + dy
    for point, marker in ((maze.entry, 'E'), (maze.exit, 'X')):
        canvas[point[1] * 2 + 1][point[0] * 4 + 2] = marker
    lines = []
    for characters in canvas:
        if ansi:
            lines.append(''.join(COLOURS[colour % len(COLOURS)] + char
                                 + '\033[0m' if char in '+-|' else char
                                 for char in characters))
        else:
            lines.append(''.join(characters))
    return '\n'.join(lines)
