import tkinter as tk

from photobooth.settings import config
from ..components.colorentry import ColorEntry

class ApperanceTab(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        self.controller = controller

        # Initialize the first and last column to be dynamically resized
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        # Initialize the first and last row to be dynamically resized
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Main Color Editor
        mainColor = config.get('Apperance', 'mainColor')
        self.mainColor = ColorEntry(self, row=1, color=mainColor, title="Main Color")
        # Secondary Color Editor
        secondaryColor = config.get('Apperance', 'secondaryColor')
        self.secondaryColor = ColorEntry(self, row=2, color=secondaryColor, title="Secondary Color", autoComplimentary=True, complimentaryField=self.mainColor.getColorField())
        
        # Font Color Editor
        self.fontColor = ColorEntry(self, row=3, color=config.get('Apperance', 'fontColor'), title="Font Color")

    def save(self):
        print("SAVE")
