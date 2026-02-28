from collections import deque

graph={'S':['A'],'A':['S','B'],
       'B':['A','C'],'C':['B','D','E'],
       'D':['C','F'],'E':['C','G'],
       'F':['D','H'],'G':['E','I'],
       'H':['F','J'],'I':['G','K'],
       'J':['H','L'],'K':['I','L'],
       'L':['J','K','M'],'M':['L','G1'],
       'G1':['M']}

def bfs(graph,start,goal):
    queue=deque([[start]])
    visited={start}
    while queue:
        path=queue.popleft()
        node=path[-1]
        if node==goal:
            return path
        for neighbor in graph.get(node,[]):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path=list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None

solution=bfs(graph,'S','G1')
print(solution)
