import pygame
from direction import Direction
from player import Player
from map import TileGridGenerator, Tile
from Ghost import Ghost

TILE_SIZE = 24
FPS = 60
FRIGHTENED_DURATION = 8.0
SCATTER_CHASE_INTERVAL = 7.0
SCORE_PELLET = 10
SCORE_POWER = 50
SCORE_GHOST = 200
STARTING_LIVES = 3

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont("consolas", 22)
small_font = pygame.font.SysFont("consolas", 16)

generator = TileGridGenerator()
grid = generator.generate()

def find_ghost_spawns(grid, count=4):
    ghost_tiles = []
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile == Tile.GHOST:
                ghost_tiles.append((x, y))
    ghost_tiles.sort(key=lambda point: (point[1], point[0]))
    if len(ghost_tiles) < count:
        return [(1 + i, 1) for i in range(count)]
    start = len(ghost_tiles) // 2 - count // 2
    return ghost_tiles[start : start + count]


def find_player_spawn(grid):
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile in (Tile.PELLET, Tile.POWER, Tile.PATH):
                return (x, y)
    return (1, 1)


def count_remaining_pellets(grid):
    return sum(1 for row in grid for tile in row if tile in (Tile.PELLET, Tile.POWER))


def draw_hud(surface, score, lives, frightened_timer, state):
    hud = f"Score: {score}   Lives: {lives}"
    if frightened_timer > 0:
        hud += f"   Frightened: {frightened_timer:0.1f}s"
    surface.blit(font.render(hud, True, "white"), (8, 8))

    controls = "WASD move | Power pellet turns ghosts frightened | ESC quit"
    surface.blit(small_font.render(controls, True, "white"), (8, 34))

    if state == "WON":
        message = "YOU WIN - Press R to restart or ESC to quit"
        surface.blit(font.render(message, True, "yellow"), (220, 360))
    elif state == "GAME_OVER":
        message = "GAME OVER - Press R to restart or ESC to quit"
        surface.blit(font.render(message, True, "red"), (200, 360))


def reset_round(player, ghosts, player_spawn):
    player.reset(player_spawn[0], player_spawn[1])
    for ghost in ghosts:
        ghost.reset_to_spawn()


def reset_game_state():
    local_grid = generator.generate()
    local_player_spawn = find_player_spawn(local_grid)
    local_player = Player(local_player_spawn[0], local_player_spawn[1], TILE_SIZE)
    local_ghost_spawns = find_ghost_spawns(local_grid, 4)
    local_ghosts = [Ghost(i + 1, TILE_SIZE, local_ghost_spawns[i]) for i in range(4)]
    return local_grid, local_player, local_player_spawn, local_ghosts


def consume_player_tile(grid, tile):
    x, y = tile
    if grid[y][x] == Tile.PELLET:
        grid[y][x] = Tile.PATH
        return SCORE_PELLET, False
    if grid[y][x] == Tile.POWER:
        grid[y][x] = Tile.PATH
        return SCORE_POWER, True
    return 0, False


ghost_spawns = find_ghost_spawns(grid, 4)
ghosts = [Ghost(i + 1, TILE_SIZE, ghost_spawns[i]) for i in range(4)]
player_spawn = find_player_spawn(grid)
player = Player(player_spawn[0], player_spawn[1], TILE_SIZE)
player_pos = player.get_pos()
score = 0
lives = STARTING_LIVES
state = "PLAYING"
mode_timer = 0.0
ghost_mode = "CHASE"
frightened_timer = 0.0
remaining_pellets = count_remaining_pellets(grid)


def draw_map(surface, grid):
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):

            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            if tile == Tile.WALL:
                pygame.draw.rect(surface, "blue", rect)

            elif tile == Tile.PELLET:
                pygame.draw.circle(surface, "white", rect.center, TILE_SIZE // 8)

            elif tile == Tile.POWER:
                pygame.draw.circle(surface, "white", rect.center, TILE_SIZE // 4)

            elif tile == Tile.GHOST:
                pygame.draw.rect(surface, "gray", rect)

            else:
                pygame.draw.rect(surface, "black", rect)


while running:

    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r and state in ("WON", "GAME_OVER"):
                grid, player, player_spawn, ghosts = reset_game_state()
                player_pos = player.get_pos()
                score = 0
                lives = STARTING_LIVES
                state = "PLAYING"
                mode_timer = 0.0
                ghost_mode = "CHASE"
                frightened_timer = 0.0
                remaining_pellets = count_remaining_pellets(grid)

    screen.fill("black")

    draw_map(screen, grid)

    if state == "PLAYING":
        keys = pygame.key.get_pressed()
        move_direction = Direction.NONE

        if keys[pygame.K_w]:
            move_direction = Direction.UP
        elif keys[pygame.K_s]:
            move_direction = Direction.DOWN
        elif keys[pygame.K_a]:
            move_direction = Direction.LEFT
        elif keys[pygame.K_d]:
            move_direction = Direction.RIGHT

        player.move(move_direction, grid)
        player_tile = player.get_tile()

        score_gain, triggered_power = consume_player_tile(grid, player_tile)
        if score_gain:
            score += score_gain
            remaining_pellets -= 1

        if triggered_power:
            frightened_timer = FRIGHTENED_DURATION

        if remaining_pellets <= 0:
            state = "WON"

        if frightened_timer > 0:
            frightened_timer = max(0.0, frightened_timer - dt)
            current_ghost_mode = "FRIGHTENED"
        else:
            mode_timer += dt
            if mode_timer >= SCATTER_CHASE_INTERVAL:
                ghost_mode = "SCATTER" if ghost_mode == "CHASE" else "CHASE"
                mode_timer = 0.0
            current_ghost_mode = ghost_mode

        blinky_tile = ghosts[0].get_tile()
        for ghost in ghosts:
            ghost.set_mode(current_ghost_mode)
            ghost.update(
                grid=grid,
                player_tile=player_tile,
                player_direction=player.last_direction,
                blinky_tile=blinky_tile,
                delta=dt,
            )

        for ghost in ghosts:
            if ghost.get_tile() != player_tile:
                continue

            if ghost.is_frightened():
                score += SCORE_GHOST
                ghost.reset_to_spawn()
                continue

            lives -= 1
            frightened_timer = 0.0
            mode_timer = 0.0
            ghost_mode = "CHASE"
            if lives <= 0:
                player.kill()
                state = "GAME_OVER"
            else:
                reset_round(player, ghosts, player_spawn)
            break

    player_pos = player.get_pos()
    pygame.draw.circle(screen, "red", player_pos, TILE_SIZE // 2)

    for ghost in ghosts:
        ghost_color = "blue" if ghost.is_frightened() else ghost.color
        pygame.draw.circle(screen, ghost_color, ghost.get_pos(), TILE_SIZE // 2)

    draw_hud(screen, score, lives, frightened_timer, state)

    pygame.display.flip()

pygame.quit()
