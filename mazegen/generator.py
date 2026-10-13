"""Seeded maze generation, independent of the terminal application."""

from collections import deque
import random
from typing import Optional

Point = tuple[int, int]
DIRECTIONS = ((0, -1, 1, 4, 'N'), (1, 0, 2, 8, 'E'),
              (0, 1, 4, 1, 'S'), (-1, 0, 8, 2, 'W'))
PATTERN = ('#..#.####', '#..#....#', '#..#....#', '####.####',
           '...#.#...', '...#.#...', '...#.####')


class MazeGenerator:
    """Generate a wall grid; coordinates are (x, y), grid access is [y][x]."""

    def __init__(self, width: int, height: int, entry: Point,
                 exit: Point, perfect: bool = False,
                 seed: Optional[int] = None) -> None:
        """Validate dimensions and endpoints and prepare a local RNG."""
        if type(width) is not int or type(height) is not int:
            raise ValueError('Width and height must be integers.')
        if width < 1 or height < 1 or width * height > 100000:
            raise ValueError('Use positive dimensions, at most 100000 cells.')
        for point in (entry, exit):
            if (len(point) != 2 or any(type(v) is not int for v in point)
                    or not 0 <= point[0] < width
                    or not 0 <= point[1] < height):
                raise ValueError('Entry and exit must be inside the maze.')
        if entry == exit:
            raise ValueError('Entry and exit must be different.')
        if type(perfect) is not bool:
            raise ValueError('Perfect must be a boolean.')
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.random = random.Random(seed)
        self.grid: list[list[int]] = []
        self.blocked: set[Point] = set()
        self.warning = ''

    def neighbors(self, point: Point) -> list[tuple[Point, int, int, str]]:
        """Return in-bounds, non-pattern neighbors with paired wall bits."""
        x, y = point
        result = []
        for dx, dy, wall, opposite, letter in DIRECTIONS:
            next_point = (x + dx, y + dy)
            if (0 <= x + dx < self.width and 0 <= y + dy < self.height
                    and next_point not in self.blocked):
                result.append((next_point, wall, opposite, letter))
        return result

    def _place_pattern(self) -> None:
        """Place a readable 42 with a surrounding corridor and clear center."""
        self.blocked = set()
        self.warning = ''
        if self.width < 11 or self.height < 9:
            self.warning = 'Error: maze too small for 42; pattern omitted.'
            return
        forbidden = {self.entry, self.exit}
        if not self.perfect:
            forbidden.add((self.width // 2, self.height // 2))
        positions = [(x, y) for y in range(1, self.height - 7)
                     for x in range(1, self.width - 9)]
        positions.sort(key=lambda p: abs(p[0] - (self.width - 9) // 2)
                       + abs(p[1] - (self.height - 7) // 2))
        for left, top in positions:
            cells = {(left + x, top + y) for y, row in enumerate(PATTERN)
                     for x, value in enumerate(row) if value == '#'}
            if not cells & forbidden:
                self.blocked = cells
                return
        raise ValueError('Endpoints/center conflict with every 42 placement.')

    def _open(self, point: Point, other: Point,
              wall: int, opposite: int) -> None:
        """Remove both sides of a shared wall."""
        self.grid[point[1]][point[0]] &= ~wall
        self.grid[other[1]][other[0]] &= ~opposite

    def _tree(self) -> None:
        """Carve an iterative randomized depth-first spanning tree."""
        self.grid = [[15] * self.width for _ in range(self.height)]
        visited = {self.entry}
        stack = [self.entry]
        while stack:
            point = stack[-1]
            choices = [item for item in self.neighbors(point)
                       if item[0] not in visited]
            if not choices:
                stack.pop()
                continue
            other, wall, opposite, _ = self.random.choice(choices)
            self._open(point, other, wall, opposite)
            visited.add(other)
            stack.append(other)
        if len(visited) != self.width * self.height - len(self.blocked):
            raise ValueError('The 42 pattern disconnects this grid.')

    def _large_area(self, point: Point) -> bool:
        """Check 3x3 areas near a newly opened wall for missing inner walls."""
        px, py = point
        for y in range(max(0, py - 2), min(py, self.height - 3) + 1):
            for x in range(max(0, px - 2), min(px, self.width - 3) + 1):
                horizontal = all(not self.grid[j][i] & 2
                                 for j in range(y, y + 3)
                                 for i in range(x, x + 2))
                vertical = all(not self.grid[j][i] & 4
                               for j in range(y, y + 2)
                               for i in range(x, x + 3))
                if horizontal and vertical:
                    return True
        return False

    def _try_open(self, point: Point, other: Point,
                  wall: int, opposite: int) -> bool:
        """Open a wall unless this creates a fully open 3x3 area."""
        self._open(point, other, wall, opposite)
        if self._large_area(point):
            self.grid[point[1]][point[0]] |= wall
            self.grid[other[1]][other[0]] |= opposite
            return False
        return True

    def degree(self, point: Point) -> int:
        """Count open passages from a cell."""
        return 4 - self.grid[point[1]][point[0]].bit_count()

    def _braid(self) -> bool:
        """Remove dead ends and ensure at least two independent cycles."""
        cells = [(x, y) for y in range(self.height)
                 for x in range(self.width) if (x, y) not in self.blocked]
        self.random.shuffle(cells)
        cycles = 0
        for point in cells:
            if self.degree(point) != 1:
                continue
            choices = self.neighbors(point)
            self.random.shuffle(choices)
            for other, wall, opposite, _ in choices:
                if self.grid[point[1]][point[0]] & wall:
                    if self._try_open(point, other, wall, opposite):
                        cycles += 1
                        break
        for point in cells:
            if cycles >= 2:
                break
            for other, wall, opposite, _ in self.neighbors(point):
                if self.grid[point[1]][point[0]] & wall:
                    if self._try_open(point, other, wall, opposite):
                        cycles += 1
                        break
        dead_ends = sum(self.degree(point) == 1 for point in cells)
        return cycles >= 2 and dead_ends <= 2

    def generate(self) -> list[list[int]]:
        """Generate the grid, raising ValueError for unsupported parameters."""
        self._place_pattern()
        if not self.perfect and (min(self.width, self.height) < 2
                                 or self.width * self.height < 6):
            raise ValueError('Non-perfect mode needs at least a 2x3 grid.')
        for _ in range(50):
            self._tree()
            if self.perfect or self._braid():
                return self.grid
        raise ValueError('Could not build a board with at most two dead ends.')

    def solve(self) -> str:
        """Return a shortest NESW path using breadth-first search."""
        if not self.grid:
            raise ValueError('Call generate() before solve().')
        queue = deque([self.entry])
        previous: dict[Point, tuple[Point, str]] = {}
        visited = {self.entry}
        while queue:
            point = queue.popleft()
            if point == self.exit:
                break
            for other, wall, _, letter in self.neighbors(point):
                if (other not in visited
                        and not self.grid[point[1]][point[0]] & wall):
                    visited.add(other)
                    previous[other] = (point, letter)
                    queue.append(other)
        if self.exit not in visited:
            raise ValueError('No path from entry to exit.')
        path = []
        point = self.exit
        while point != self.entry:
            point, letter = previous[point]
            path.append(letter)
        return ''.join(reversed(path))
