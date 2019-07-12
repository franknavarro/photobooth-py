import tkinter as tk
from tkinter import font

dud = tk.Tk()
systemFonts = sorted( ( list( dict.fromkeys(font.families()) ) ) )
dud.destroy()

globe = {
    "fieldPadding": 20,
    "font": (systemFonts[0], 45, "bold"),
    "fontColor": "white"
}

# Used in settings page
darksetting = {
    "font": (systemFonts[0], 25),
    "fg": "white",
    "primary": "#1B1B1B",
    "secondary": "#484848"
}

