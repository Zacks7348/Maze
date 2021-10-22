import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class MazeConsole(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.console = ScrolledText(
            self,
            text_wrap=None,
            font=("Courier New", 10, "normal"),
            wrap=tk.WORD,
            state='disabled'
        )
        self.console.pack(anchor='nw', fill='both', expand=True)
        self.console.tag_config('info', foreground='black')
        self.console.tag_config('warning', foreground='orange')
        self.console.tag_config('error', foreground='red2')
    
    def clear(self):
        self.console.config(state='normal')
        self.console.delete('1.0', tk.END)
        self.console.config(state='disabled')

    def info(self, msg):
        self.__write(msg)
    
    def warning(self, msg):
        self.__write(msg, 'warning')
    
    def error(self, msg):
        self.__write(msg, 'error')

    def __write(self, msg, tag='info'):
        self.console.config(state='normal')
        self.console.insert(tk.INSERT, msg+'\n', tag)
        self.console.config(state='disabled')