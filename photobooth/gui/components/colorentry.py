import tkinter as tk
from tkinter import colorchooser

import photobooth.settings.colors as colorconvert

from photobooth.settings.constants import globe
from photobooth.settings.constants import darksetting

from .hoverbutton import HoverButton

class ColorEntry(tk.Frame):
    def __init__(self, parent, title=None, callback=None, color="#000000", autoComplimentary=False, complimentaryField=None, size=None):
        tk.Frame.__init__(self, parent, bg=parent['bg'])

        # Formatting vars
        pad = globe['fieldPadding']
        padHalf = globe['fieldPadding']/2

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
        if( title ):
            self.headerText = title
        else:
            self.headerText = "Color"
        # Create the header 
        self.header = tk.Label(self, font=darksetting['font'], text=self.headerText, bg=self["bg"], fg=darksetting['fg'])

        # Show a button to auto get the complimentary color 
        self.autoButton = HoverButton(self, text="Get Complimentary", command=self.computeComplimentary)

        # Initialize the text entry field
        self.entry = tk.Entry(self, font=darksetting['font'], width=8, relief="flat", textvariable=self.colorField, state="readonly", readonlybackground="white")
        self.entry.bind('<Button-1>', self.colorPicker)

        # Create a Preview Box
        self.previewBox = HoverButton(self, bg=self.colorField.get(), command=self.colorPicker)
        # self.previewBox.bind('<Button-1>', self.colorPicker)

        if(size == "compact"):
            # Dynamically size everything
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)
            # Place the header
            if( title ):
                self.header.config(text=self.headerText + ":")
                self.header.grid(row=0, column=0, sticky="nsew", padx=(0, padHalf))
            # Place the auto complimentary button
            if( autoComplimentary ):
                self.autoButton.config(text="C")
                self.autoButton.grid(row=0, column=2, sticky="nsew", padx=(pad, 0))
            # Place the preview box
            self.previewBox.grid(row=0, column=1, sticky="nsew")
        else:
            # Dynamically size everything
            self.grid_columnconfigure(2, weight=1)
            self.grid_columnconfigure(3, weight=2)
            self.grid_rowconfigure(0, weight=1)
            # Place the header
            if( title ):
                self.grid_columnconfigure(0, weight=2)
                self.header.grid(row=0, column=0, columnspan=4, sticky="sew", pady=(0, pad))
            # place the auto complimenatry button
            if( autoComplimentary ):
                self.grid_columnconfigure(0, weight=2)
                self.autoButton.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=(0, pad))
            # Place the entry field
            self.entry.grid(row=2, column=1, sticky="nsew")
            # Place the preview box
            self.previewBox.grid(row=2, column=2, sticky="nsew")




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
        self.previewBox.config(bg=self.colorField.get())

    # Reviels the color picker field (OS dependant)
    def colorPicker(self, event=None):
        tempColor = colorchooser.askcolor(initialcolor=self.colorField.get(), title=self.headerText)
        if(tempColor[1]):
            self.colorField.set(tempColor[1].upper())
            self.previewBox.config(bg=self.colorField.get())

