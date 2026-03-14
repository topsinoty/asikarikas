import random
from direction import Direction
from map import Tile
from Navigation import a_star


def _clamp(value, low, high):
    return max(low, min(value, high))


class Ghost:
    def __new__(cls, number, tile_size, spawn_tile):
        ghosts = {1: Blinky, 2: Inky, 3: Pinky, 4: Clyde}
        if number not in ghosts:
            raise ValueError("Invalid ghost number. Choose 1-4.")
        return ghosts[number](tile_size, spawn_tile)


class GhostBase:
    def __init__(self, name, color, tile_size, spawn_tile, scatter_target, move_delay=0.18):
        self.name = name
        self.color = color
        self.tile_size = tile_size
        self.spawn_tile = spawn_tile
        self.tile_x, self.tile_y = spawn_tile
        self.scatter_target = scatter_target
        self.mode = "CHASE"
        self.move_delay = move_delay
        self._move_timer = 0.0

    def get_tile(self):
        return (self.tile_x, self.tile_y)

    def get_pos(self):
        return (
            self.tile_x * self.tile_size + self.tile_size // 2,
            self.tile_y * self.tile_size + self.tile_size // 2,
        )

    def set_mode(self, mode):
        if mode in ("CHASE", "SCATTER", "FRIGHTENED"):
            self.mode = mode

    def reset_to_spawn(self):
        self.tile_x, self.tile_y = self.spawn_tile
        self._move_timer = 0.0

    def is_frightened(self):
        return self.mode == "FRIGHTENED"

    def _is_walkable(self, grid, tile):
        tx, ty = tile
        return (
            0 <= ty < len(grid)
            and 0 <= tx < len(grid[0])
            and grid[ty][tx] != Tile.WALL
        )

    def _project_player(self, player_tile, player_direction, distance):
        px, py = player_tile
        if player_direction == Direction.UP:
            py -= distance
        elif player_direction == Direction.DOWN:
            py += distance
        elif player_direction == Direction.LEFT:
            px -= distance
        elif player_direction == Direction.RIGHT:
            px += distance
        return (px, py)

    def _normalize_target(self, target, grid):
        tx = _clamp(target[0], 0, len(grid[0]) - 1)
        ty = _clamp(target[1], 0, len(grid) - 1)
        if self._is_walkable(grid, (tx, ty)):
            return (tx, ty)
        for radius in range(1, 6):
            for oy in range(-radius, radius + 1):
                for ox in range(-radius, radius + 1):
                    candidate = (tx + ox, ty + oy)
                    if self._is_walkable(grid, candidate):
                        return candidate
        return self.get_tile()

    def _fallback_step(self, grid):
        x, y = self.get_tile()
        candidates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        random.shuffle(candidates)
        for candidate in candidates:
            if self._is_walkable(grid, candidate):
                return candidate
        return (x, y)

    def _get_chase_target(self, player_tile, player_direction, blinky_tile):
        return player_tile

    def _get_target(self, player_tile, player_direction, blinky_tile, grid):
        if self.mode == "SCATTER":
            target = self.scatter_target
        elif self.mode == "FRIGHTENED":
            return None
        else:
            target = self._get_chase_target(player_tile, player_direction, blinky_tile)
        return self._normalize_target(target, grid)

    def update(self, grid, player_tile, player_direction, blinky_tile=None, delta=0.0):
        self._move_timer += delta
        mode_speed = self.move_delay * (1.6 if self.mode == "FRIGHTENED" else 1.0)
        if self._move_timer < mode_speed:
            return
        self._move_timer = 0.0

        if self.mode == "FRIGHTENED":
            next_tile = self._fallback_step(grid)
        else:
            start = self.get_tile()
            target = self._get_target(player_tile, player_direction, blinky_tile, grid)
            path = a_star(grid, start, target)

            if path is None or len(path) < 2:
                next_tile = self._fallback_step(grid)
            else:
                next_tile = path[1]

        self.tile_x, self.tile_y = next_tile


class Blinky(GhostBase):
    def __init__(self, tile_size, spawn_tile):
        super().__init__("Blinky", "red", tile_size, spawn_tile, scatter_target=(26, 1))

    def _get_chase_target(self, player_tile, player_direction, blinky_tile):
        return player_tile


class Pinky(GhostBase):
    def __init__(self, tile_size, spawn_tile):
        super().__init__("Pinky", "pink", tile_size, spawn_tile, scatter_target=(1, 1))

    def _get_chase_target(self, player_tile, player_direction, blinky_tile):
        return self._project_player(player_tile, player_direction, 4)


class Inky(GhostBase):
    def __init__(self, tile_size, spawn_tile):
        super().__init__("Inky", "cyan", tile_size, spawn_tile, scatter_target=(26, 29))

    def _get_chase_target(self, player_tile, player_direction, blinky_tile):
        if blinky_tile is None:
            return player_tile
        ahead = self._project_player(player_tile, player_direction, 2)
        vx = ahead[0] - blinky_tile[0]
        vy = ahead[1] - blinky_tile[1]
        return (ahead[0] + vx, ahead[1] + vy)


class Clyde(GhostBase):
    def __init__(self, tile_size, spawn_tile):
        super().__init__("Clyde", "orange", tile_size, spawn_tile, scatter_target=(1, 29))

    def _get_chase_target(self, player_tile, player_direction, blinky_tile):
        gx, gy = self.get_tile()
        px, py = player_tile
        if abs(gx - px) + abs(gy - py) <= 8:
            return self.scatter_target
        return player_tile
