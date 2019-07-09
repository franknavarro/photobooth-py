import tkinter as tk

from photobooth.settings import config
from photobooth.settings.constants import darksetting
from photobooth.settings.constants import globe
from ..components.colorentry import ColorEntry

class ApperanceTab(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        self.controller = controller

        # Initialize the grid to be dynamically resized
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # A Container to hold the entry fields
        self.entryContainer = tk.Frame(self, bg=self["bg"])
        self.entryContainer.grid(row=0, column=1, sticky="nsew", padx=globe['fieldPadding'])
        self.entryContainer.grid_rowconfigure(0, weight=1)
        self.entryContainer.grid_rowconfigure(1, weight=1)
        self.entryContainer.grid_rowconfigure(2, weight=1)
        self.entryContainer.grid_columnconfigure(0, weight=1)

        # Main Color Editor
        mainColor = config.get('Apperance', 'mainColor')
        self.mainColor = ColorEntry(self.entryContainer, callback=self.updatePreviewPane, color=mainColor, title="Main Color", autoComplimentary=True)
        self.mainColor.grid(row=0, column=0)
        # Secondary Color Editor
        secondaryColor = config.get('Apperance', 'secondaryColor')
        self.secondaryColor = ColorEntry(self.entryContainer, callback=self.updatePreviewPane, color=secondaryColor, title="Secondary Color", autoComplimentary=True, complimentaryField=self.mainColor.getColorField())
        self.mainColor.setComplimentaryField(self.secondaryColor.getColorField())
        self.secondaryColor.grid(row=1, column=0)
        # Font Color Editor
        fontColor = config.get('Apperance', 'fontColor')
        self.fontColor = ColorEntry(self.entryContainer, callback=self.updatePreviewPane, color=fontColor, title="Font")
        self.fontColor.grid(row=2, column=0)

        # A Canvas that will preview what the options set in the entry fields
        self.previewPane = tk.Frame(self, bg=self["bg"])
        self.previewPane.grid(row=0, column=0, sticky="nsew")
        self.previewPane.grid_rowconfigure(0, weight=1)
        self.previewPane.grid_rowconfigure(1, weight=1)
        self.previewPane.grid_columnconfigure(0, weight=1)

        self.previewMain = tk.Label(self.previewPane, bg=self.mainColor.getColor(), text="PHOTOBOOTH", fg=self.fontColor.getColor(), font=("Droid", 65, "bold"))
        self.previewMain.grid(row=0, column=0, sticky="nsew")
        self.previewSecondary = tk.Label(self.previewPane, bg=self.secondaryColor.getColor(), text="PHOTOBOOTH", fg=self.fontColor.getColor(), font=("Droid", 65, "bold"))
        self.previewSecondary.grid(row=1, column=0, sticky="nsew")
        self.previewText = tk.Label(self.previewPane, bg=darksetting['secondary'], text="Preview", fg=darksetting['fg'], font=darksetting['font'])
        self.previewText.grid(row=2, column=0, sticky='nsew', ipady=globe['fieldPadding'])


    def save(self):
        print("SAVE")

    def updatePreviewPane(self, *args):
        self.previewMain.configure(bg=self.mainColor.getColor(), fg=self.fontColor.getColor(), font=("Droid", 65, "bold"))
        self.previewSecondary.configure(bg=self.secondaryColor.getColor(), fg=self.fontColor.getColor(), font=("Droid", 65, "bold"))
        
