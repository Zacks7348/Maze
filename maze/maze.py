from __future__ import annotations
from enum import Enum
from typing import List
from collections import namedtuple
import random


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
    def empty(cls, **kwargs) -> Maze:
        self = cls(None, **kwargs)
        height = kwargs.pop('height', 75)
        width = kwargs.pop('width', 105)
        self.maze = [[CellType.PASSAGE for _ in range(
            width)] for _ in range(height)]
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

    @property
    def height(self):
        return len(self.maze)

    @property
    def width(self):
        return len(self.maze[0])

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


class MazeGenerator:
    """
    Class used to generate a :class:`Maze` object.

    Provides the ability to step through the generation process. 
    """

    def __init__(self) -> None:
        self.maze: Maze = None
        self.method = None
        self.step_mode = False
        self.frontier = None
        self.finished = False

    def randomized_finish(self):
        """
        Randomly choose finish
        """

        f = self.__random_cell(self.maze.height, self.maze.width, is_odd=True)
        while self.maze.is_wall(f):
            f = self.__random_cell(
                self.maze.height, self.maze.width, is_odd=True)
        self.maze.finish_pos = f

    def rdfs(self, **kwargs) -> None:
        """
        Generate a maze using Randomized Depth-First Search
        """
        self.method = 'rdfs'
        height = kwargs.pop('height', 25)
        if height % 2 == 0:
            raise ValueError('Height must be odd!')
        width = kwargs.pop('width', 55)
        if width % 2 == 0:
            raise ValueError('Width must be odd!')

        # Initialize maze as a grid of walls
        m = [[CellType.WALL for _ in range(
            width)] for _ in range(height)]

        self.maze = Maze(m)
        self.frontier = []  # Stack

        # Randomly choose starting point
        self.maze.start_pos = self.__random_cell(height, width, is_odd=True)
        self.maze.set(self.maze.start_pos, CellType.PASSAGE)
        self.frontier.append(self.maze.start_pos)

        self.step_mode = kwargs.pop('step', False)
        if self.step_mode:
            return
        while not self.step():
            pass

    def rpa(self, **kwargs) -> None:
        self.method = 'rpa'
        height = kwargs.pop('height', 25)
        if height % 2 == 0:
            raise ValueError('Height must be odd!')
        width = kwargs.pop('width', 55)
        if width % 2 == 0:
            raise ValueError('Width must be odd!')

        # Initialize maze as a grid of walls
        m = [[CellType.WALL for _ in range(
            width)] for _ in range(height)]

        self.maze = Maze(m)
        self.frontier = []
        self.frontier_set = set()

        self.maze.start_pos = self.__random_cell(
            height-1, width-1, is_odd=True)
        self.maze.set(self.maze.start_pos, CellType.PASSAGE)
        for n in self.maze.get_neighboring_walls(self.maze.start_pos, d=2):
            self.frontier.append(n)
            self.frontier_set.add(n)

        self.step_mode = kwargs.pop('step', False)
        if self.step_mode:
            return
        while not self.step():
            pass

    def step(self) -> List[Cell]:
        """
        Function for stepping through the generation process.

        Each call performs a single step and returns a list of cells
        (if any) that were modified
        """
        if self.finished:
            return None
        if self.method == 'rdfs':
            return self.__rdfs_step()
        if self.method == 'rpa':
            return self.__rpa_step()

    def __rdfs_step(self) -> List[Cell]:
        if not self.frontier:
            # Finished
            self.finished = True
            return None
        cell = self.frontier[-1]
        neighbors = self.maze.get_neighboring_walls(cell, d=2)
        if neighbors:
            n = random.choice(neighbors)
            #self.maze.set(cell, CellType.PASSAGE)
            self.maze.set(n, CellType.PASSAGE)
            middle = self.__middle_cell(cell, n)
            self.maze.set(middle, CellType.PASSAGE)
            self.frontier.append(n)
            return (middle, n)
        else:
            self.frontier.pop()
        return None

    def __rpa_step(self):

        def add(c1, c2, c3):
            self.maze.set(c1, CellType.PASSAGE)
            self.maze.set(c2, CellType.PASSAGE)
            self.maze.set(c3, CellType.PASSAGE)

            for tmp in self.maze.get_neighboring_walls(c1, d=2):
                if not tmp in self.frontier_set:
                    self.frontier.append(tmp)
                    self.frontier_set.add(tmp)

        if not self.frontier:
            self.finished = True
            return None
        wall = self.frontier.pop(random.randint(0, len(self.frontier)-1))
        self.frontier_set.remove(wall)
        neighbors = self.maze.get_neighboring_cells(wall, d=2)
        random.shuffle(neighbors)
        for n in neighbors:
            if self.maze.is_passage(n):
                o = self.__opposite_cell(wall, n)
                if self.maze.is_valid_cell(o):
                    if self.maze.is_wall(o):
                        middle = self.__middle_cell(wall, n)
                        add(wall, middle, n)
                        return (wall, middle, n)
                else:
                    middle = self.__middle_cell(wall, n)
                    add(wall, middle, n)
                    return (wall, middle, n)

    def __random_cell(self, max_row: int, max_col: int, is_odd: bool = False):
        row = random.randint(0, max_row-1)
        while is_odd and row % 2 == 0:
            row = random.randint(0, max_row-1)
        col = random.randint(0, max_col-1)
        while is_odd and col % 2 == 0:
            col = random.randint(0, max_col-1)
        return Cell(row, col)

    def __middle_cell(self, c1: Cell, c2: Cell) -> Cell:
        if c1.row == c2.row:
            return Cell(c1.row, max(c1.col, c2.col)-1)
        return Cell(max(c1.row, c2.row)-1, c1.col)

    def __opposite_cell(self, cell: Cell, n: Cell):
        dr = cell.row - n.row
        row = dr + min(cell.row, n.row) if dr < 0 else dr + \
            max(cell.row, n.row)
        dc = cell.col - n.col
        col = dc + min(cell.col, n.col) if dc < 0 else dc + \
            max(cell.col, n.col)
        return Cell(row, col)


if __name__ == '__main__':
    #m = Maze.from_file('tests/Maze1.txt')
    gen = MazeGenerator()
    gen.rpa(height=55, width=105, step=False)

    while not gen.finished:
        gen.step()
        print(gen.maze)
