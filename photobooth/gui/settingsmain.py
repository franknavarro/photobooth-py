import tkinter as tk

from .settings.apperancetab import ApperanceTab
from .settings.interactionstab import InteractionsTab
from .settings.photostriptab import PhotostripTab

from .components.tablabel import TabLabel

class SettingsMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        self.controller = controller

        # Initialize the grid for the page
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Set up the tabs and their container frame
        self.tabs = (ApperanceTab, InteractionsTab, PhotostripTab)
        self.tabNames = ("Apperances", "Interactions", "Photostrip")
        self.tabFrame = tk.Frame(self, bg="#808080")
        self.tabFrame.grid(row=0, column=0, sticky="nsew")
        self.tabFrame.grid_rowconfigure(0, weight=1)

        # Set up the container where the tabs will be displayed
        self.container = tk.Frame(self, bg=self["bg"])
        self.container.grid(row=1, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


        # Initialize the different settings tabs
        self.frames = []
        self.tabLabels = []
        self.activeTab = 0
        for index, tab in enumerate(self.tabs):
            # Initialize the tab column that this will be in
            self.tabFrame.grid_columnconfigure(index, weight=1)
            tabLabel = TabLabel(self.tabFrame, self, index, self.tabNames[index])
            self.tabLabels.append(tabLabel)
            # Get the padding around the label
            pad = 7
            padHalf = pad/2
            if index == 0:
                padding = (0, padHalf)
            elif index == len(self.tabs) - 1:
                padding = (padHalf, 0)
            else:
                padding = padHalf
            tabLabel.grid(row=0, column=index, sticky="nsew", ipady=20, padx=padding, pady=(0, pad))
            # Initialize the page assosiated with the tab
            frame = tab(self.container, self)
            self.frames.append(frame)
            frame.grid(row=0, column=0, stick="nsew")


    # Perform any initial configurations
    def open(self):
        # Reshow the arrow
        self.configure(cursor='arrow')
        self.changeSelected(0)

    # Çhange the selected tab to the new index selected tab
    def changeSelected(self, newTab):
        self.tabLabels[self.activeTab].unselect()
        self.tabLabels[self.activeTab].grid_configure(pady=(0, 7))
        self.activeTab = newTab
        self.tabLabels[newTab].select()
        self.tabLabels[newTab].grid_configure(pady=0)
        frame = self.frames[newTab]
        frame.tkraise()
        frame.focus_set()

    # Function that will show the correct tab page
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.focus_set()

    # Show the main application once again 
    def close(self, event=None):
        # Rehide the cursor
        self.configure(cursor='none')
        # Show the main application
        self.controller.showMain()





