import tkinter as tk

from photobooth.settings import config

# A class to format the bottom and top text of the application
class LabelText(tk.Frame):
    def __init__(self, parent, initText):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        # Size the contents of this Frame appropriately
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Add the text to this frame
        self.text = tk.Label(self, text=initText, font=("Droid", 65, "bold"), bg=self["bg"], fg=config.get('Apperance', 'fontColor'))
        # Position this text in the frame
        self.text.grid(row=0, column=0, sticky="nsew")

    def updateText(self, newText):
        self.text.configure(text=newText)

    def hideText(self):
        self.text.configure(text="")


