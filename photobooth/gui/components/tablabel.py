import tkinter as tk

class TabLabel(tk.Label):
    def __init__(self, parent, controller, index, text):
        self.controller = controller
        self.bgcolor = controller["bg"]
        self.unselectedColor = "#808080"

        tk.Label.__init__(self, parent, bg=self.bgcolor, text=text, font=("Droid", 45, "bold"), fg="white", cursor="hand1", borderwidth=5, relief="flat")

        self.index = index

        self.bind("<Button-1>", self.updateSelection)

    def updateSelection(self, event=None):
        self.controller.changeSelected(self.index)

    def select(self):
        self.configure(bg=self.bgcolor)

    def unselect(self):
        self.configure(bg=self.bgcolor)
