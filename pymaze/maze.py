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
