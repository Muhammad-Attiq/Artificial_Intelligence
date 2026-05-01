import numpy as np

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.start = None
        self.goal = None

    def find_start_goal(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == 'S':
                    self.start = (i, j)
                elif self.maze[i][j] == 'G':
                    self.goal = (i, j)

    def distance_to_goal(self, pos):
        return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])

    def get_neighbors(self, pos):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []

        for dx, dy in directions:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                if self.maze[new_x][new_y] != 1:
                    neighbors.append((new_x, new_y))

        return neighbors

    def simple_hill_climbing(self):
        current = self.start
        path = [current]
        visited = set([current])

        print("\n--- Simple Hill Climbing ---")

        while current != self.goal:
            neighbors = self.get_neighbors(current)
            current_dist = self.distance_to_goal(current)

            found_better = False
            for neighbor in neighbors:
                if neighbor not in visited:
                    neighbor_dist = self.distance_to_goal(neighbor)
                    if neighbor_dist < current_dist:
                        path.append(neighbor)
                        visited.add(neighbor)
                        current = neighbor
                        found_better = True
                        print(f"Moving to {current}, Distance: {neighbor_dist}")
                        break

            if not found_better:
                print("Stuck! No better neighbor found")
                break

        return path, len(path) - 1

    def steepest_hill_climbing(self):
        current = self.start
        path = [current]
        visited = set([current])

        print("\n--- Steepest Ascent Hill Climbing ---")

        while current != self.goal:
            neighbors = self.get_neighbors(current)
            current_dist = self.distance_to_goal(current)

            unvisited_neighbors = [n for n in neighbors if n not in visited]

            if not unvisited_neighbors:
                print("Stuck! No unvisited neighbors")
                break

            best_neighbor = None
            best_dist = float('inf')

            for neighbor in unvisited_neighbors:
                dist = self.distance_to_goal(neighbor)
                if dist < best_dist:
                    best_dist = dist
                    best_neighbor = neighbor

            if best_dist < current_dist:
                path.append(best_neighbor)
                visited.add(best_neighbor)
                current = best_neighbor
                print(f"Moving to {current}, Distance: {best_dist}")
            else:
                print("Stuck! No better neighbor found")
                break

        return path, len(path) - 1

    def print_solution(self, path, steps, algorithm_name):
        print(f"\n{algorithm_name}:")
        print(f"Path length: {steps} steps")
        print(f"Path: {path}")

        maze_copy = [row[:] for row in self.maze]
        for i, pos in enumerate(path):
            if pos == self.start:
                maze_copy[pos[0]][pos[1]] = 'S'
            elif pos == self.goal:
                maze_copy[pos[0]][pos[1]] = 'G'
            else:
                maze_copy[pos[0]][pos[1]] = '*'

        print("\nMaze with path (* = path):")
        for row in maze_copy:
            print(' '.join(str(cell) for cell in row))

    def solve(self):
        self.find_start_goal()

        if not self.start or not self.goal:
            print("Error: Start (S) or Goal (G) not found!")
            return

        print(f"Start: {self.start}")
        print(f"Goal: {self.goal}")

        path1, steps1 = self.simple_hill_climbing()
        self.print_solution(path1, steps1, "Simple Hill Climbing")

        path2, steps2 = self.steepest_hill_climbing()
        self.print_solution(path2, steps2, "Steepest Ascent Hill Climbing")


def create_test_maze():
    return [
        ['S', 0,   0,   0],
        [1,   1,   0,   1],
        [0,   0,   0,   0],
        [0,   1,   0,  'G']
    ]


if __name__ == "__main__":
    print("=" * 50)
    print("MAZE SOLVER - HILL CLIMBING ALGORITHMS")
    print("=" * 50)

    maze = create_test_maze()

    print("\nMaze Layout:")
    print("S = Start, G = Goal, 1 = Wall, 0 = Path")
    for row in maze:
        print(row)

    solver = MazeSolver(maze)
    solver.solve()
