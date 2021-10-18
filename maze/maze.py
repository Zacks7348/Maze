from __future__ import annotations
from enum import Enum
from typing import List
from collections import namedtuple
import random
import pdb


class CellType(Enum):
    WALL = 0
    PASSAGE = 1
    START = 2
    FINISH = 3


Cell = namedtuple('Cell', ['row', 'col'])


class Maze:

    def __init__(self, maze: List[List[CellType]], **kwargs) -> None:
        """
        Create a :class:`Maze` object given a 2D list of CellTypes

        Parameters
        ----------
        maze: List[List[CellType]]
            a 2D list of CellTypes
        """

        self.maze = maze

        self.wall_char = kwargs.pop('wall_char', '%')
        self.passage_char = kwargs.pop('passage_char', ' ')
        self.start_char = kwargs.pop('start_char', 'S')
        self.finish_char = kwargs.pop('finish_char', 'F')

        self.start_pos = None
        self.finish_pos = None

    @classmethod
    def from_file(cls, filename: str, **kwargs) -> Maze:
        """
        Create a :class:`Maze` object from a txt file

        Keyword arguments are send to the :class:`Maze` constructor

        Parameters
        ----------
        filename: str
            The name of the file to read

        """
        self = cls([], **kwargs)
        with open(filename, 'r') as f:
            for row, line in enumerate(f.readlines()):
                cells = []
                for col, c in enumerate(line):
                    if c == self.wall_char:
                        cells.append(CellType.WALL)
                    elif c == self.passage_char:
                        cells.append(CellType.PASSAGE)
                    elif c == self.start_char:
                        self.start_pos = Cell(row, col)
                        cells.append(CellType.START)
                    elif c == self.finish_char:
                        self.finish_pos = Cell(row, col)
                        cells.append(CellType.FINISH)
                    elif c == '\n':
                        break
                    else:
                        raise ValueError(f'Invalid character: {c}')
                self.maze.append(cells)
        return self

    @classmethod
    def generate(cls, method: str = 'rdfs', **kwargs) -> Maze:
        """
        Create a :class:`Maze` object with a randomly generated maze

        Keyword arguments are sent to the :class:`Maze` constructor
        and to the generator function

        Parameters
        ----------
        method: str, default='rdfs'
            The method to use for generation
        """
        self = cls([], **kwargs)
        gen_methods = {
            'rdfs': rdfs,
            'rpa': rpa
        }

        gen_methods[method](self, **kwargs)
        #self.set(self.start_pos, CellType.START)
        #self.set(self.finish_pos, CellType.FINISH)
        return self

    def get(self, c: Cell) -> CellType:
        """
        Shortcut for getting the value of a cell
        """
        if not self.is_valid_cell(c):
            raise ValueError(f'Invalid Cell: {c}')
        return self.maze[c.row][c.col]

    def set(self, c: Cell, val: CellType) -> None:
        """
        Shortcut for setting the value of a cell
        """
        if not self.is_valid_cell(c):
            raise ValueError(f'Invalid Cell: {c}')
        self.maze[c.row][c.col] = val

    def is_valid_cell(self, c: Cell) -> bool:
        """
        Returns True if the cell is in the maze
        """
        if not c:
            return False
        return (0 <= c.row < len(self.maze)) and (0 <= c.col < len(self.maze[0]))

    def is_passage(self, c: Cell) -> bool:
        """
        Returns True if the cell is a passage
        """
        return self.get(c) != CellType.WALL

    def is_wall(self, c: Cell) -> bool:
        """
        Returns True if the cell is a wall
        """
        return self.get(c) == CellType.WALL

    def get_neighboring_cells(self, c: Cell, d: int = 1) -> List[Cell]:
        """
        Returns a list of :class:`Cell` objects that are neighbors to c

        Parameters
        ----------
        c: Cell
            The cell whose neighbors we are looking for
        d: int, default=1
            The distance to look for neighbors
        """
        if d <= 0:
            raise ValueError(f'Invalid distance: {d}')
        deltas = [(d, 0), (-1*d, 0), (0, d), (0, -1*d)]
        res = []

        for dr, dc in deltas:
            tmp = Cell(c.row+dr, c.col+dc)
            if self.is_valid_cell(tmp):
                res.append(tmp)
        return res

    def get_neighboring_walls(self, c: Cell, d: int = 1) -> List[Cell]:
        """
        Shortcut for filtering the result of :method:`get_neighboring_cells` to
        just walls
        """
        return [n for n in self.get_neighboring_cells(c, d) if self.is_wall(n)]

    def get_neighboring_passages(self, c: Cell, d: int = 1) -> List[Cell]:
        """
        Shortcut for filtering the result of :method:`get_neighboring_cells` to
        just passages
        """
        return [n for n in self.get_neighboring_cells(c, d) if self.is_passage(n)]

    def to_file(self, filename: str) -> None:
        """
        Write the maze to a txt file

        Parameters
        ----------
        filename: str
            The name of the file to write to. If the file does not exist one
            will be created
        """
        with open(filename, 'w') as f:
            f.write(self.__str__())

    def __str__(self) -> str:
        output = ''
        maps = {
            CellType.PASSAGE: self.passage_char,
            CellType.WALL: self.wall_char,
            CellType.START: self.start_char,
            CellType.FINISH: self.finish_char}
        for row in self.maze:
            output += ''.join([maps[c] for c in row]) + '\n'
        return output

# ------------------------------------------------------------------------
# MAZE GENERATION ALGORITHMS
# ------------------------------------------------------------------------


def random_cell(max_row: int, max_col: int, is_odd: bool = False):
    row = random.randint(0, max_row-1)
    while is_odd and row % 2 == 0:
        row = random.randint(0, max_row-1)
    col = random.randint(0, max_col-1)
    while is_odd and col % 2 == 0:
        col = random.randint(0, max_col-1)
    return Cell(row, col)

def opposite_cell(cell: Cell, n: Cell):
    dr = cell.row - n.row
    row = dr + min(cell.row, n.row) if dr < 0 else dr + max(cell.row, n.row)
    dc = cell.col - n.col
    col = dc + min(cell.col, n.col) if dc < 0 else dc + max(cell.col, n.col)
    return Cell(row, col)

def middle_cell(cell: Cell, n: Cell):
    if cell.row == n.row:
        return Cell(cell.row, max(cell.col, n.col)-1)
    else:
        return Cell(max(cell.row, n.row)-1, cell.col)


def rdfs(maze: Maze, **kwargs) -> None:
    """
    Generate a maze using Randomized Depth-First Search
    """

    height = kwargs.pop('height', 25)
    if height % 2 == 0:
        raise ValueError('Height must be odd!')
    width = kwargs.pop('width', 55)
    if width % 2 == 0:
        raise ValueError('Width must be odd!')
    frontier = []  # Stack

    # Initialize maze as a grid of walls
    maze.maze = [[CellType.WALL for _ in range(
        width)] for _ in range(height)]

    # Randomly choose starting point
    maze.start_pos = random_cell(height, width, is_odd=True)
    frontier.append(maze.start_pos)

    while frontier:
        cell = frontier[-1]
        neighbors = maze.get_neighboring_walls(cell, d=2)
        if neighbors:
            n = random.choice(neighbors)
            maze.set(cell, CellType.PASSAGE)
            maze.set(n, CellType.PASSAGE)
            middle = None
            if cell.row == n.row:
                middle = Cell(cell.row, max(cell.col, n.col)-1)
            else:
                middle = Cell(max(cell.row, n.row)-1, cell.col)
            maze.set(middle, CellType.PASSAGE)
            frontier.append(n)
            print(maze)
            for _ in range(10000000): pass
        else:
            frontier.pop()


    maze.finish_pos = random_cell(height, width, is_odd=True)
    while maze.is_wall(maze.finish_pos) and maze.finish_pos == maze.start_pos:
        maze.finish_pos = random_cell(height, width, is_odd=True)

def rpa(maze: Maze, **kwargs) -> None:
    """
    Generate a maze using Randomized Prim's Algorithm
    """

    height = kwargs.pop('height', 25)
    if height % 2 == 0:
        raise ValueError('Height must be odd!')
    width = kwargs.pop('width', 55)
    if width % 2 == 0:
        raise ValueError('Width must be odd!')
    
    frontier = []
    frontier_set = set()


    # Initialize maze as a grid of walls
    maze.maze = [[CellType.WALL for _ in range(
        width)] for _ in range(height)]
    
    # Randomly choose starting point
    maze.start_pos = random_cell(height-1, width-1, is_odd=True)
    maze.set(maze.start_pos, CellType.PASSAGE)

    for n in maze.get_neighboring_walls(maze.start_pos, d=2):
        frontier.append(n)
        frontier_set.add(n)

    while frontier:
        print(maze)
        for _ in range(1000000): pass
        #pdb.set_trace()
        wall = frontier.pop(random.randint(0, len(frontier)-1))
        frontier_set.remove(wall)
        neighbors = maze.get_neighboring_cells(wall, d=2)
        random.shuffle(neighbors)
        for n in neighbors:
            if maze.is_passage(n):
                #pdb.set_trace()
                o = opposite_cell(wall, n)
                if maze.is_valid_cell(o):
                    if maze.is_wall(o):
                        #pdb.set_trace()
                        maze.set(wall, CellType.PASSAGE)
                        maze.set(n, CellType.PASSAGE)
                        maze.set(middle_cell(wall, n), CellType.PASSAGE)
                        for nn in maze.get_neighboring_walls(wall, d=2):
                            #pdb.set_trace()
                            if not nn in frontier_set:
                                frontier.append(nn)
                                frontier_set.add(nn)
                        break
                else:
                    #pdb.set_trace()
                    maze.set(wall, CellType.PASSAGE)
                    maze.set(n, CellType.PASSAGE)
                    maze.set(middle_cell(wall, n), CellType.PASSAGE)
                    for nn in maze.get_neighboring_walls(wall, d=2):
                        #pdb.set_trace()
                        if not nn in frontier_set:
                            frontier.append(nn)
                            frontier_set.add(nn)
                    break
        
        




if __name__ == '__main__':
    #m = Maze.from_file('tests/Maze1.txt')
    m = Maze.generate(method='rpa', height=55, width=105)
    # c = Cell(3, 5)
    # n = Cell(5, 5)
    # print(opposite_cell(c, n))
