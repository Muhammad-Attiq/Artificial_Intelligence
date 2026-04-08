from collections import deque

graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['G'],
    'D': ['E'],
    'E': [],
    'G': []
}

def bfs(graph, start, goal):
    visited = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            if node == goal:
                break
            queue.extend(graph[node])
    return visited


def dfs(graph, start, goal):
    visited = []
    stack = [start]

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.append(node)

            if node == goal:
                break

            stack.extend(reversed(graph[node]))

    return visited


start = 'A'
goal = 'G'

bfs_nodes = bfs(graph, start, goal)
dfs_nodes = dfs(graph, start, goal)

print("BFS visited:", bfs_nodes)
print("BFS nodes count:", len(bfs_nodes))

print("DFS visited:", dfs_nodes)
print("DFS nodes count:", len(dfs_nodes))
