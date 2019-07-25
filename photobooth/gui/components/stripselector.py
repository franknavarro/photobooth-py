import tkinter as tk
from photobooth.settings import config


class StripSelector(tk.Frame):
    def __init__ (self, parent, photostrip, selected=False, option='color', **kwargs):
        tk.Frame.__init__(self, parent, bg=parent["bg"], **kwargs)

        # Get the toggled background color
        if 'toggleHighlight' in kwargs:
            toggleHighlight = kwargs.get('toggleHighlight')
        else:
            toggleHighlight = config.get('Apperance', 'secondaryColor')

        # Get the font used
        if 'font' in kwargs:
            font = kwargs.get('font')
        else:
            font = config.getFont('secondary')

        self.selected = selected
        self.option = option

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
        self.text = tk.Label(self, text=text, bg=self["bg"], font=font[0], fg=font[1])
        self.text.grid(row=1, column=0, sticky="nsew")

        self.highlightColor = toggleHighlight
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

