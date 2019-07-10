import tkinter as tk
from tkinter import font

from photobooth.settings.constants import globe
from photobooth.settings.constants import darksetting

class FontEntry(tk.Frame):
    def __init__(self, parent, title=None, callback=None, fontcolor="#FFFFFF", fontfamily=None, fontsize=65, fontstyles=""):
        tk.Frame.__init__(self, parent, bg=parent['bg'])
        # Auto size grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Initialize the header text
        if(title):
            self.headerText = title
            self.header = tk.Label(self, font=darksetting['font'], text=self.headerText, bg=self["bg"], fg=darksetting['fg'])
            self.header.grid(row=0, column=0, pady=(0, globe['fieldPadding']/2))
        else:
            self.headerText = "Font"

        # Remove any duplicate font familes and sort them in alphabetical order
        fontfamilies = sorted( list( dict.fromkeys(font.families()) ) )
        # Set the default font family
        if(fontfamily):
            self.fontfamily = fontfamily
        else:
            self.fontfamily = fontfamilies[0]

        # Create the list box for font selection
        self.fontlist = tk.Listbox(self, font=darksetting['font'], selectmode="single")
        # Insert all font families into the list box
        for index, fontFam in enumerate(fontfamilies):
            self.fontlist.insert(tk.END, fontFam)
            if( fontFam == self.fontfamily ):
                self.fontindex = index
        self.fontlist.selection_set(first=0)
        self.fontlist.grid(row=1, column=0, sticky="nsew")

        # Make our bindings to whatever our callback funciton is
        if(callback):
            self.fontlist.bind('<Button-1>', callback)

    def getFont(self):
        fontFamily = self.fontlist.get(tk.ACTIVE)
        return (fontFamily, 65, "bold")


