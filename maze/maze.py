from __future__ import annotations

from typing import List, Union
from collections import namedtuple
from random import randint, choice
import pdb

from maze.utils import Position


class Movement():
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


class Maze():
    """
    Represents a maze 
    """

    def __init__(self, maze: List[List[str]] = None, wall_char: str = '%',
                 passage_char: str = ' ', start_char: str = 'S',
                 finish_char: str = 'F') -> None:
        """
        Create a maze 

        Parameters
        ----------
        maze: List[List[str]], default=None
            A 2D list of characters representing a maze
        """
        self.wall_char = wall_char
        self.passage_char = passage_char
        self.start_char = start_char
        self.finish_char = finish_char
        self.start_pos: Position = None
        self.finish_pos: Position = None
        self.maze: List[List[str]] = maze

    @classmethod
    def from_file(cls, filename: str, **kwargs) -> Maze:
        """
        Return a :class:`Maze` object from a file

        Keyword arguments are sent to the :class:`Maze` constructor
        """

        self = cls(maze=[], **kwargs)
        with open(filename, 'r') as f:
            for row, line in enumerate(f.readlines()):
                cells = []
                for col, c in enumerate(line):
                    p = Position(row, col)
                    if c == self.start_char:
                        self.start_pos = p
                    elif c == self.finish_char:
                        self.finish_pos = p
                    elif c == '\n':
                        break
                    cells.append(c)
                self.maze.append(cells)
        return self

    @classmethod
    def generate(cls, method: str = 'rdfs', **kwargs) -> Maze:
        """
        Return a :class:`Maze` object by randomly generating a maze

        """
        self = cls()
        height = kwargs.pop('height', 10)
        width = kwargs.pop('width', 10)

        if method == 'rdfs':
            rdfs(self, height=height, width=width, **kwargs)
        return self

    def get(self, p: Position) -> str:
        """
        Return the character at p
        """
        if not self.is_valid_position(p):
            raise ValueError(f'Invalid position: {p}')
        return self.maze[p.row][p.col]

    def set(self, p: Position, c: str) -> None:
        """
        Set the character in the maze to c at p
        """
        if not self.is_valid_position(p):
            raise ValueError(f'Invalid position: {p}')
        self.maze[p.row][p.col] = c

    def get_neighbor_positions(self, position: Position) -> dict:
        """
        Returns a dictionary of adjacent positions
        """
        if not self.is_valid_position(position):
            raise ValueError('Invalid maze position: {}'.format(position))
        res = {}
        # UP
        p = Position(position.row-1, position.col)
        if self.is_valid_position(p):
            res[Movement.UP] = p
        # DOWN
        p = Position(position.row+1, position.col)
        if self.is_valid_position(p):
            res[Movement.DOWN] = p
        # LEFT
        p = Position(position.row, position.col-1)
        if self.is_valid_position(p):
            res[Movement.LEFT] = p
        # RIGHT
        p = Position(position.row, position.col+1)
        if self.is_valid_position(p):
            res[Movement.RIGHT] = p
        return res


    def get_neighbors(self, position: Position) -> dict:
        """
        Shortcut for getting all adjacent passage positions
        """
        return {d: p for d, p in self.get_neighbor_positions(position).items() if self.is_passage(p)}

    def get_neighbor_walls(self, position: Position) -> dict:
        """
        Shortcut for getting all adjacent wall positions
        """
        return {d: p for d, p in self.get_neighbor_positions(position).items() if self.is_wall(p)}

    def is_valid_position(self, position: Position) -> bool:
        if not position: 
            return False
        if not 0 <= position.row < len(self.maze):
            return False
        if not 0 <= position.col < len(self.maze[0]):
            return False
        return True

    def is_passage(self, position: Position) -> bool:
        return self.maze[position.row][position.col] != self.wall_char
    
    def is_wall(self, position: Position) -> bool:
        return self.maze[position.row][position.col] == self.wall_char

    def change_walls(self, wall_char: str) -> None:
        """
        Change the character representing walls in the maze
        """

        self.__replace_chars(self.wall_char, wall_char)
        self.wall_char = wall_char

    def change_passage_char(self, empty_char: str) -> None:
        """
        Change the character representing passages in the maze
        """

        self.__replace_chars(self.passage_char, empty_char)
        self.passage_char = empty_char

    def change_start_char(self, start_char) -> None:
        if self.start_char == start_char:
            return
        self.start_char = start_char
        self.maze[self.start_pos.row][self.start_pos.col] = self.start_char

    def change_finish_char(self, finish_char) -> None:
        if self.finish_char == finish_char:
            return
        self.finish_char = finish_char
        self.maze[self.finish_pos.row][self.finish_pos.col] = self.finish_char

    def to_txt(self, filename: str) -> None:
        """
        Dumps the maze into a .txt file

        Parameters
        ----------
        filename: str
            The file to dump to
        """
        with open(filename, 'w') as f:
            for row in self.maze:
                f.write(''.join(row)+'\n')

    def reset(self) -> None:
        """
        Reset the maze back to its initial state. 
        """
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if not self.maze[i][j] in (self.wall_char, self.passage_char,
                                           self.start_char, self.finish_char):
                    self.maze[i][j] = self.passage_char

    def __replace_chars(self, old: str, new_: str) -> None:
        if old == new_:
            return
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == old:
                    self.maze[i][j] = new_

    def __str__(self) -> str:
        output = ''
        for row in self.maze:
            output += ''.join(row) + '\n'
        return output

def __opposite(p: Position, parent: Position) -> Position:
    """
    Returns the opposite position given p and it's parent
    """

    if p.row == parent.row:
        return Position(p.row, p.col+(p.col-parent.col))
    if p.col == parent.col:
        return Position(p.row+(p.row-parent.row), p.col)

def rdfs(maze: Maze, height: int=10, width: int=10, **kwargs):
    """
    Generates a maze using Randomized Depth-First Search
    """

    frontier = [] # Acting as a stack
    explored = set()

    maze.maze = [[maze.wall_char for _ in range(width)] for _ in range(height)]
    
    start = Position(randint(0, height-1), randint(0, width-1))
    maze.set(start, maze.passage_char)
    explored.add(start)
    frontier.append(start)

    while frontier:
        print(maze)
        pdb.set_trace()
        p = frontier.pop()
        maze.set(p, maze.passage_char)
        neighbors = maze.get_neighbor_positions(p).values()
        unvisited = [n for n in neighbors if not n in explored]
        if unvisited:
            frontier.append(p)
            un = choice(unvisited)
            maze.set(un, maze.passage_char)
            explored.add(un)
            frontier.append(un)










if __name__ == '__main__':
    maze = Maze.from_random(height=5, width=10)
    print(maze)
