import tkinter as tk


class StripSelector(tk.Frame):
    def __init__ (self, parent, photostrip, **kwargs):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        if 'selected' in kwargs:
            self.selected = kwargs.get('selected')
        else:
            self.selected = False

        # Get the option passed in if there was one
        if 'option' in kwargs:
            option = kwargs.get('option')
        else:
            option = 'color'

        # Get preset depending on the option
        if option == "grayscale":
            text = "Black & White"
            pic = photostrip.grayscaleStripTK
        elif option == "both":
            text = "Both"
            pic = photostrip.bothTK
        else:
            text = "Color"
            pic = photostrip.stripTK

        # Size the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create the image
        self.image = tk.Label(self, image=pic, bg=self["bg"])
        self.image.grid(row=0, column=0, sticky="nsew") 

        # Create the text
        self.text = tk.Label(self, text=text, bg=self["bg"], font=("Droid", 45, "bold"), fg="white")
        self.text.grid(row=1, column=0, sticky="nsew")

        self.highlightColor = "#AFF2F1"
        if self.selected:
            self.text.configure( bg=self.highlightColor )

    def toggleSelected(self):
        self.selected = not self.selected

        # Change background color
        if self.selected:
            self.text.configure(bg=self.highlightColor)
        else:
            self.text.configure(bg=self["bg"])

        # Update the screen 
        self.update()

