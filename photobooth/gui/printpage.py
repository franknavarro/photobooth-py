import tkinter as tk

class PrintPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])
        print("Starting Printing Process")
