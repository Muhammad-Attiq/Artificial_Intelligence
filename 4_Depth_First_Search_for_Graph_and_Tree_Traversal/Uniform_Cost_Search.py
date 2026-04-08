import math

class Node:
    def __init__(self, state, parent, actions, totalCost):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.totalCost = totalCost

def findMin(frontier):
    minV = math.inf
    node = ''
    for i in frontier:
        if minV > frontier[i][1]:
            minV = frontier[i][1]
            node = i
    return node

def actionSequence(graph, initialState, goalState):
    solution = [goalState]
    currentParent = graph[goalState].parent
    while currentParent != None:
        solution.append(currentParent)
        currentParent = graph[currentParent].parent
    solution.reverse()
    return solution

def UCS():
    initialState = 'C'
    goalState = 'B'

    graph = {
        'A': Node('A', None, [('B', 6), ('C', 9), ('E', 1)], 0),
        'B': Node('B', None, [('A', 6), ('D', 3), ('E', 4)], 0),
        'C': Node('C', None, [('A', 9), ('F', 2), ('G', 3)], 0),
        'D': Node('D', None, [('B', 3), ('E', 5), ('F', 7)], 0),
        'E': Node('E', None, [('A', 1), ('B', 4), ('D', 5), ('F', 6)], 0),
        'F': Node('F', None, [('C', 2), ('E', 6), ('D', 7)], 0),
        'G': Node('G', None, [('C', 3)], 0)
    }

    frontier = dict()
    frontier[initialState] = (None, 0)
    explored = []

    while len(frontier) != 0:
        currentNode = findMin(frontier)
        del frontier[currentNode]

        if graph[currentNode].state == goalState:
            return actionSequence(graph, initialState, goalState)

        explored.append(currentNode)

        for child in graph[currentNode].actions:
            currentCost = child[1] + graph[currentNode].totalCost
            if child[0] not in frontier and child[0] not in explored:
                graph[child[0]].parent = currentNode
                graph[child[0]].totalCost = currentCost
                frontier[child[0]] = (graph[child[0]].parent, graph[child[0]].totalCost)
            elif child[0] in frontier:
                if frontier[child[0]][1] < currentCost:
                    graph[child[0]].parent = frontier[child[0]][0]
                    graph[child[0]].totalCost = frontier[child[0]][1]
                else:
                    frontier[child[0]] = (currentNode, currentCost)
                    graph[child[0]].parent = frontier[child[0]][0]
                    graph[child[0]].totalCost = frontier[child[0]][1]

solution = UCS()
print(solution)
