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

    def get_move(self, pacman_pos=None, ghost_pos=None):
        # This function was inspired by chatgpt when I asked what would be a smart way to combine, my init functions into GhostBase
        """
        Default chase behavior (override in subclasses).
        """
        raise NotImplementedError("Each ghost must implement its own chase method.")


class Blinky(GhostBase):
    def __init__(self, max_ghosts=4, num_ghost=1):
        # In all ghosts the idea to set "angry=False" was something I didn't know and was told to me in chatgpt
        super().__init__("Blinky", max_ghosts, num_ghost, angry=False)

    def get_move(self, pacman_pos=None, ghost_pos=None):
        return "Chasing Pac-Man aggressively!"


class Inky(GhostBase):
    def __init__(self, max_ghosts=4, num_ghost=2):
        super().__init__("Inky", max_ghosts, num_ghost, chase=False)

    def get_move(self, pacman_pos=None, ghost_pos=None):
        return "Moves unpredictably!"


class Pinky(GhostBase):
    def __init__(self, max_ghosts=4, num_ghost=3):
        super().__init__("Pinky", max_ghosts, num_ghost)

    def get_move(self, pacman_pos=None, ghost_pos=None):
        return "Tries to ambush Pac-Man!"


class Clyde(GhostBase):
    def __init__(self, max_ghosts=4, num_ghost=4):
        super().__init__("Clyde", max_ghosts, num_ghost, scatter=False)

    def get_move(self, pacman_pos=None, ghost_pos=None):
        return "Random but cautious movement."
