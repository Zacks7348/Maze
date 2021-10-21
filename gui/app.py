import tkinter as tk
from enum import Enum

from gui.maze_frame import MazeCanvas
from gui.menus import MainMenu

class App():
    def __init__(self) -> None:
        # Configure root
        self.root = tk.Tk()
        self.root.title('PyMaze')
        self.root.geometry('1000x800')
        self.root.minsize(1000, 800)

        # Configure wdigets
        self.maze = MazeCanvas(
            self.root,
            margin=20,
            width=1000,
            height=800)
        self.maze.pack(fill=tk.BOTH, side=tk.TOP)

        self.menu = MainMenu(self.root, self.maze)
    
    def run(self):
        """
        Starts the GUI application. 
        
        This is a blocking call that returns when the application is closed
        """
        self.root.mainloop()
