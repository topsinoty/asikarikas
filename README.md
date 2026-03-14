# Asikarikas (Pac-Man Style Prototype)

Grid-based Pac-Man style prototype built with Python and Pygame.

## Features

- Procedural tile-map generation (`wall`, `path`, `pellet`, `power`, `ghost box`).
- Player movement with wall collision checks.
- Pellet consumption and scoring.
- Four ghosts with distinct chase behavior:
  - `Blinky`: directly chases player.
  - `Pinky`: targets 4 tiles ahead of player direction.
  - `Inky`: uses vector logic based on Blinky + player projection.
  - `Clyde`: chases from far away, scatters when too close.
- Ghost pathing uses A* (`Navigation.py`).
- Power-pellet frightened mode with slower ghosts that can be eaten.
- Chase/scatter mode switching in the main loop.
- Lives system, win state, and game-over state with restart support.

## Requirements

- Python 3.10+ (tested with newer versions)
- Pygame 2.6.1

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Controls

- `W`: move up
- `S`: move down
- `A`: move left
- `D`: move right
- `R`: restart after win/game over
- `ESC`: quit
- Close window / `X`: quit

## Project Structure

- `main.py`: game loop, rendering, pellet scoring, frightened mode, collisions, lives/state flow.
- `map.py`: procedural tile grid generation and tile enum definitions.
- `player.py`: player tile movement and state.
- `Ghost.py`: ghost classes and AI targeting logic.
- `Navigation.py`: A* implementation used by ghosts.
- `direction.py`: movement direction enum.

## Ghost AI Notes

- Ghosts move tile-by-tile at a fixed interval (`move_delay`).
- Target tiles are clamped to map bounds and normalized to nearest walkable tile.
- If no A* path is found, ghosts choose a random valid neighboring tile.
- Global mode toggles between `CHASE` and `SCATTER` every 7 seconds in `main.py`.
- During `FRIGHTENED`, ghosts move slower and use random fallback movement.
- Colliding with frightened ghosts awards bonus points and returns them to spawn.

## Known Limitations

- No title screen or level progression yet.
- Ghost "eyes returning home" behavior is simplified to immediate respawn.
- No arcade tunnel wrap-around yet.

## Next Practical Improvements

1. Add level progression and increasing ghost speed per level.
2. Add tunnel wrap-around movement on side corridors.
3. Add fruit/bonus pickups and high-score persistence.
4. Add deterministic map seed option for debugging and tests.
