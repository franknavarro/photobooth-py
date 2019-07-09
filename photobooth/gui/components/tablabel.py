import tkinter as tk

class TabLabel(tk.Label):
    def __init__(self, parent, controller, index, text):
        self.controller = controller
        self.bgcolor = controller["bg"]

        tk.Label.__init__(self, parent, bg=self.bgcolor, text=text, font=("Droid", 45, "bold"), fg="white", cursor="hand1")

        self.index = index

        # Get the padding around the label
        self.pad = 7
        padHalf = self.pad/2
        if index == 0:
            padding = (0, padHalf)
        elif index == len(controller.tabs) - 1:
            padding = (padHalf, 0)
        else:
            padding = padHalf
        # Update the padding around the label
        self.grid_configure(ipady=20, padx=padding, pady=(0, self.pad))

        self.bind("<Button-1>", self.updateSelection)

    def updateSelection(self, event=None):
        self.controller.changeSelected(self.index)

    def select(self):
        self.configure(bg=self.bgcolor)
        self.grid_configure(pady=0)

    def unselect(self):
        self.configure(bg=self.bgcolor)
        self.grid_configure(pady=(0, self.pad))
