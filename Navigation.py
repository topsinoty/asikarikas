import heapq
import map


class Node:
    def __init__(self, a_pos, b_pos, time=0, distance=-1, parents=None):
        self.a_pos = a_pos
        self.b_pos = b_pos
        self.time = time
        self.distance = distance
        self.parents = parents or []

    def f(self):
        return self.time + self.distance

    def __lt__(self, other):
        return self.f() < other.f()


def heuristic(a_pos, goal):
    # Manhattan distance as a simple heuristic
    return abs(a_pos[0] - goal[0]) + abs(a_pos[1] - goal[1])


def get_neighbors(pos, maze):
    neighbors = []
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
            if maze[nx][ny] != map.Tile.WALL:  # assuming 1 is wall
                neighbors.append((nx, ny))
    return neighbors


def a_star(maze, start, goal):
    open_heap = []
    start_node = Node(a_pos=start, b_pos=goal, time=0, distance=heuristic(start, goal))
    heapq.heappush(open_heap, start_node)

    closed_set = set()

    while open_heap:
        current = heapq.heappop(open_heap)

        if current.a_pos == goal:
            # Reconstruct path
            path = current.parents + [current.a_pos]
            return path

        if current.a_pos in closed_set:
            continue

        closed_set.add(current.a_pos)

        for neighbor in get_neighbors(current.a_pos, maze):
            if neighbor in closed_set:
                continue
            g = current.time + 1
            h = heuristic(neighbor, goal)
            neighbor_node = Node(
                a_pos=neighbor,
                b_pos=goal,
                time=g,
                distance=h,
                parents=current.parents + [current.a_pos],
            )
            heapq.heappush(open_heap, neighbor_node)

    return None  # No path found


# get_direction function, takes in variable, touple of touples the each position the object will be in as it moves. I need the direction of the first movement the object will make. up is 1, down 2, left 3, right 4 in python
def get_direction(positions):
    if len(positions) < 2:
        return None  # Not enough positions to determine direction

    x1, y1 = positions[0]
    x2, y2 = positions[1]

    if x2 == x1 and y2 < y1:
        return 1  # Up
    elif x2 == x1 and y2 > y1:
        return 2  # Down
    elif y2 == y1 and x2 < x1:
        return 3  # Left
    elif y2 == y1 and x2 > x1:
        return 4  # Right
    else:
        return None  # Diagonal or invalid movement


if __name__ == "__main__":
    maze = [
        [0, 0, 0, 0, 1],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]

    start = (0, 0)
    goal = (4, 4)
    path = a_star(maze, start, goal)
    print("Path:", get_direction(path))
