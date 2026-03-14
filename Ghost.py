from math import floor
from re import error
from Navigation import get_move as navigation_move


class Ghost:
    def __new__(cls, number, max_ghosts, num_ghost):
        ghosts = {1: Blinky, 2: Inky, 3: Pinky, 4: Clyde}
        if number in ghosts:
            return ghosts[number](max_ghosts, num_ghost)
        else:
            raise ValueError("Invalid ghost number. Choose 1-4.")


class GhostBase:
    width = 25
    height = 25
    facing = 0  # North, South, East, West

    def __init__(self, name, max_ghosts=4, num_ghost=1, **attributes):
        # Name and attributes unique to each ghost
        self.name = name
        self.attribute = attributes

        # Position calculated based on total ghosts and ghost index
        self.position = self.get_init_pos(max_ghosts, num_ghost)

    def get_init_pos(self, max_ghosts, num_ghost):
        """
        Calculate initial position based on the ghost index and total ghosts.
        Spreads ghosts evenly horizontally from start point (0,0).
        """
        start_x = 0
        start_y = 0
        spacing = 40  # horizontal spacing between ghosts
        x = start_x + spacing * (num_ghost - 1)
        y = start_y
        return [x, y]

    def get_pos(self):
        # chatgpt: Generate a python match case 0-3 north south east west respectevely based on this return (self.position[0], floor(self.position[1] - 1))
        match self.facing:
            case 0:  # North
                return (self.position[0], floor(self.position[1] - 1))
            case 1:  # South
                return (self.position[0], floor(self.position[1] + 1))
            case 2:  # East
                return (floor(self.position[0] + 1), self.position[1])
            case 3:  # West
                return (floor(self.position[0] - 1), self.position[1])
            case _:  # invalid facing
                raise ValueError(f"Invalid facing: {self.facing}")

    def get_move(self, maze, pacman_pos=None):
        if pacman_pos is None:
            raise ValueError("No Pacman Pos")
        goal = pacman_pos

        return navigation_move(maze, self.get_pos(), goal)


class Blinky(GhostBase):
    def __init__(self, max_ghosts=4, num_ghost=1):
        # In all ghosts the idea to set "angry=False" was something I didn't know and was told to me in chatgpt
        super().__init__("Blinky", max_ghosts, num_ghost, angry=False)

    def get_move(self, maze, pacman_pos=None):
        return super().get_move(maze, pacman_pos)


class Inky(GhostBase):
    def __init__(self, max_ghosts=4, num_ghost=2):
        super().__init__("Inky", max_ghosts, num_ghost, chase=False)

    def get_move(self, maze, pacman_pos=None):
        if pacman_pos is None:
            raise ValueError("No Pacman Pos")
        goal = pacman_pos

        return navigation_move(maze, self.get_pos(), goal)


class Pinky(GhostBase):
    def __init__(self, max_ghosts=4, num_ghost=3):
        super().__init__("Pinky", max_ghosts, num_ghost)

    def get_move(self, maze, pacman_pos=None):
        if pacman_pos is None:
            raise ValueError("No Pacman Pos")
        goal = pacman_pos

        return navigation_move(maze, self.get_pos(), goal)


class Clyde(GhostBase):
    def __init__(self, max_ghosts=4, num_ghost=4):
        super().__init__("Clyde", max_ghosts, num_ghost, scatter=False)

    def get_move(self, maze, pacman_pos=None):
        if pacman_pos is None:
            raise ValueError("No Pacman Pos")
        # chatgpt: {I just gave it the GhostBase get_move with blinky's name}
        vector = (pacman_pos[0] - blinky_pos[0], pacman_pos[1] - blinky_pos[1])
        goal = (pacman_pos[0] + vector[0], pacman_pos[1] + vector[1])
        return navigation_move(maze, self.get_pos(), goal)
