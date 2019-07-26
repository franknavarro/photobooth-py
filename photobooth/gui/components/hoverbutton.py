# A new tkinter button that keeps the same background color when you hover over it

import tkinter as tk

from photobooth.settings.constants import darksetting

class HoverButton(tk.Button):
    def __init__(self, master, font=darksetting['font'], fg=darksetting['fg'], bg=darksetting['primary'], cursor='hand1', **kw):
        tk.Button.__init__(self, master=master, fg=fg, font=font, bg=bg, cursor=cursor, **kw)

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

    def changeBackground(self, color):
        self.defaultBackground = color
        self['background'] = self.defaultBackground
        self['activebackground'] = self.defaultBackground
