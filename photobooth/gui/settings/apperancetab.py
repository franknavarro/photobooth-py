import tkinter as tk

class ApperanceTab(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#15dbcc")

        self.controller = controller
