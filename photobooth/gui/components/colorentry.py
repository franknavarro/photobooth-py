import tkinter as tk
from tkinter import colorchooser

import photobooth.settings.colors as colorconvert

from photobooth.settings.constants import globe
from photobooth.settings.constants import darksetting

from .hoverbutton import HoverButton
from photobooth.settings import config

class ColorEntry(tk.Frame):
    def __init__(self, parent, title=None, callback=None, color="#000000", autoComplimentary=False, complimentaryField=None):
        tk.Frame.__init__(self, parent, bg=parent['bg'])
        # Take up the full row height
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Set the color for the field
        self.colorField = tk.StringVar()
        self.colorField.set(color)
        if(callback):
            self.colorField.trace("w", callback)


        # Set the complimentary color field provided
        if(complimentaryField):
            self.complimentaryField = complimentaryField
        # Set a default complimentary color
        else:
            self.complimentaryField = tk.StringVar()
            self.complimentaryField.set("#000000")

        # Initialize the header text
        if(title):
            self.headerText = title
            self.header = tk.Label(self, font=darksetting['font'], text=self.headerText, bg=self["bg"], fg=darksetting['fg'])
            self.header.grid(row=0, column=0, columnspan=3, sticky="sew", pady=(0, globe['fieldPadding']/2))
        else:
            self.headerText = "Color"

        # Show a button to auto get the complimentary color 
        if ( autoComplimentary ):
            self.autoButton = HoverButton(self, text="Get Complimentary", command=self.computeComplimentary)
            self.autoButton.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(globe['fieldPadding']/2, globe['fieldPadding']/2))

        # Initialize the text entry field
        self.entry = tk.Entry(self, font=darksetting['font'], width=8, relief="flat", textvariable=self.colorField, state="readonly", readonlybackground="white")
        self.entry.grid(row=2, column=1, sticky="new", pady=(globe['fieldPadding']/2, globe['fieldPadding']*2))
        self.entry.bind('<Button-1>', self.colorPicker)

    # Helper function to get and return the color field to use as a reference else where
    def getColorField(self):
        return self.colorField
    # Helper function to return the value within the color field
    def getColor(self):
        return self.colorField.get()

    # Set a field for a complimentary color calculation
    def setComplimentaryField(self, field):
        self.complimentaryField = field

    # Call back function for computing complimentary color
    def computeComplimentary(self):
        complimentary = colorconvert.hex_complimentary(self.complimentaryField.get())
        self.colorField.set(complimentary)

    # Reviels the color picker field (OS dependant)
    def colorPicker(self, event=None):
        tempColor = colorchooser.askcolor(initialcolor=self.colorField.get(), title=self.headerText)
        if(tempColor[1]):
            self.colorField.set(tempColor[1].upper())

