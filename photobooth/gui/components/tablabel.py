import tkinter as tk

class TabLabel(tk.Label):
    def __init__(self, parent, index, text):
        self.selectedColor = parent["bg"]
        self.unselectedColor = "#808080"

        tk.Label.__init__(self, parent, bg=self.unselectedColor, text=text, font=("Droid", 45, "bold"), fg="white", cursor="hand1")

        self.parent = parent

        self.index = index


        self.bind("<Button-1>", self.updateSelection)

    def updateSelection(self, event=None):
        self.parent.changeSelected(self.index)

    def select(self):
        self.configure(bg=self.selectedColor)

    def unselect(self):
        self.configure(bg=self.unselectedColor)
