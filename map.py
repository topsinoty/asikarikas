import random
from enum import Enum


class Tile(Enum):
    WALL = 0
    PATH = 1
    PELLET = 2
    POWER = 3
    GHOST = 4


MAP_WIDTH = 28
MAP_HEIGHT = 31


class TileGridGenerator:

    def __init__(self, width=MAP_WIDTH, height=MAP_HEIGHT):

        def normalize(v):
            if (v - 3) % 2 != 0:
                v -= 1
            return max(3, v)

        self.width = normalize(width)
        self.height = normalize(height)

    __SHAPES = {
        "PLUS": [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        "VERTICAL": [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
        "HORIZONTAL": [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
        "CORNER_NE": [[0, 1, 0], [0, 1, 1], [0, 0, 0]],
        "CORNER_NW": [[0, 1, 0], [1, 1, 0], [0, 0, 0]],
        "CORNER_SE": [[0, 0, 0], [0, 1, 1], [0, 1, 0]],
        "CORNER_SW": [[0, 0, 0], [1, 1, 0], [0, 1, 0]],
        "EMPTY": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
    }

    __CONNECTIONS = {
        "PLUS": {"N", "S", "E", "W"},
        "VERTICAL": {"N", "S"},
        "HORIZONTAL": {"E", "W"},
        "CORNER_NE": {"N", "E"},
        "CORNER_NW": {"N", "W"},
        "CORNER_SE": {"S", "E"},
        "CORNER_SW": {"S", "W"},
        "EMPTY": set(),
    }

    __OPPOSITE = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E",
    }

    __WEIGHTS = {
        "HORIZONTAL": 4,
        "VERTICAL": 4,
        "CORNER_NE": 2,
        "CORNER_NW": 2,
        "CORNER_SE": 2,
        "CORNER_SW": 2,
        "PLUS": 1,
    }

    def generate(self):

        grid = [[Tile.WALL for _ in range(self.width)] for _ in range(self.height)]

        self._carve_maze(grid)

        self._ensure_connectivity(grid)

        self._mirror(grid)

        self._place_ghost_box(grid)

        self._place_pellets(grid)

        self._place_power_pellets(grid)

        return grid

    def _choose_shape(self, neighbors):

        valid: list[str] = []

        for shape, exits in self.__CONNECTIONS.items():

            if shape == "EMPTY":
                continue

            ok = True

            for direction, neighbor_shape in neighbors.items():

                if neighbor_shape is None:
                    continue

                neighbor_exits = self.__CONNECTIONS[neighbor_shape]

                if self.__OPPOSITE[direction] in neighbor_exits:
                    if direction not in exits:
                        ok = False
                        break

            if ok:
                valid.append(shape)

        if not valid:
            return "EMPTY"

        weights = [self.__WEIGHTS.get(s, 1) for s in valid]

        return random.choices(valid, weights=weights)[0]

    def _carve_maze(self, grid):

        group_w = (self.width - 1) // 2
        group_h = (self.height - 1) // 2

        groups = [[None for _ in range(group_w)] for _ in range(group_h)]

        for gy in range(group_h):
            for gx in range(group_w):

                neighbors = {
                    "N": groups[gy - 1][gx] if gy > 0 else None,
                    "W": groups[gy][gx - 1] if gx > 0 else None,
                    "S": None,
                    "E": None,
                }

                shape = self._choose_shape(neighbors)

                groups[gy][gx] = shape

                shape_map = self.__SHAPES[shape]

                base_x = gx * 2 + 1
                base_y = gy * 2 + 1

                for y in range(3):
                    for x in range(3):

                        px = base_x + x - 1
                        py = base_y + y - 1

                        if 0 <= px < self.width and 0 <= py < self.height:
                            if shape_map[y][x] == 1:
                                grid[py][px] = Tile.PATH

    def _ensure_connectivity(self, grid):

        visited = set()

        start = None

        for y in range(self.height):
            for x in range(self.width):
                if grid[y][x] == Tile.PATH:
                    start = (x, y)
                    break
            if start:
                break

        if start is None:
            return

        stack = [start]

        while stack:

            x, y = stack.pop()

            if (x, y) in visited:
                continue

            visited.add((x, y))

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

                nx = x + dx
                ny = y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if grid[ny][nx] == Tile.PATH:
                        stack.append((nx, ny))

        for y in range(self.height):
            for x in range(self.width):

                if grid[y][x] != Tile.PATH:
                    continue

                if (x, y) in visited:
                    continue

                self._connect_to_region(grid, x, y, visited)
                return self._ensure_connectivity(grid)

    def _connect_to_region(self, grid, x, y, visited):

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

            cx, cy = x, y

            while True:

                cx += dx
                cy += dy

                if not (0 <= cx < self.width and 0 <= cy < self.height):
                    break

                if (cx, cy) in visited:
                    break

                grid[cy][cx] = Tile.PATH

    def _mirror(self, grid):

        mid = self.width // 2

        for y in range(self.height):
            for x in range(mid):
                grid[y][self.width - 1 - x] = grid[y][x]

    def _place_ghost_box(self, grid):

        cx = self.width // 2
        cy = self.height // 2

        for y in range(cy - 2, cy + 2):
            for x in range(cx - 3, cx + 3):
                grid[y][x] = Tile.GHOST

    def _place_pellets(self, grid):

        for y in range(self.height):
            for x in range(self.width):

                if grid[y][x] == Tile.PATH:
                    grid[y][x] = Tile.PELLET

    def _place_power_pellets(self, grid):

        corners = [
            (1, 3),
            (1, self.height - 4),
            (self.width - 2, 3),
            (self.width - 2, self.height - 4),
        ]

        for x, y in corners:
            if grid[y][x] == Tile.PELLET:
                grid[y][x] = Tile.POWER


if __name__ == "__main__":

    gen = TileGridGenerator()

    grid = gen.generate()

    for row in grid:
        print(
            "".join(
                {
                    Tile.WALL: "[.]",
                    Tile.PELLET: " * ",
                    Tile.POWER: " o ",
                    Tile.GHOST: " g ",
                }.get(cell, "   ")
                for cell in row
            )
        )
