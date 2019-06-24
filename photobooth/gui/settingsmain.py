import tkinter as tk

from .settings.apperancetab import ApperanceTab
from .settings.interactionstab import InteractionsTab
from .settings.photostriptab import PhotostripTab

class SettingsMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        self.controller = controller

        # Initialize the grid for the page
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)

        self.tabs = (ApperanceTab, InteractionsTab, PhotostripTab)

        # Set up the container where the tabs will be displayed
        self.container = tk.Frame(self, bg=self["bg"])
        self.container.grid(row=1, column=0, columnspan=len(self.tabs), sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


        # Initialize the different settings tabs
        self.frames = {}
        for index, tab in enumerate(self.tabs):
            # Initialize the tab column that this will be in
            self.grid_columnconfigure(index, weight=1)
            # Initialize the page assosiated with the tab
            frame = tab(self.container, self)
            self.frames[tab] = frame
            frame.grid(row=0, column=0, stick="nsew")


    # Perform any initial configurations
    def open(self):
        # Reshow the arrow
        self.configure(cursor='arrow')
        # Bind the close key
        self.bind('x', self.close)
        self.show_frame(self.tabs[0])

    # Function that will show the correct tab page
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.focus_set()

    # Show the main application once again and unbind the close button
    def close(self, event=None):
        # Rehide the cursor
        self.configure(cursor='none')
        # Unbind the close button
        self.unbind('x')
        # Show the main application
        self.controller.showMain()





