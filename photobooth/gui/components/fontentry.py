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

        # Make our bindings to whatever our callback funciton is
        if(callback):
            self.callback = callback
        else:
            self.callback = self.getFont

        # Padding
        pad = globe['fieldPadding']
        halfPad = pad/2
        
        # Initialize the header text
        if(title):
            self.headerText = title
            self.header = tk.Label(self, font=darksetting['font'], text=self.headerText, bg=self["bg"], fg=darksetting['fg'])
            self.header.grid(row=0, column=0, pady=(0, halfPad))
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
        self.fontlist.grid(row=1, column=0, sticky="nsew", pady=(halfPad, halfPad))
        self.fontlist.bind('<Button-1>', self.callback)

        # Create a variable to hold the value of the fontsize
        self.fontsize = tk.StringVar()
        self.fontsize.set(fontsize)
        self.fontsize.trace('w', self.callback)
        # Create the font size entry field
        fontvalid = (self.register(self.sizeValidation), '%P', '%S')
        self.sizeEntry = tk.Entry(self, font=darksetting['font'], width=3, relief="flat")
        self.sizeEntry.insert(tk.END, self.fontsize.get())
        self.sizeEntry.config(validate="key", validatecommand=fontvalid)
        self.sizeEntry.grid(row=2, column=0, sticky="nsew", pady=(halfPad, 0), padx=(0, halfPad))


    def sizeValidation(self, textafter, textinserted):
        # Only allow digit entries 
        if textinserted.isdigit():
            self.fontsize.set(textafter)
            return True
        else:
            return False
        

    def getFont(self):
        fontFamily = self.fontlist.get(tk.ACTIVE)
        fontSize = 0 if self.fontsize.get() == "" else self.fontsize.get()
        return (fontFamily, fontSize, "bold")


