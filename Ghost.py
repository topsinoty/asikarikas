class Ghost:
    """Create a ghost with a specific color which is assigned by its type"""

    def __init__(self, type: int):
        match type:
            case 1:
                print("Blinky")
            case 2:
                print("Inky")
            case 3:
                print("Red Fuck")
            case 4:
                print("I forgot the 4th color.")
            case _:
                raise ValueError(f"Invalid Ghost type: {type}")
