import random
from enum import Enum


class Tile(Enum):
    WALL = 0
    PATH = 1
    PELLET = 2
    POWER = 3
    GHOST = 4


MAP_WIDTH = 40
MAP_HEIGHT = 20


class TileGridGenerator:

    def __init__(self, width=MAP_WIDTH, height=MAP_HEIGHT):
        # if width % 2 == 0:
        #     width -= 1
        # if height % 2 == 0:
        #     height -= 1

        self.width = width
        self.height = height

    def generate(self):
        grid = [[Tile.WALL for _ in range(self.width)] for _ in range(self.height)]

        self._carve_maze(grid, 1, 1)

        self._mirror(grid)

        self._place_ghost_box(grid)

        self._place_pellets(grid)

        self._place_power_pellets(grid)

        return grid

    def _carve_maze(self, grid, x, y):
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if not self._inside(nx, ny):
                continue

            if grid[ny][nx] != Tile.WALL:
                continue

            grid[y + dy // 2][x + dx // 2] = Tile.PATH
            grid[ny][nx] = Tile.PATH

            self._carve_maze(grid, nx, ny)

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

    def _inside(self, x, y):
        return 0 < x < self.width - 1 and 0 < y < self.height - 1


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
                }.get(cell, " ")
                for cell in row
            )
        )
