import tkinter as tk

class App():
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.geometry('1000x500')
        self.root.minsize(1000, 500)
        self.root.title("Python Maze")
        