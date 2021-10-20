import tkinter as tk

from maze import Maze, CellType

MARGIN = 20
SIZE = 10 
MAZE_HEIGHT = 70
MAZE_WIDTH = 100
HEIGHT = MARGIN * 2 + SIZE * MAZE_HEIGHT
WIDTH = MARGIN * 2 + SIZE * MAZE_WIDTH

class MazeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.maze: Maze = Maze.empty(height=MAZE_HEIGHT, width=MAZE_WIDTH)

        # Save lines from maze so we can delete them
        self.row_lines = []
        self.col_lines = []

        self.__init_ui()
    
    def __init_ui(self):
        self.pack(fill=tk.BOTH, expand=1)
        self.canvas = tk.Canvas(self, height=HEIGHT, width=WIDTH)
        self.canvas.pack(fill=tk.BOTH, side=tk.TOP)
        self.gen_button = tk.Button(self, text='Generate', command=self.generate_maze)
        self.gen_button.pack(fill=tk.BOTH, side=tk.BOTTOM)
        self.__draw_maze_border()
        self.__draw_maze()

    def generate_maze(self):
        self.maze = Maze.generate(method='rpa', height=MAZE_HEIGHT, width=MAZE_WIDTH)
    
    def __draw_maze_border(self):
        self.canvas.create_line(MARGIN, MARGIN, MARGIN, HEIGHT-MARGIN)
        self.canvas.create_line(WIDTH-MARGIN, MARGIN, WIDTH-MARGIN, HEIGHT-MARGIN)
        self.canvas.create_line(MARGIN, MARGIN, WIDTH-MARGIN, MARGIN)
        self.canvas.create_line(MARGIN, HEIGHT-MARGIN, WIDTH-MARGIN, HEIGHT-MARGIN)

    def __draw_maze(self):
        # Draw rows
        row_height = (HEIGHT - MARGIN*2) / self.maze.height
        for i in range(1, self.maze.height):
            self.row_lines.append(
                self.canvas.create_line(MARGIN, MARGIN+(row_height*i), WIDTH-MARGIN, MARGIN+(row_height*i))
            )
        
        # Draw cols
        col_width = (WIDTH - MARGIN*2) / self.maze.width
        for i in range(1, self.maze.width):
            self.col_lines.append(
                self.canvas.create_line(MARGIN + (col_width*i), MARGIN, MARGIN + (col_width*i), HEIGHT-MARGIN)
            )
    
    def __erase_maze(self):
        for line in self.row_lines:
            self.canvas.delete(line)
        for line in self.col_lines:
            self.canvas.delete(line)
    

def start():
    root = tk.Tk()
    MazeFrame(root)
    root.geometry(f'{WIDTH}x{HEIGHT+40}')
    root.mainloop()