import collections
import tkinter as tk
from enum import Enum

from gui.maze_frame import MazeCanvas
from gui.menus import MainMenu
from gui.console import MazeConsole

class App():
    def __init__(self) -> None:
        # Configure root
        self.root = tk.Tk()
        self.root.title('PyMaze')
        self.root.geometry('800x700')
        self.root.minsize(1500, 700)

        # Configure wdigets
        self.console = MazeConsole(self.root)
        self.maze = MazeCanvas(
            self.root,
            margin=20,
            width=800,
            height=700,
            console=self.console)

        self.maze.grid(row=1, column=0)
        self.console.grid(row=1, column=1)

        self.menu = MainMenu(self.root, self.maze, self.console)
    
    def run(self):
        """
        Starts the GUI application. 
        
        This is a blocking call that returns when the application is closed
        """
        self.root.mainloop()
