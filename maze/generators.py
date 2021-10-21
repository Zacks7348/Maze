import random

from maze.maze import Maze, Cell, CellType

class MazeGenMethods:
    RDFS = 'RDFS'
    RPA = "RPA"

class MazeGenerator:
    def __init__(self, **kwargs) -> None:
        self.maze: Maze = None
        self.step_mode = kwargs.pop('step', False)
        self.height = kwargs.pop('height', 105)
        if self.height % 2 == 0:
            raise ValueError('Maze height must be odd!')
        self.width = kwargs.pop('width', 105)
        if self.width % 2 == 0:
            raise ValueError('Maze width must be odd!')
        self.frontier = None
        self.finished = False

    def randomized_finish(self):
        """
        Randomly choose finish cell
        """

        f = self.random_cell(self.maze.height, self.maze.width, is_odd=True)
        while self.maze.is_wall(f):
            f = self.random_cell(self.maze.height, self.maze.width, is_odd=True)
        self.maze.finish_pos = f
    
    def random_cell(self, max_row: int, max_col: int, is_odd: bool = False):
        row = random.randint(0, max_row-1)
        while is_odd and row % 2 == 0:
            row = random.randint(0, max_row-1)
        col = random.randint(0, max_col-1)
        while is_odd and col % 2 == 0:
            col = random.randint(0, max_col-1)
        return Cell(row, col)

    def middle_cell(self, c1: Cell, c2: Cell) -> Cell:
        if c1.row == c2.row:
            return Cell(c1.row, max(c1.col, c2.col)-1)
        return Cell(max(c1.row, c2.row)-1, c1.col)
    
    def opposite_cell(self, cell: Cell, n: Cell):
        dr = cell.row - n.row
        row = dr + min(cell.row, n.row) if dr < 0 else dr + max(cell.row, n.row)
        dc = cell.col - n.col
        col = dc + min(cell.col, n.col) if dc < 0 else dc + max(cell.col, n.col)
        return Cell(row, col)
    
    def loopify(self, chance=0.1):
        if not 0 <= chance <= 1:
            raise ValueError('Loop chance must be a number between 0 and 1!')
        changed = []
        for i in range(1, self.maze.height-1):
            for j in range(1, self.maze.width-1):
                c = Cell(i, j)
                if self.maze.is_wall(c) and random.random() < chance:
                    self.maze.set(c, CellType.PASSAGE)
                    changed.append(c)
        return changed

class RDFSMazeGenerator(MazeGenerator):
    """
    Maze Generator using Randomized Depth-First Search
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
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

        # Randomly choose starting point
        self.maze.start_pos = self.random_cell(height, width, is_odd=True)
        self.maze.set(self.maze.start_pos, CellType.PASSAGE)
        self.frontier.append(self.maze.start_pos)

        if self.step_mode:
            return
        while not self.finished:
            self.step()
    
    def step(self):
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
            middle = self.middle_cell(cell, n)
            self.maze.set(middle, CellType.PASSAGE)
            self.frontier.append(n)
            return (middle, n)
        else:
            self.frontier.pop()
        return None

class RPAMazeGenerator(MazeGenerator):
    """
    Maze Generator using Randomized Prim's Algorithm
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
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

        self.maze.start_pos = self.random_cell(height-1, width-1, is_odd=True)
        self.maze.set(self.maze.start_pos, CellType.PASSAGE)
        for n in self.maze.get_neighboring_walls(self.maze.start_pos, d=2):
            self.frontier.append(n)
            self.frontier_set.add(n)

        if self.step_mode:
            return
        while not self.finished:
            self.step()
    
    def step(self):
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
                middle = self.middle_cell(wall, n)
                add(wall, middle, n)
                return (wall, middle, n)
        return None
