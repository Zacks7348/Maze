import tkinter as tk

from maze import Maze, Cell, CellType 
from maze import MazeGenMethods, RPAMazeGenerator, RDFSMazeGenerator
from maze import MazeSolverMethods, DFSMazeSolver

MARGIN = 20
SIZE = 10
MAZE_HEIGHT = 70
MAZE_WIDTH = 100
HEIGHT = MARGIN * 2 + SIZE * MAZE_HEIGHT
WIDTH = MARGIN * 2 + SIZE * MAZE_WIDTH


class MazeCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        self.margin = kwargs.pop('margin', 20)
        self.height = kwargs.get('height')
        self.width = kwargs.get('width')
        self.maze: Maze = None

        self.row_lines = []
        self.col_lines = []
        self.row_height = 0
        self.col_width = 0
        self.cells = []
        self.traversed_cells = []
        self.solution = []
        super().__init__(master, **kwargs)

        # Init UI
        self.__draw_border()

    def generate(self, method, height, width):
        self.__clear_cells()
        if method == MazeGenMethods.RDFS:
            g = RDFSMazeGenerator(height=height, width=width, step=True)
        elif method == MazeGenMethods.RPA:
            g = RPAMazeGenerator(height=height, width=width, step=True)
        else:
            raise ValueError('Invalid method')
        self.maze = g.maze
        self.__draw_maze()
        self.__draw_cells()

        while not g.finished:
            cells = g.step()
            if cells:
                self.__update_cells(cells)
            self.update()
        
        g.randomized_finish()
        self.__draw_cell(self.maze.start_pos)
        self.__draw_cell(self.maze.finish_pos)

    def solve(self, method):
        if method == MazeSolverMethods.DFS:
            s = DFSMazeSolver(self.maze, step=True)
        else:
            raise ValueError('Invalid method')

        while not s.finished:
            cells = s.step()
            if cells:
                for c in cells:
                    if c != self.maze.start_pos and c != self.maze.finish_pos:
                        x1, y1, x2, y2 = self.__cell_2_coords(c)
                        self.traversed_cells.append(self.create_rectangle(x1, y1, x2, y2, fill='yellow'))
                self.update()
        if s.solution:
            for c in s.solution:
                if c != self.maze.start_pos and c != self.maze.finish_pos:
                    x1, y1, x2, y2 = self.__cell_2_coords(c)
                    self.solution.append(self.create_rectangle(x1, y1, x2, y2, fill='blue'))
                    self.update()


    def __draw_border(self):
        wm = self.width - self.margin
        hm = self.height - self.margin
        self.create_line(self.margin, self.margin,
                         self.margin, hm)
        self.create_line(wm, self.margin, wm, hm)
        self.create_line(self.margin, self.margin, wm, self.margin)
        self.create_line(self.margin, hm, wm, hm)
    
    def __draw_maze(self):
        # Draw rows
        self.row_height = (self.height - self.margin*2) / self.maze.height
        for i in range(1, self.maze.height):
            dy = self.margin + (self.row_height * i)
            self.row_lines.append(
                self.create_line(self.margin, dy, self.width-self.margin, dy)
            )
        # Draw cols
        self.col_width = (self.width - self.margin*2) / self.maze.width
        for i in range(1, self.maze.width):
            dx = self.margin + (self.col_width * i)
            self.col_lines.append(
                self.create_line(dx, self.margin, dx, self.height-self.margin)
            )
    
    def __update_cells(self, cells):
        for cell in cells:
            self.__draw_cell(cell)

    def __draw_cells(self):
        for row in range(self.maze.height):
            for col in range(self.maze.width):
                cell = Cell(row, col)
                self.__draw_cell(cell)
    
    def __draw_cell(self, cell: Cell):
        x1, y1, x2, y2 = self.__cell_2_coords(cell)
        if cell == self.maze.start_pos:
            self.cells.append(
                self.create_rectangle(x1, y1, x2, y2, fill='green')
            )
        elif cell == self.maze.finish_pos:
            self.cells.append(
                self.create_rectangle(x1, y1, x2, y2, fill='red')
            )
        elif self.maze.is_wall(cell):
            self.cells.append(
                self.create_rectangle(x1, y1, x2, y2, fill='black')
            )
        elif self.maze.is_passage(cell):
            self.cells.append(
                self.create_rectangle(x1, y1, x2, y2, fill='white')
            )
    
    def __clear_cells(self):
        for c in self.cells:
            self.delete(c)
        for c in self.traversed_cells:
            self.delete(c)
        for c in self.solution:
            self.delete(c)
    
    def __cell_2_coords(self, c: Cell):
        x1 = self.margin + (self.col_width * c.col)
        y1 = self.margin + (self.row_height * c.row)
        return x1, y1, x1+self.col_width, y1+self.row_height
