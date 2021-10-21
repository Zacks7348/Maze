from maze.maze import Maze, Cell
from maze.utils import PriorityQueue, heuristic


class MazeSolverMethods:
    DFS = 'DFS'
    BFS = 'BFS'
    UCS = 'UCS'
    ASTAR = 'ASTAR'


class MazeSolver:
    """
    Base class for maze solvers
    """

    def __init__(self, maze: Maze, **kwargs) -> None:
        self.maze: Maze = maze
        self.solution = []
        self.solution_cost = 0
        self.nodes_expanded = 0
        self.frontier = None
        self.explored = None
        self.parent = {}

        self.step_mode = kwargs.pop('step', False)
        self.finished = False

    def backtrack_solution(self):
        p = self.maze.finish_pos
        while p and p != self.maze.start_pos:
            self.solution.append(p)
            p = self.parent.get(p, None)
        self.solution.reverse()


class DFSMazeSolver(MazeSolver):
    def __init__(self, maze, **kwargs) -> None:
        super().__init__(maze, **kwargs)
        self.frontier = [self.maze.start_pos]
        self.explored = set()
        self.explored.add(self.maze.start_pos)
        self.nodes_expanded += 1

        if self.step_mode:
            return
        while not self.finished:
            self.step()

    def step(self):
        if self.finished:
            return None
        if not self.frontier:
            self.finished = True
            return None
        p = self.frontier.pop()
        if p == self.maze.finish_pos:
            self.backtrack_solution()
            self.solution_cost = len(self.solution)
            self.finished = True
            return None
        res = []
        for neighbor in self.maze.get_neighboring_passages(p):
            if not neighbor in self.explored:
                self.explored.add(neighbor)
                self.parent[neighbor] = p
                self.frontier.append(neighbor)
                self.nodes_expanded += 1
                res.append(neighbor)
        return res  # Return nodes we just added to frontier


class BFSMazeSolver(MazeSolver):
    def __init__(self, maze: Maze, **kwargs) -> None:
        super().__init__(maze, **kwargs)
        self.frontier = []
        self.explored = set()
        self.frontier.append(self.maze.start_pos)

        if self.step_mode:
            return

        while not self.finished:
            self.step()

    def step(self):
        if self.finished:
            return None
        if not self.frontier:
            self.finished = True
            return None
        p = self.frontier.pop(0)
        self.explored.add(p)
        res = []
        for neighbor in self.maze.get_neighboring_passages(p):
            if not neighbor in self.explored:
                res.append(neighbor)
                self.nodes_expanded += 1
                self.explored.add(neighbor)
                self.parent[neighbor] = p
                if neighbor == self.maze.finish_pos:
                    self.finished = True
                    self.backtrack_solution()
                    self.solution_cost = len(self.solution)
                    return res
                self.frontier.append(neighbor)
        return res


class UCSMazeSolver(MazeSolver):
    def __init__(self, maze: Maze, **kwargs) -> None:
        super().__init__(maze, **kwargs)
        self.frontier = PriorityQueue()
        self.frontier.add(maze.start_pos, 0)
        self.costs = {self.maze.start_pos: 0}
        self.nodes_expanded = 1

        if self.step_mode:
            return

    def step(self):
        if self.finished:
            return None
        if self.frontier.is_empty:
            self.finished = True
            return None
        cost, p = self.frontier.pop()
        if p == self.maze.finish_pos:
            self.backtrack_solution()
            self.solution_cost = len(self.solution)
            self.finished = True
            return None
        res = []
        for neighbor in self.maze.get_neighboring_passages(p):
            new_cost = cost+1
            if not neighbor in self.costs or new_cost < self.costs.get(neighbor, new_cost):
                self.costs[neighbor] = new_cost
                self.frontier.add(neighbor, new_cost)
                self.parent[neighbor] = p
                self.nodes_expanded += 1
                res.append(neighbor)
        return res


class ASTARMazeSolver(MazeSolver):
    def __init__(self, maze: Maze, **kwargs) -> None:
        super().__init__(maze, **kwargs)
        self.heuristic = kwargs.pop('heuristic', 'euclidian')
        self.frontier = PriorityQueue()
        self.frontier.add(self.maze.start_pos, 0)
        self.costs = {self.maze.start_pos: 0}
        self.nodes_expanded = 1

        if self.step_mode:
            return
        while not self.finished:
            self.step()

    def step(self):
        if self.finished:
            return None
        if self.frontier.is_empty:
            self.finished = True
            return None
        _, p = self.frontier.pop()
        if p == self.maze.finish_pos:
            self.backtrack_solution()
            self.solution_cost = len(self.solution)
            self.finished = True
            return None
        res = []
        for neighbor in self.maze.get_neighboring_passages(p):
            new_cost = self.costs[p] + 1
            if not neighbor in self.costs or new_cost < self.costs.get(neighbor, new_cost):
                self.nodes_expanded += 1
                self.costs[neighbor] = new_cost
                self.frontier.add(
                    neighbor, new_cost+heuristic(neighbor, self.maze.finish_pos, self.heuristic))
                self.parent[neighbor] = p
                res.append(neighbor)
        return res