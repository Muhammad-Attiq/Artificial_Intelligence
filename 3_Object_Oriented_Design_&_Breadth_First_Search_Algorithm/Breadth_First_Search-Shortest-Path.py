class Node:
    def __init__(self, state, parent, actions):
        self.state = state
        self.parent = parent
        self.actions = actions


def actionSequence(graph, initialState, goalState):
    solution = [goalState]
    currentParent = graph[goalState].parent

    while currentParent is not None:
        solution.append(currentParent)
        currentParent = graph[currentParent].parent

    solution.reverse()
    return solution


def BFS():
    initialState = 'Arad'
    goalState = 'Bucharest'
    graph = {
        'Arad': Node('Arad', None, ['Zerind', 'Sibiu', 'Timisoara']),
        'Zerind': Node('Zerind', None, ['Arad', 'Oradea']),
        'Oradea': Node('Oradea', None, ['Zerind', 'Sibiu']),
        'Sibiu': Node('Sibiu', None, ['Arad', 'Oradea', 'Fagaras', 'Rimnicu Vilcea']),
        'Timisoara': Node('Timisoara', None, ['Arad', 'Lugoj']),
        'Lugoj': Node('Lugoj', None, ['Timisoara', 'Mehadia']),
        'Mehadia': Node('Mehadia', None, ['Lugoj', 'Drobeta']),
        'Drobeta': Node('Drobeta', None, ['Mehadia', 'Craiova']),
        'Craiova': Node('Craiova', None, ['Drobeta', 'Rimnicu Vilcea', 'Pitesti']),
        'Rimnicu Vilcea': Node('Rimnicu Vilcea', None, ['Sibiu', 'Craiova', 'Pitesti']),
        'Fagaras': Node('Fagaras', None, ['Sibiu', 'Bucharest']),
        'Pitesti': Node('Pitesti', None, ['Rimnicu Vilcea', 'Craiova', 'Bucharest']),
        'Bucharest': Node('Bucharest', None, ['Fagaras', 'Pitesti', 'Giurgiu', 'Urziceni']),
        'Giurgiu': Node('Giurgiu', None, ['Bucharest']),
        'Urziceni': Node('Urziceni', None, ['Bucharest', 'Hirsova', 'Vaslui']),
        'Hirsova': Node('Hirsova', None, ['Urziceni', 'Eforie']),
        'Eforie': Node('Eforie', None, ['Hirsova']),
        'Vaslui': Node('Vaslui', None, ['Urziceni', 'Iasi']),
        'Iasi': Node('Iasi', None, ['Vaslui', 'Neamt']),
        'Neamt': Node('Neamt', None, ['Iasi'])
    }

    frontier = [initialState]
    explored = []

    while frontier:
        currentNode = frontier.pop(0)
        explored.append(currentNode)

        for child in graph[currentNode].actions:
            if child not in frontier and child not in explored:
                graph[child].parent = currentNode

                if child == goalState:
                    return actionSequence(graph, initialState, goalState)

                frontier.append(child)

    return None


solution = BFS()
print("Shortest Path:", solution)
