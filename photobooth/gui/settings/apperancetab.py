import tkinter as tk

from photobooth.settings import config
from photobooth.settings.constants import darksetting
from photobooth.settings.constants import globe

from ..components.colorentry import ColorEntry
from ..components.fontentry import FontEntry

class ApperanceTab(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        self.controller = controller

        # Constants for formatting
        pad = globe['fieldPadding']
        padHalf = pad/2

        # Initialize the grid to be dynamically resized
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # A Container to hold the entry fields
        self.entryContainer = tk.Frame(self, bg=self["bg"])
        self.entryContainer.grid(row=0, column=1, sticky="nsew", padx=pad)
        self.entryContainer.grid_rowconfigure(2, weight=1)
        self.entryContainer.grid_columnconfigure(0, weight=1)

        # Main Color Editor
        mainColor = config.get('Apperance', 'mainColor')
        self.mainColor = ColorEntry(self.entryContainer, callback=self.updatePreviewPane, color=mainColor, title="Main Color", autoComplimentary=True, size="")
        self.mainColor.grid(row=0, column=0, sticky="nsew", pady=(pad, padHalf))
        # Secondary Color Editor
        secondaryColor = config.get('Apperance', 'secondaryColor')
        self.secondaryColor = ColorEntry(self.entryContainer, callback=self.updatePreviewPane, color=secondaryColor, title="Secondary Color", autoComplimentary=True, complimentaryField=self.mainColor.getColorField(), size="compact")
        self.mainColor.setComplimentaryField(self.secondaryColor.getColorField())
        self.secondaryColor.grid(row=1, column=0, sticky="nsew", pady=(padHalf, padHalf))
        # Font Color Editor
        self.fontColor = config.get('Apperance', 'fontColor')
        self.fontEntry = FontEntry(self.entryContainer, title="Font", callback=self.updatePreviewPane)
        self.fontEntry.grid(row=2, column=0, sticky="nsew", pady=(padHalf, 0))

        # A Canvas that will preview what the options set in the entry fields
        self.previewPane = tk.Frame(self, bg=self["bg"])
        self.previewPane.grid(row=0, column=0, sticky="nsew")
        self.previewPane.grid_rowconfigure(0, weight=1)
        self.previewPane.grid_rowconfigure(1, weight=1)
        self.previewPane.grid_columnconfigure(0, weight=1)

        fontVal = self.fontEntry.getFont()
        self.previewMain = tk.Label(self.previewPane, bg=self.mainColor.getColor(), text="PHOTOBOOTH", fg=fontVal[1], font=fontVal[0])
        self.previewMain.grid(row=0, column=0, sticky="nsew")
        self.previewSecondary = tk.Label(self.previewPane, bg=self.secondaryColor.getColor(), text="PHOTOBOOTH", fg=fontVal[1], font=fontVal[0])
        self.previewSecondary.grid(row=1, column=0, sticky="nsew")
        self.previewText = tk.Label(self.previewPane, bg=darksetting['secondary'], text="Preview", fg=darksetting['fg'], font=darksetting['font'])
        self.previewText.grid(row=2, column=0, sticky='nsew', ipady=pad)



    def save(self):
        print("SAVE")

    def updatePreviewPane(self, *args):
        fontVal = self.fontEntry.getFont()
        self.previewMain.configure(bg=self.mainColor.getColor(), fg=fontVal[1], font=fontVal[0])
        self.previewSecondary.configure(bg=self.secondaryColor.getColor(), fg=fontVal[1], font=fontVal[0])
        
