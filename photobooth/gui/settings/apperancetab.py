import tkinter as tk

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

        # Initialize the header text
        headerText = "Main Color: " if colorType == 'mainColor' else "Secondary Color: "
        self.header = tk.Label(parent, font=parent.font, text=headerText, bg=parent["bg"], fg="white")
        self.header.grid(row=row, column=0, sticky="nse", pady=parent.bottomPadding)

        # Initialize the text entry field
        self.entry = tk.Entry(parent, font=("", parent.font[1]), width=8, relief="flat", textvariable=self.color)
        self.entry.grid(row=row, column=1, sticky="nsew", pady=parent.bottomPadding)
