import tkinter as tk

from photobooth.settings.constants import globe
from photobooth.settings.constants import darksetting
from photobooth.settings.constants import systemFonts

from .togglebutton import ToggleButton
from .colorentry import ColorEntry

class FontEntry(tk.Frame):
    def __init__(self, parent, title=None, callback=None, fontcolor="#FFFFFF", fontfamily=None, fontsize=65, fontstyles=""):
        tk.Frame.__init__(self, parent, bg=parent['bg'])
        # Auto size grid
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Make our bindings to whatever our callback funciton is
        if(callback):
            self.callback = callback
        else:
            self.callback = self.getFont

        # Formatting vars
        pad = globe['fieldPadding']
        halfPad = pad/2
        fontTup = darksetting['font']
        
        # Initialize the header text
        if(title):
            self.headerText = title
            self.header = tk.Label(self, font=fontTup, text=self.headerText, bg=self["bg"], fg=darksetting['fg'])
            self.header.grid(row=0, column=0, pady=(0, pad), columnspan=4)
        else:
            self.headerText = "Font"

        # Set the default font family
        if(fontfamily):
            self.fontfamily = fontfamily
        else:
            self.fontfamily = systemFonts[0]

        # Create the list box for font selection
        self.fontlist = tk.Listbox(self, font=fontTup, selectmode="single", selectbackground="blue", exportselection=False)
        # Insert all font families into the list box
        for index, fontFam in enumerate(systemFonts):
            self.fontlist.insert(tk.END, fontFam)
            if( fontFam == self.fontfamily ):
                self.fontindex = index
        self.fontlist.selection_set(first=0)
        self.fontlist.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=(0, pad))
        self.fontlist.bind('<Button-1>', self.callback)

        # Create a variable to hold the value of the fontsize
        self.fontsize = tk.StringVar()
        self.fontsize.set(fontsize)
        self.fontsize.trace('w', self.callback)
        # Create the font size entry field
        fontvalid = (self.register(self.sizeValidation), '%P', '%S')
        self.sizeEntry = tk.Entry(self, font=fontTup, width=3, relief="flat")
        self.sizeEntry.insert(tk.END, self.fontsize.get())
        self.sizeEntry.config(validate="key", validatecommand=fontvalid)
        self.sizeEntry.grid(row=2, column=0, sticky="nsew", padx=(0, halfPad))

        # Create the bold toggle button
        self.boldButton = ToggleButton(self, font=("", fontTup[1], "bold"), text="B", callback=self.callback, padx=pad, pady=pad)
        self.boldButton.grid(row=2, column=1, sticky="nsew", pady=(halfPad, 0), padx=(halfPad, halfPad))

        # Create the italic toggle button
        self.italicButton = ToggleButton(self, font=("", fontTup[1], "italic"), text="I", callback=self.callback, padx=pad, pady=pad)
        self.italicButton.grid(row=2, column=2, sticky="nsew", pady=(halfPad, 0), padx=(halfPad, halfPad))

        # Create the color picker for font
        self.color = ColorEntry(self, callback=self.callback, color="#FFFFFF", size="compact")
        self.color.grid(row=2, column=3, sticky="nsew", padx=(halfPad, 0))

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
        fontBold = "bold" if self.boldButton.get() else ""
        fontItalic = "italic" if self.italicButton.get() else ""
        fontProps = fontBold + " " + fontItalic
        fontColor = self.color.getColor()
        return ((fontFamily, fontSize,fontProps), fontColor)


