import tkinter as tk
from photobooth.settings import config


class StripSelector(tk.Frame):
    def __init__ (self, parent, photostrip, **kwargs):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        if 'selected' in kwargs:
            self.selected = kwargs.get('selected')
        else:
            self.selected = False

        # Get the option passed in if there was one
        if 'option' in kwargs:
            self.option = kwargs.get('option')
        else:
            self.option = 'color'

        # Get preset depending on the option
        if self.option == "grayscale":
            text = "Black & White"
        elif self.option == "both":
            text = "Both"
        else:
            text = "Color"

        # Size the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create the image
        self.photostrip = photostrip
        pic = self.photostrip.getPrintTK(self.option)
        self.image = tk.Label(self, image=pic, bg=self["bg"])
        self.image.grid(row=0, column=0, sticky="nsew") 

        # Create the text
        self.text = tk.Label(self, text=text, bg=self["bg"], font=("Droid", 45, "bold"), fg="white")
        self.text.grid(row=1, column=0, sticky="nsew")

        self.highlightColor = config.get('Apperance', 'secondaryColor')
        if self.selected:
            self.text.configure( bg=self.highlightColor )

    def updatePicture(self):
        pic = self.photostrip.getPrintTK(self.option)
        self.image.configure(image=pic)

    def toggleSelected(self):
        # Change background color
        if self.selected:
            self.untoggle()
        else:
            self.toggleOn()

        # Update the screen 
        self.update()

    def untoggle(self):
        self.selected = False
        self.text.configure(bg=self["bg"])

    def toggleOn(self):
        self.selected = True
        self.text.configure(bg=self.highlightColor)

