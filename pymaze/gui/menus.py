import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import os

from pymaze.gui.states import AppState
from pymaze.gui.frames import GenerateWindow, SolveWindow


class MainMenu(tk.Menu):
    def __init__(self, master: tk.Tk, app):
        self.app = app
        super().__init__(master, tearoff=False)
        self.master.config(menu=self)

        self.file_menu = FileMenu(master, self.app)

        self.add_cascade(label='File', menu=self.file_menu)
        self.add_command(label='Generate', command=self.on_generate)
        self.add_command(label='Solve', command=self.on_solve)

    def on_generate(self):
        g = GenerateWindow(self)
        self.wait_window(g)
        if not g.do_action:
            return
        self.app.maze.generate(*g.action_opt)

    def on_solve(self):
        s = SolveWindow(self)
        self.wait_window(s)
        if not s.do_action:
            return
        self.app.maze.solve(*s.action_opt)


class FileMenu(tk.Menu):
    def __init__(self, master, app):
        self.app = app
        super().__init__(master, tearoff=False)
        self.add_command(label='Open', command=self.on_open)
        self.add_separator()
        self.add_command(label='Save As', command=self.on_save_as)
        self.add_separator()
        self.add_command(label='Exit', command=self.on_exit)

    def on_open(self):
        file_dir = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Open File",
            filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
            defaultextension="*.txt",
        )
        if file_dir:
            self.app.maze.open_maze(file_dir)

    def on_save_as(self):
        # Only is enabled when state is maze
        file_dir = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title='Save As',
            filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
            defaultextension="*.txt",
        )
        if file_dir:
            try:
                self.app.maze.maze.to_file(file_dir)
            except:
                # self.app.console.error('Could not save to file!')
                pass


    def on_exit(self):
        self.master.destroy()
