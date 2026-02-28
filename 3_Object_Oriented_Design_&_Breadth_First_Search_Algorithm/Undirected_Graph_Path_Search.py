graph = {
    '6': ['4'],
    '4': ['6', '3', '5'],
    '3': ['4', '2'],
    '5': ['4', '2', '1'],
    '2': ['3', '5', '1'],
    '1': ['5', '2']
}

def get_degrees(graph):
    for node, neighbors in graph.items():
        print(f"Node {node} degree: {len(neighbors)}")

def find_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]

    all_paths = []
    for node in graph[start]:
        if node not in path:
            new_paths = find_paths(graph, node, end, path)
            for p in new_paths:
                all_paths.append(p)
    return all_paths

get_degrees(graph)
paths = find_paths(graph, '6', '1')

print(f"\nAny path from 6 to 1: {paths[0]}")
print(f"All paths from 6 to 1: {paths}")
