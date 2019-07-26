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
        self.entryContainer.grid_columnconfigure(0, weight=1)
        self.entryContainer.grid_rowconfigure(0, weight=1)
        self.entryContainer.grid_rowconfigure(1, weight=1)


        # Main Editor
        self.mainContainer = tk.Frame(self.entryContainer, bg=self["bg"])
        self.mainContainer.grid(row=0, column=0, sticky="nsew")

        self.mainLabel = tk.Label(self.mainContainer, text="Main", fg=darksetting['fg'], bg=darksetting['primary'], font=darksetting['font'])
        self.mainLabel.grid(row=0, column=0, sticky="nsew", pady=(pad, padHalf))

        mainColor = config.get('Apperance', 'mainColor')
        self.mainColor = ColorEntry(self.mainContainer, callback=self.updatePreviewPane, color=mainColor, title="Background", autoComplimentary=True, size="compact")
        self.mainColor.grid(row=1, column=0, sticky="nsew", pady=(padHalf, padHalf))

        mainFont = config.getFont('main')
        self.mainFont = FontEntry(self.mainContainer, callback=self.updatePreviewPane, fontcolor=mainFont[1], fontfamily=mainFont[0][0], fontsize=mainFont[0][1], fontstyles=mainFont[0][2])
        self.mainFont.grid(row=2, column=0, sticky="nsew", pady=(padHalf, padHalf))

        self.mainPreviewText = tk.StringVar(self)
        self.mainPreviewText.set("Preview Text 1")
        self.mainPreviewEntry = tk.Entry(self.mainContainer, font=darksetting['font'], textvariable=self.mainPreviewText)
        self.mainPreviewEntry.grid(row=3, column=0, sticky="nsew", pady=(padHalf, padHalf))

        # Secondary Editor
        self.secondaryContainer = tk.Frame(self.entryContainer, bg=self["bg"])
        self.secondaryContainer.grid(row=1, column=0, sticky="nsew")

        self.secondaryLabel = tk.Label(self.secondaryContainer, text="Secondary", fg=darksetting['fg'], bg=darksetting['primary'], font=darksetting['font'])
        self.secondaryLabel.grid(row=4, column=0, sticky="nsew", pady=(pad, padHalf))

        secondaryColor = config.get('Apperance', 'secondaryColor')
        self.secondaryColor = ColorEntry(self.secondaryContainer, callback=self.updatePreviewPane, color=secondaryColor, title="Background", autoComplimentary=True, size="compact")
        self.secondaryColor.grid(row=5, column=0, sticky="nsew", pady=(padHalf, padHalf))

        secondaryFont = config.getFont('secondary')
        self.secondaryFont = FontEntry(self.secondaryContainer, callback=self.updatePreviewPane, fontcolor=secondaryFont[1], fontfamily=secondaryFont[0][0], fontsize=secondaryFont[0][1], fontstyles=secondaryFont[0][2])
        self.secondaryFont.grid(row=6, column=0, sticky="nsew", pady=(padHalf, padHalf))

        self.secondaryPreviewText = tk.StringVar(self)
        self.secondaryPreviewText.set("Preview Text 2")
        self.secondaryPreviewEntry = tk.Entry(self.secondaryContainer, font=darksetting['font'], textvariable=self.secondaryPreviewText)
        self.secondaryPreviewEntry.grid(row=7, column=0, sticky="nsew", pady=(padHalf, padHalf))

        # Make sure each color field has a reference to the other to compute complimentary fields
        self.mainColor.setComplimentaryField(self.secondaryColor.getColorField())
        self.secondaryColor.setComplimentaryField(self.mainColor.getColorField())

        # Preview the options set in the entry fields
        self.previewPane = tk.Frame(self, bg=self["bg"])
        self.previewPane.grid(row=0, column=0, sticky="nsew")
        self.previewPane.grid_rowconfigure(0, weight=1)
        self.previewPane.grid_rowconfigure(1, weight=1)
        self.previewPane.grid_columnconfigure(0, weight=1)

        mainFontVal = self.mainFont.getFont()
        print("Main Initial Font: ", mainFontVal)
        self.previewMain = tk.Label(self.previewPane, bg=self.mainColor.getColor(), textvariable=self.mainPreviewText, fg=mainFontVal[1], font=mainFontVal[0])
        self.previewMain.grid(row=0, column=0, sticky="nsew")


        secondaryFontVal = self.secondaryFont.getFont()
        self.previewSecondary = tk.Label(self.previewPane, bg=self.secondaryColor.getColor(), textvariable=self.secondaryPreviewText, fg=secondaryFontVal[1], font=secondaryFontVal[0])

        self.previewSecondary.grid(row=1, column=0, sticky="nsew")
        self.previewText = tk.Label(self.previewPane, bg=darksetting['secondary'], text="Preview", fg=darksetting['fg'], font=darksetting['font'])
        self.previewText.grid(row=2, column=0, sticky='nsew', ipady=pad)


    def save(self):
        mainFontVal = self.mainFont.getFont()
        secondaryFontVal = self.secondaryFont.getFont()
        saveApperances = {
            'mainColor': self.mainColor.getColor(),
            'mainFontFamily': mainFontVal[0][0],
            'mainFontSize': mainFontVal[0][1],
            'mainFontSettings': mainFontVal[0][2],
            'mainFontColor': mainFontVal[1],

            'secondaryColor': self.secondaryColor.getColor(),
            'secondaryFontFamily': secondaryFontVal[0][0],
            'secondaryFontSize': secondaryFontVal[0][1],
            'secondaryFontSettings': secondaryFontVal[0][2],
            'secondaryFontColor': secondaryFontVal[1]
        }
        return {'Apperance': saveApperances}


    def updatePreviewPane(self, *args):
        mainFontVal = self.mainFont.getFont()
        self.previewMain.configure(bg=self.mainColor.getColor(), fg=mainFontVal[1], font=mainFontVal[0])

        secondaryFontVal = self.secondaryFont.getFont()
        self.previewSecondary.configure(bg=self.secondaryColor.getColor(), fg=secondaryFontVal[1], font=secondaryFontVal[0])
        
