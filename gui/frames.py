import tkinter as tk
from tkinter import ttk

from maze import MazeGenMethods, MazeSolverMethods, HeuristicMethods

class ActionBaseWindow(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Should be set to True before self destruction to let caller
        # know to do the action
        self.do_action = False
        # Any options should be stored in this var as a tuple
        self.action_opt = None
        self.resizable(False, False)
        self.__init_ui()
        self.int_validation = (self.register(self.on_int_validate), '%i', '%P')
        self.float_validation = (self.register(self.on_float_validate), '%i', '%P')
    
    def __init_ui(self):
        self.cancel_button = tk.Button(
            self, text='Cancel', command=self.on_cancel)

    def on_int_validate(self, i, P):
        try:
            int(P)
            return True
        except:
            return False
    
    def on_float_validate(self, i, P):
        try:
            float(P)
            return True
        except:
            return False
    
    def on_cancel(self):
        self.destroy()

class GenerateWindow(ActionBaseWindow):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.__init_ui()
    
    def __init_ui(self):
        self.title_label = tk.Label(self, text='Maze Generation Options')
        self.method_label = tk.Label(self, text='Method')
        self.method_combo = ttk.Combobox(
            self, values=[MazeGenMethods.RDFS,
                          MazeGenMethods.RPA], state='readonly'
        )
        self.method_combo.current(0)
        self.height_label = tk.Label(self, text='Maze Height')
        self.height_input = tk.Entry(self, validate='key', validatecommand=self.int_validation)
        self.height_input.insert(0, 105)
        self.width_label = tk.Label(self, text='Maze Width')
        self.width_input = tk.Entry(self, validate='key', validatecommand=self.int_validation)
        self.width_input.insert(0, 105)
        self.loop_label = tk.Label(self, text='Loop Chance')
        self.loop_input = tk.Entry(self, validate='key', validatecommand=self.float_validation)
        self.loop_input.insert(0, 0)
        self.help_button = tk.Button(self, text='Help')
        self.gen_button = tk.Button(
            self, text='Generate', command=self.on_generate)
        
        self.title_label.grid(row=0, column=0, columnspan=3)
        self.method_label.grid(row=1, column=0)
        self.method_combo.grid(row=1, column=1, columnspan=2)
        self.height_label.grid(row=2, column=0)
        self.height_input.grid(row=2, column=1, columnspan=2)
        self.width_label.grid(row=3, column=0)
        self.width_input.grid(row=3, column=1, columnspan=2)
        self.loop_label.grid(row=4, column=0)
        self.loop_input.grid(row=4, column=1, columnspan=2)
        self.cancel_button.grid(row=5, column=0)
        self.gen_button.grid(row=5, column=1)
        self.help_button.grid(row=5, column=2)
    
    def on_generate(self):
        self.action_opt = (
            self.method_combo.get(), 
            int(self.height_input.get()),
            int(self.width_input.get()),
            float(self.loop_input.get()),
        )
        self.do_action = True
        self.destroy() # Goodbye cruel world

class SolveWindow(ActionBaseWindow):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.__init_ui()
    
    def __init_ui(self):
        self.title_label = tk.Label(self, text='Maze Solving Options')
        self.method_label = tk.Label(self, text='Method')
        self.method_combo = ttk.Combobox(
            self, values=[MazeSolverMethods.DFS, MazeSolverMethods.BFS,
                          MazeSolverMethods.UCS, MazeSolverMethods.ASTAR], state='readonly'
        )
        self.method_combo.current(0)
        self.heuristic_label = tk.Label(self, text='Heuristic')
        self.heuristic_combo = ttk.Combobox(
            self, values=[HeuristicMethods.EUCLIDIAN, HeuristicMethods.MANHATTAN], state='readonly'
        )
        self.heuristic_combo.current(0)
        self.help_button = tk.Button(self, text='Help')
        self.gen_button = tk.Button(self, text='Solve', command=self.on_solve)

        self.title_label.grid(row=0, column=0, columnspan=3)
        self.method_label.grid(row=1, column=0)
        self.method_combo.grid(row=1, column=1, columnspan=2)
        self.heuristic_label.grid(row=2, column=0)
        self.heuristic_combo.grid(row=2, column=1, columnspan=2)
        self.cancel_button.grid(row=3, column=0)
        self.gen_button.grid(row=3, column=1)
        self.help_button.grid(row=3, column=2)

    def on_solve(self):
        self.action_opt = (self.method_combo.get(), self.heuristic_combo.get())
        self.do_action = True
        self.destroy()