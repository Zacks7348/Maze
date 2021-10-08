from __future__ import annotations

from typing import List, Union
from collections import namedtuple
from random import randint


class Movement():
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


Position = namedtuple('Position', ['row', 'col'])


class Maze():
    """
    Represents a maze 
    """

    def __init__(self, maze: List[List[str]] = None, wall_char: str = '%',
                 empty_char: str = ' ', start_char: str = 'S',
                 finish_char: str = 'F') -> None:
        """
        Create a maze 

        Parameters
        ----------
        maze: List[List[str]], default=None
            A 2D list of characters representing a maze
        """
        self.wall_char = wall_char
        self.empty_char = empty_char
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
    def generate(self, method: str = 'RPA', **kwargs) -> Maze:
        """
        Return a :class:`Maze` object by randomly generating a maze

        TODO: implement
        """
        pass

    def get_neighbors(self, position: Position) -> List[Position]:
        neighbors = [
            Position(position.row-1, position.col),  # UP
            Position(position.row+1, position.col),  # DOWN
            Position(position.row, position.col-1),  # LEFT
            Position(position.row, position.col+1)  # RIGHT
        ]
        return [p for p in neighbors if self.is_passable(p) and self.is_valid_position(p)]

    def is_valid_position(self, position: Position) -> bool:
        if not 0 <= position.row < len(self.maze):
            return False
        if not 0 <= position.col < len(self.maze[0]):
            return False
        return True

    def is_passable(self, position: Position) -> bool:
        return self.maze[position.row][position.col] != self.wall_char

    def change_walls(self, wall_char: str) -> None:
        """
        Change the character representing walls in the maze
        """

        self.__replace_chars(self.wall_char, wall_char)
        self.wall_char = wall_char

    def change_empty_spaces(self, empty_char: str) -> None:
        """
        Change the character representing empty spaces in the maze
        """

        self.__replace_chars(self.empty_char, empty_char)
        self.empty_char = empty_char

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
                if not self.maze[i][j] in (self.wall_char, self.empty_char,
                                           self.start_char, self.finish_char):
                    self.maze[i][j] = self.empty_char

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


if __name__ == '__main__':
    maze = Maze.from_random(height=5, width=10)
    print(maze)
