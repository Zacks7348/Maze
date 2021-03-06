import tkinter as tk

from pymaze.gui.states import AppState
from pymaze.maze import Maze, Cell, CellType
from pymaze.generators import MazeGenMethods, RPAMazeGenerator, RDFSMazeGenerator
from pymaze.solvers import (
    MazeSolverMethods, DFSMazeSolver, BFSMazeSolver, UCSMazeSolver, ASTARMazeSolver)


class MazeCanvas(tk.Canvas):
    def __init__(self, master, app, **kwargs):
        self.margin = kwargs.pop('margin', 20)
        self.height = kwargs.get('height')
        self.width = kwargs.get('width')
        self.maze: Maze = None
        self.app = app

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

    def open_maze(self, file_dir):
        try:
            self.app.change_state(AppState.GENERATING)
            self.maze = Maze.from_file(file_dir)
            self.__clear_cells()
            self.update()
            self.__draw_maze()
            self.update()
            self.__draw_cells()
            self.update()
            self.app.change_state(AppState.MAZE)
        except Exception as e:
            # self.console.error(str(e))
            pass

    def generate(self, method, height, width, loop):
        self.app.change_state(AppState.GENERATING)
        self.__clear_cells()
        try:
            if method == MazeGenMethods.RDFS:
                g = RDFSMazeGenerator(height=height, width=width, step=True)
            elif method == MazeGenMethods.RPA:
                g = RPAMazeGenerator(height=height, width=width, step=True)
            else:
                self.app.revert_state()
                raise ValueError('Invalid method')
            self.maze = g.maze
            self.__draw_maze()
            self.__draw_cells()

            while not g.finished:
                cells = g.step()
                if cells:
                    self.__update_cells(cells)
                self.update()
        except Exception as e:
            self.app.revert_state()
            return

        g.randomized_start_finish()
        self.__draw_cell(self.maze.start_pos)
        self.__draw_cell(self.maze.finish_pos)
        self.update()
        try:
            np = g.loopify(chance=loop)
        except Exception as e:
            # self.console.error(str(e))
            self.app.revert_state()
            return
        self.__update_cells(np)
        self.update()
        self.app.change_state(AppState.MAZE)

    def solve(self, method, heuristic):
        self.app.change_state(AppState.SOLVING)
        if not self.maze:
            self.app.revert_state()
            return
        self.__clear_traversal_cells()
        self.__clear_solution_cells()
        if method == MazeSolverMethods.DFS:
            s = DFSMazeSolver(self.maze, step=True)
        elif method == MazeSolverMethods.BFS:
            s = BFSMazeSolver(self.maze, step=True)
        elif method == MazeSolverMethods.UCS:
            s = UCSMazeSolver(self.maze, step=True)
        elif method == MazeSolverMethods.ASTAR:
            s = ASTARMazeSolver(self.maze, step=True)
        else:
            self.app.revert_state()
            raise ValueError('Invalid method')

        while not s.finished:
            cells = s.step()
            if cells:
                for c in cells:
                    if c != self.maze.start_pos and c != self.maze.finish_pos:
                        x1, y1, x2, y2 = self.__cell_2_coords(c)
                        self.traversed_cells.append(
                            self.create_rectangle(x1, y1, x2, y2, fill='yellow'))
                self.update()
        if s.solution:
            for c in s.solution:
                if c != self.maze.start_pos and c != self.maze.finish_pos:
                    x1, y1, x2, y2 = self.__cell_2_coords(c)
                    self.solution.append(self.create_rectangle(
                        x1, y1, x2, y2, fill='blue'))
                    self.update()
            # self.console.info('Done!')
            # self.console.info('Search results:')
            # self.console.info(f'  Nodes Expanded: {s.nodes_expanded}')
            # self.console.info(f'  Solution Cost: {s.solution_cost}')
        else:
            # self.console.info('No solution found!')
            pass
        self.app.change_state(AppState.MAZE)

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
                self.create_rectangle(x1, y1, x2, y2, fill='springgreen2')
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
        self.__clear_traversal_cells()
        self.__clear_solution_cells()
        self.update()

    def __clear_traversal_cells(self):
        for c in self.traversed_cells:
            self.delete(c)
        self.traversed_cells.clear()

    def __clear_solution_cells(self):
        for c in self.solution:
            self.delete(c)
        self.solution.clear()

    def __cell_2_coords(self, c: Cell):
        x1 = self.margin + (self.col_width * c.col)
        y1 = self.margin + (self.row_height * c.row)
        return x1, y1, x1+self.col_width, y1+self.row_height
