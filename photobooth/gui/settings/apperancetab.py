import tkinter as tk
from tkinter import colorchooser

from photobooth.settings import config

class ApperanceTab(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        self.controller = controller
        # Constant variables used for formatting
        self.font = ("Droid", 45, "bold")
        self.bottomPadding = (0, 10)

        # Initialize the first and last column to be dynamically resized
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        # Initialize the first and last row to be dynamically resized
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Main Color Editor
        self.mainColor = ColorEntry(self, 1, "mainColor")

        # Secondary Color Editor
        self.secondaryColor = ColorEntry(self, 2, "secondaryColor")


class ColorEntry():
    def __init__(self, parent, row, colorType):

        # Set the color for the field
        self.color = tk.StringVar()
        self.color.set(config.get('Apperance', colorType))
        self.color.trace("w", self.updateColorBox)

        # Initialize the header text
        self.headerText = "Main Color" if colorType == 'mainColor' else "Secondary Color"
        self.header = tk.Label(parent, font=parent.font, text=self.headerText+":", bg=parent["bg"], fg="white")
        self.header.grid(row=row, column=0, sticky="nse", pady=parent.bottomPadding)


        # Initialize the text entry field
        self.entry = tk.Entry(parent, font=("", parent.font[1]), width=8, relief="flat", textvariable=self.color, state="readonly", readonlybackground="white")
        self.entry.grid(row=row, column=1, sticky="nsew", pady=parent.bottomPadding, padx=(20, 20))
        self.entry.bind('<Button-1>', self.colorPicker)

        # Show a preview box of the color entry
        parent.update_idletasks()
        previewSize = self.entry.winfo_height()
        self.previewCanvas = tk.Canvas(parent, width=previewSize, height=previewSize)
        self.preview = self.previewCanvas.create_rectangle(0, 0, previewSize, previewSize, fill=self.color.get())
        self.previewCanvas.grid(row=row, column=2, sticky="nsw", pady=parent.bottomPadding)


    def colorPicker(self, event=None):
        tempColor = colorchooser.askcolor(initialcolor=self.color.get(), title=self.headerText)
        if(tempColor[1]):
            self.color.set(tempColor[1])
        #else:
            #print("CANCELLED COLOR PICKER")

    def updateColorBox(self, *args):
        self.previewCanvas.itemconfig(self.preview, fill=self.color.get())

