import tkinter as tk

from photobooth.settings.constants import globe
from photobooth.settings.constants import darksetting
import photobooth.settings.colors as colors


class ToggleButton(tk.Label):
    def __init__(self, parent, text="", toggled=False, callback=None, bg=darksetting["primary"], fg=darksetting['fg'], font=darksetting['font'], cursor="hand1", **kwargs):
        # Get the background color
        self.unselectedColor = bg
        self.selectedColor = colors.hex_lighten(bg, 0.3)
        currColor = self.selectedColor if toggled else self.unselectedColor

        # Create the label conaining the contents
        tk.Label.__init__(self, parent, text=text, font=font, bg=currColor, fg=fg, cursor=cursor, **kwargs)

        # Create the var that holds the toggled state
        self.toggled = tk.BooleanVar()
        self.toggled.set(toggled)
        if(callback):
            self.toggled.trace('w', callback)

        # Toggle the buttons state when clicked on
        self.bind('<Button-1>', self.toggleState)

    def toggleState(self, event=None):
        if(self.toggled.get()):
            self.toggled.set(False)
            self.config(bg=self.unselectedColor)
        else:
            self.toggled.set(True)
            self.config(bg=self.selectedColor)

    def get(self):
        return self.toggled.get()


        
