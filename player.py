from direction import Direction


class Player:

    def __init__(self, tile_x, tile_y, tile_size):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tile_size = tile_size
        self.isAlive = True
        self.last_direction = Direction.NONE

    def move(self, direction, grid):

        next_x = self.tile_x
        next_y = self.tile_y

        if direction in (Direction.UP, 1):
            next_y -= 1
        elif direction in (Direction.DOWN, 2):
            next_y += 1
        elif direction in (Direction.LEFT, 3):
            next_x -= 1
        elif direction in (Direction.RIGHT, 4):
            next_x += 1

        if (
            0 <= next_y < len(grid)
            and 0 <= next_x < len(grid[0])
            and grid[next_y][next_x].name != "WALL"
        ):
            self.tile_x = next_x
            self.tile_y = next_y
            self.last_direction = direction

    def kill(self):
        self.isAlive = False

    def revive(self):
        self.isAlive = True

    def get_pos(self):

        return (
            self.tile_x * self.tile_size + self.tile_size // 2,
            self.tile_y * self.tile_size + self.tile_size // 2,
        )

    def get_tile(self):
        return (self.tile_x, self.tile_y)

    def reset(self, tile_x, tile_y):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.last_direction = Direction.NONE
        self.isAlive = True
