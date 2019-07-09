# A new tkinter button that keeps the same background color when you hover over it

import tkinter as tk

from photobooth.settings import config

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self["fg"] = config.get('Apperance', 'fontColor')
        self["bg"] = config.get('Apperance', 'secondaryColor')
        self['font'] = ("Droid", 25, "bold")
        self['cursor'] = "hand1"

        self.defaultBackground = self['background']
        self.defaultFontColor = self['foreground']
        self['activebackground'] = self.defaultBackground
        self['activeforeground'] = self.defaultFontColor

        self.bind("<Enter>", self.onEnter)
        self.bind("<Leave>", self.onLeave)

    def onEnter(self, e):	
        self['background'] = self.defaultBackground
        self['foreground'] = self.defaultFontColor

    def onLeave(self, e):
        self['background'] = self.defaultBackground
        self['foreground'] = self.defaultFontColor
