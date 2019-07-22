import tkinter as tk

class InteractionsTab(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#15dbcc")

        self.controller = controller

    def save(self):
        print("SAVING INTERACTIONS")
