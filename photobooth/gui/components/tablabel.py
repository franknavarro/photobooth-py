import tkinter as tk

from photobooth.settings.constants import darksetting

class TabLabel(tk.Label):
    def __init__(self, parent, controller, index, text, bgcolor=darksetting['primary'], unselectedcolor=darksetting['secondary'], font=darksetting['font'], fg=darksetting['fg'], cursor='hand1'):
        self.controller = controller
        self.bgcolor = bgcolor
        self.unselectedcolor = unselectedcolor

        tk.Label.__init__(self, parent, bg=self.unselectedcolor, text=text, font=font, fg=fg, cursor=cursor)

        self.grid_configure(ipadx=20, ipady=20)

        self.index = index

        self.bind("<Button-1>", self.updateSelection)

    def updateSelection(self, event=None):
        self.controller.changeSelected(self.index)

    def select(self):
        self.configure(bg=self.bgcolor)

    def unselect(self):
        self.configure(bg=self.unselectedcolor)
