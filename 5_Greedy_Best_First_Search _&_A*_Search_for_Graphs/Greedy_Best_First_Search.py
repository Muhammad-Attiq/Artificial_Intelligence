import math
import heapq

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.h = 0

    def __lt__(self, other):
        return self.h < other.h

def greedy_best_first_search(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])

    def is_valid(x, y):
        return 0 <= x < cols and 0 <= y < rows and maze[y][x] == 0

    def heuristic(x, y):
        return math.sqrt((goal[0] - x)**2 + (goal[1] - y)**2)

    start_node = Node(start[0], start[1])
    start_node.h = heuristic(start_node.x, start_node.y)

    open_set = [(start_node.h, start_node)]
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)[1]

        if (current.x, current.y) == goal:
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        closed_set.add((current.x, current.y))

        for dx, dy in [(0,-1), (1,0), (0,1), (-1,0)]:
            nx, ny = current.x + dx, current.y + dy
            if is_valid(nx, ny) and (nx, ny) not in closed_set:
                neighbor = Node(nx, ny, current)
                neighbor.h = heuristic(nx, ny)
                heapq.heappush(open_set, (neighbor.h, neighbor))

    return None

maze = [
    [0,0,0,0,0],
    [1,1,0,1,0],
    [0,0,0,1,0],
    [0,1,1,0,0],
    [0,0,0,0,0]
]

start = (0, 0)
goal = (4, 4)

path = greedy_best_first_search(maze, start, goal)

print("Path:")
for step in path:
    print(step)
