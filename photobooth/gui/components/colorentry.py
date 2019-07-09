import tkinter as tk
from tkinter import colorchooser

import photobooth.settings.colors as colorconvert

from photobooth.settings.constants import globe
from photobooth.settings.constants import darksetting

from .hoverbutton import HoverButton
from photobooth.settings import config

class ColorEntry():
    def __init__(self, parent, row=None, title="Color", color="#000000", autoComplimentary=False, complimentaryField=None):
        sidePadding = (globe['fieldPadding'], globe['fieldPadding'])
        bottomPadding = (0, globe['fieldPadding'])

        # Set the color for the field
        self.colorField = tk.StringVar()
        self.colorField.set(color)
        self.colorField.trace("w", self.updateColorBox)
        # Set the complimentary color field provided
        if(complimentaryField):
            self.complimentaryField = complimentaryField
        # Set a default complimentary color
        else:
            self.complimentaryField = tk.StringVar()
            self.complimentaryField.set("#000000")

        # Initialize the header text
        self.headerText = title
        self.header = tk.Label(parent, font=darksetting['font'], text=self.headerText+":", bg=parent["bg"], fg=darksetting['fg'])
        self.header.grid(row=row, column=0, sticky="nse", pady=bottomPadding)

        # Initialize the text entry field
        self.entry = tk.Entry(parent, font=darksetting['font'], width=8, relief="flat", textvariable=self.colorField, state="readonly", readonlybackground="white")
        self.entry.grid(row=row, column=1, sticky="nsew", pady=bottomPadding, padx=sidePadding)
        self.entry.bind('<Button-1>', self.colorPicker)

        # Show a preview box of the color entry
        parent.update_idletasks()
        previewSize = self.entry.winfo_height()
        self.previewCanvas = tk.Canvas(parent, width=previewSize, height=previewSize)
        self.preview = self.previewCanvas.create_rectangle(0, 0, previewSize, previewSize, fill=self.colorField.get())
        self.previewCanvas.grid(row=row, column=2, sticky="nsw", pady=bottomPadding)

        # Get things depending on wether using main or secondary color
        if ( autoComplimentary ):
            self.autoButton = HoverButton(parent, text="Get Complimentary", command=self.computeComplimentary)
            self.autoButton.grid(row=row, column=3, sticky="nsw", pady=bottomPadding, padx=sidePadding)


    # Helper function to get and return the color field to use as a reference else where
    def getColorField(self):
        return self.colorField
    # Helper function to return the value within the color field
    def getColor(self):
        return self.colorField.get()

    # Call back function for computing complimentary color
    def computeComplimentary(self):
        complimentary = colorconvert.hex_complimentary(self.complimentaryField.get())
        self.colorField.set(complimentary)

    # Reviels the color picker field (OS dependant)
    def colorPicker(self, event=None):
        tempColor = colorchooser.askcolor(initialcolor=self.colorField.get(), title=self.headerText)
        if(tempColor[1]):
            self.colorField.set(tempColor[1].upper())

    # Call back function for updating the preview box whenever the colorField variable changes
    def updateColorBox(self, *args):
        self.previewCanvas.itemconfig(self.preview, fill=self.colorField.get())

