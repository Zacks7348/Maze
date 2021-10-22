import tkinter as tk
from tkinter import ttk

from gui.maze_frame import MazeCanvas
from maze import MazeGenMethods, MazeSolverMethods


class MainMenu(tk.Menu):
    def __init__(self, master: tk.Tk, maze: MazeCanvas, console):
        self.maze = maze
        self.console = console
        super().__init__(master, tearoff=False)
        self.master.config(menu=self)

        self.file_menu = FileMenu(master)
        self.edit_menu = EditMenu(master)

        self.add_cascade(label='File', menu=self.file_menu)
        self.add_cascade(label='Edit', menu=self.edit_menu)
        self.add_command(label='Generate', command=self.on_generate)
        self.add_command(label='Solve', command=self.on_solve)

    def on_generate(self):
        g = GenerateWindow(self, self.console)
        self.wait_window(g)
        if not g.generate:
            return
        self.maze.generate(g.method, g.height, g.width, g.loop)

    def on_solve(self):
        s = SolveWindow(self)
        self.wait_window(s)
        if not s.solve:
            return
        self.maze.solve(s.method)


class FileMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=False)
        self.add_command(label='Save')
        self.add_separator()
        self.add_command(label='Settings')
        self.add_separator()
        self.add_command(label='Exit', command=self.on_exit)

    def on_exit(self):
        self.master.destroy()


class EditMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=False)


class GenerateWindow(tk.Toplevel):
    def __init__(self, master, console, **kwargs):
        self.generate = False
        self.method = None
        self.height = None
        self.width = None
        self.loop = None
        self.console = console
        super().__init__(master, **kwargs)
        self.resizable(False, False)
        self.title('Generate Maze')

        # Create Widgets
        self.method_label = tk.Label(self, text='Method')
        self.method_combo = ttk.Combobox(
            self, values=[MazeGenMethods.RDFS,
                          MazeGenMethods.RPA], state='readonly'
        )
        self.method_combo.current(0)
        self.height_label = tk.Label(self, text='Maze Height')
        self.height_input = tk.Entry(self)
        self.height_input.insert(0, 105)
        self.width_label = tk.Label(self, text='Maze Width')
        self.width_input = tk.Entry(self)
        self.width_input.insert(0, 105)
        self.loop_label = tk.Label(self, text='Loop Chance')
        self.loop_input = tk.Entry(self)
        self.loop_input.insert(0, 0)
        self.help_button = tk.Button(self, text='Help')
        self.gen_button = tk.Button(
            self, text='Generate', command=self.on_generate)
        self.cancel_button = tk.Button(
            self, text='Cancel', command=self.on_cancel)

        # Grid Widgets
        self.method_label.grid(row=0, column=0)
        self.method_combo.grid(row=0, column=1)
        self.height_label.grid(row=1, column=0)
        self.height_input.grid(row=1, column=1)
        self.width_label.grid(row=2, column=0)
        self.width_input.grid(row=2, column=1)
        self.loop_label.grid(row=3, column=0)
        self.loop_input.grid(row=3, column=1)
        self.cancel_button.grid(row=4, column=0)
        self.gen_button.grid(row=4, column=1)
        self.help_button.grid(row=5, column=0, columnspan=2)

        self.grab_set()

    def on_generate(self):
        self.method = self.method_combo.get()
        try:
            self.height = int(self.height_input.get())
        except:
            self.console.error('Maze height must be an integer')
            return
        try:
            self.width = int(self.width_input.get())
        except:
            self.console.error('Maze width must be an integer')
            return
        try:
            self.loop = float(self.loop_input.get())
        except:
            self.console.error('Loop chance must be a decimal')
            return
        self.generate = True
        self.destroy()

    def on_cancel(self):
        self.destroy()


class SolveWindow(tk.Toplevel):
    def __init__(self, master, **kwargs):
        self.solve = False
        self.method = None
        super().__init__(master, **kwargs)
        self.resizable(False, False)
        self.title('Solve Maze')

        # Create Widgets
        self.method_label = tk.Label(self, text='Method')
        self.method_combo = ttk.Combobox(
            self, values=[MazeSolverMethods.DFS, MazeSolverMethods.BFS,
                          MazeSolverMethods.UCS, MazeSolverMethods.ASTAR], state='readonly'
        )
        self.method_combo.current(0)
        self.help_button = tk.Button(self, text='Help')
        self.gen_button = tk.Button(self, text='Solve', command=self.on_solve)
        self.cancel_button = tk.Button(
            self, text='Cancel', command=self.on_cancel)

        # Grid Widgets
        self.method_label.grid(row=0, column=0)
        self.method_combo.grid(row=0, column=1)
        self.cancel_button.grid(row=1, column=0)
        self.gen_button.grid(row=1, column=1)
        self.help_button.grid(row=2, column=0, columnspan=2)

        self.grab_set()

    def on_solve(self):
        self.method = self.method_combo.get()
        self.solve = True
        self.destroy()

    def on_cancel(self):
        self.destroy()
