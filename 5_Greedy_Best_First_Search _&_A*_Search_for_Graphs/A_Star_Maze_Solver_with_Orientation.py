import math
import heapq

class Node:
    def __init__(self, x, y, orientation, parent=None):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def solve_maze(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])

    orientations = ['N', 'E', 'S', 'W']
    deltas = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}

    def is_valid(x, y):
        return 0 <= x < cols and 0 <= y < rows and maze[y][x] == 0

    def heuristic(x, y):
        return math.sqrt((goal[0] - x)**2 + (goal[1] - y)**2)

    start_node = Node(start[0], start[1], start[2])
    start_node.h = heuristic(start_node.x, start_node.y)
    start_node.f = start_node.h

    open_set = [(start_node.f, start_node)]
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)[1]

        if (current.x, current.y) == goal:
            path = []
            cost = current.g
            while current:
                path.append((current.x, current.y, current.orientation))
                current = current.parent
            return path[::-1], cost

        closed_set.add((current.x, current.y, current.orientation))

        idx = orientations.index(current.orientation)
        for new_ori in [orientations[(idx-1)%4], orientations[(idx+1)%4]]:
            neighbor = Node(current.x, current.y, new_ori, current)
            neighbor.g = current.g + 1
            neighbor.h = heuristic(neighbor.x, neighbor.y)
            neighbor.f = neighbor.g + neighbor.h

            if (neighbor.x, neighbor.y, neighbor.orientation) not in closed_set:
                heapq.heappush(open_set, (neighbor.f, neighbor))

        dx, dy = deltas[current.orientation]
        dist = 0
        while True:
            nx, ny = current.x + dx*(dist+1), current.y + dy*(dist+1)
            if not is_valid(nx, ny):
                break
            dist += 1
            neighbor = Node(nx, ny, current.orientation, current)
            neighbor.g = current.g + dist
            neighbor.h = heuristic(nx, ny)
            neighbor.f = neighbor.g + neighbor.h

            if (nx, ny, current.orientation) not in closed_set:
                heapq.heappush(open_set, (neighbor.f, neighbor))

    return None, None

maze = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,0,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,1,0,1,0,0,1,0,1,0,0,0],
    [1,1,1,0,1,0,1,0,1,1,0,1,0,1,1],
    [0,0,0,0,1,0,0,0,1,0,0,1,0,1,0],
    [0,1,1,1,1,1,1,1,1,0,1,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [1,1,1,1,1,0,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [1,1,1,1,1,0,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,1,0,0,0,0,0,0,0,0,1,0],
    [0,1,1,0,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

start = (0, 0, 'E')
goal = (14, 14)

path, cost = solve_maze(maze, start, goal)

print("Path from start to goal:")
for step in path:
    print(step)
print("Total cost:", cost)
