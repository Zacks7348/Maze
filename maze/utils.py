import heapq
import pdb
import math
from collections import namedtuple

Position = namedtuple('Position', ['row', 'col'])

class PriorityQueue:
    def __init__(self) -> None:
        self.queue = []

    def add(self, item, priority) -> None:
        heapq.heappush(self.queue, (priority, item))

    def pop(self):
        return heapq.heappop(self.queue)
    
    @property
    def is_empty(self) -> bool:
        return not self.queue

def backtrack_solution(finish, parents, start):
    """
    Returns the path found to the finish position. 
    """

    path = []
    p = finish
    while p and p != start:
        #print(f'{p} <---', end=' ')
        path.append(p)
        p = parents.get(p, None)
        #print(f'{p}')
    path.reverse()
    return path

def heuristic(p1: Position, p2: Position, method: str) -> int:
    if method == 'euclidian':
        return math.sqrt((p1.row - p2.row)**2 + (p1.col - p2.col)**2)
    if method == 'manhattan':
        return abs(p1.row-p2.row) + abs(p1.col-p2.col)
    raise ValueError('Invalid heurisitc method: {}'.format(method))