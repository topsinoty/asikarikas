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
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
            if maze[ny][nx] != map.Tile.WALL:
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

    return None
