import tkinter as tk
from tkinter.constants import NO

from maze import Maze, CellType

class MazeCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super.__init__(master=master, **kwargs)
        self.maze: Maze = None
    
    