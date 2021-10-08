"""
This file contains different search algorithms implemented to find a solution
to a :class:`Maze`
"""

import pdb
from time import time
import math

from maze.maze import Maze, Position
from maze.utils import PriorityQueue, backtrack_solution, heuristic


class SearchAlgorithms():
    DEPTH = 'depth'
    BREADTH = 'breadth'
    UNIFORM = 'uniform'
    ASTAR = 'astar'


class Heuristic:
    EUCLIDEAN = 'euclidian'
    MANHATTAN = 'manhattan'


# ------------------------------------------------------------------------
# UNINFORMED ALGORITHMS
# ------------------------------------------------------------------------


def depth_first_search(maze: Maze, **kwargs):
    """
    Find a solution to a maze using Depth-First Search

    Returns
    -------
    solution: dict
        A dictionary
    """
    start = time()
    solution = {
        'path': None,
        'path-cost': None,
        'nodes-expanded': None,
        'time-elapsed': None
    }
    frontier = [maze.start_pos]  # Stack
    explored = set()
    parent = {}

    explored.add(maze.start_pos)

    while frontier:  # While Stack is not empty
        p = frontier.pop()
        if p == maze.finish_pos:
            solution['time-elapsed'] = time() - start
            solution['path'] = backtrack_solution(p, parent, maze)
            solution['path-cost'] = len(solution['path'])
            solution['nodes-expanded'] = len(explored)
            return solution
        for neighbor in maze.get_neighbors(p):
            if not neighbor in explored:
                explored.add(neighbor)
                parent[neighbor] = p
                frontier.append(neighbor)
    # Could not find a solution
    solution['time-elapsed'] = time_elapsed = time() - start
    solution['nodes-expanded'] = len(explored)
    return solution


def breadth_first_search(maze: Maze, **kwargs):
    """
    Traverse a maze using BFS.
    """
    start = time()
    solution = {
        'path': None,
        'path-cost': None,
        'nodes-expanded': None,
        'time-elapsed': None
    }
    frontier = []  # FIFO Queue
    explored = set()
    parent = {}

    frontier.append(maze.start_pos)

    while frontier:
        p = frontier.pop(0)
        explored.add(p)
        for neighbor in maze.get_neighbors(p):
            if not neighbor in explored:
                explored.add(neighbor)
                parent[neighbor] = p
                if neighbor == maze.finish_pos:
                    solution['time-elapsed'] = time() - start
                    solution['path'] = backtrack_solution(
                        neighbor, parent, maze)
                    solution['path-cost'] = len(solution['path'])
                    solution['nodes-expanded'] = len(explored)
                    return solution
                frontier.append(neighbor)
    solution['time-elapsed'] = time() - start
    solution['nodes-expanded'] = len(explored)
    return solution


# ------------------------------------------------------------------------
# INFORMED ALGORITHMS
# ------------------------------------------------------------------------


def uniform_cost_search(maze: Maze, **kwargs):
    """
    Solve a maze using Uniform-Cost Search
    """

    start = time()
    solution = {
        'path': None,
        'path-cost': None,
        'nodes-expanded': None,
        'time-elapsed': None
    }
    frontier = PriorityQueue()
    frontier.add(maze.start_pos, 0)
    parent = {}
    costs = {maze.start_pos: 0}
    nodes_expanded = 1

    while not frontier.is_empty:
        cost, p = frontier.pop()
        if p == maze.finish_pos:
            solution['time-elapsed'] = time() - start
            solution['path'] = backtrack_solution(p, parent, maze)
            solution['path-cost'] = cost
            solution['nodes-expanded'] = nodes_expanded
            return solution
        for neighbor in maze.get_neighbors(p):
            new_cost = cost+1
            if not neighbor in costs or new_cost < costs.get(neighbor, new_cost):
                costs[neighbor] = new_cost
                frontier.add(neighbor, new_cost)
                parent[neighbor] = p
                nodes_expanded += 1
    solution['time-elapsed'] = time() - start
    solution['nodes-expanded'] = nodes_expanded
    return solution


def astar_search(maze: Maze, **kwargs):
    heuristic_method = kwargs.pop('heuristic', 'euclidian')
    start = time()
    solution = {
        'path': None,
        'path-cost': None,
        'nodes-expanded': None,
        'time-elapsed': None
    }
    frontier = PriorityQueue()
    frontier.add(maze.start_pos, 0)
    parent = {}
    costs = {maze.start_pos: 0}
    nodes_expanded = 1

    while frontier:
        _, p = frontier.pop()
        if p == maze.finish_pos:
            solution['time-elapsed'] = time() - start
            solution['path'] = backtrack_solution(p, parent, maze)
            solution['path-cost'] = costs[p]
            solution['nodes-expanded'] = nodes_expanded
            return solution
        for neighbor in maze.get_neighbors(p):
            new_cost = costs[p] + 1
            if not neighbor in costs or new_cost < costs.get(neighbor, new_cost):
                nodes_expanded += 1
                costs[neighbor] = new_cost
                frontier.add(neighbor, new_cost+heuristic(neighbor,
                             maze.finish_pos, heuristic_method))
                parent[neighbor] = p
    return None, None, nodes_expanded


def solve_maze(maze, method='astar', **kwargs):
    """
    Runs a search algorithm on the maze provided

    Parameters
    ----------
    maze : :class:`Maze`
        The Maze object to find a solution for

    Keyword Arguments
    -----------------
    method : str
        The name of the method to run
    """

    if method == 'depth':
        solution = depth_first_search(maze, **kwargs)
    elif method == 'breadth':
        solution = breadth_first_search(maze, **kwargs)
    elif method == 'uniform':
        solution = uniform_cost_search(maze, **kwargs)
    elif method == 'astar':
        solution = astar_search(maze, **kwargs)
    else:
        raise ValueError('Invalid method: {}'.format(method))
    if solution['path']:
        print('Path found!')
        for p in solution['path']:
            print(p)
        print('-----Method Stats-----')
        print('Path Cost: {}'.format(solution['path-cost']))
        print('Nodes Expanded: {}'.format(solution['nodes-expanded']))
        print('Time Elapsed: {:06f}s'.format(solution['time-elapsed']))
