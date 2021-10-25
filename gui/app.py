import tkinter as tk

from gui.maze_frame import MazeCanvas
from gui.menus import MainMenu
from gui.console import MazeConsole
from gui.states import AppState



class App():
    def __init__(self) -> None:
        # Configure root
        self.root = tk.Tk()
        self.root.title('PyMaze')
        self.root.geometry('800x700')
        self.root.minsize(1500, 700)
        self.prev_state = None
        self.state = None

        # Configure wdigets
        self.console = MazeConsole(self.root)
        self.maze = MazeCanvas(
            self.root,
            self,
            margin=20,
            width=800,
            height=700,
            console=self.console)

        self.maze.grid(row=1, column=0)
        self.console.grid(row=1, column=1)

        self.menu = MainMenu(self.root, self, self.maze, self.console)
    
    def change_state(self, state: AppState) -> None:
        if state == self.state:
            return
        if state == AppState.GENERATING or state == AppState.SOLVING:
            self.menu.entryconfig('Generate', state='disabled')
            self.menu.entryconfig('Solve', state='disabled')
            self.menu.file_menu.entryconfig('Save As', state='disabled')
            self.menu.file_menu.entryconfig('Open', state='disabled')
        elif state == AppState.HOME:
            self.menu.entryconfig('Generate', state='normal')
            self.menu.entryconfig('Solve', state='disabled')
            self.menu.file_menu.entryconfig('Save As', state='disabled')
            self.menu.file_menu.entryconfig('Open', state='normal')
        elif state == AppState.MAZE:
            self.menu.entryconfig('Generate', state='normal')
            self.menu.entryconfig('Solve', state='normal')
            self.menu.file_menu.entryconfig('Save As', state='normal')
            self.menu.file_menu.entryconfig('Open', state='normal')
        else:
            raise ValueError(f'Invalid App State: {state}')
        self.prev_state = self.state
        self.state = state
    
    def revert_state(self):
        self.change_state(self.prev_state)


    def run(self):
        """
        Starts the GUI application. 
        
        This is a blocking call that returns when the application is closed
        """
        self.change_state(AppState.HOME)
        self.root.mainloop()
