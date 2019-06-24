import tkinter as tk

class PhotostripTab(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#48a90a")

        self.controller = controller
