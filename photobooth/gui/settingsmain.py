import tkinter as tk

from .settings.apperancetab import ApperanceTab
from .settings.interactionstab import InteractionsTab
from .settings.photostriptab import PhotostripTab

from .components.tablabel import TabLabel
from .components.hoverbutton import HoverButton

from  photobooth.settings.constants import globe
from  photobooth.settings.constants import darksetting

from photobooth.settings import config

class SettingsMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=darksetting["primary"])

        self.controller = controller

        # Initialize the grid for the page
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Set up the tabs and their container frame
        self.tabs = (ApperanceTab, InteractionsTab, PhotostripTab)
        self.tabNames = ("Apperances", "Interactions", "Photostrip")
        self.tabFrame = tk.Frame(self, bg=self["bg"])
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
            tabLabel.grid(row=0, column=index, sticky="nsew", )
            # Initialize the page assosiated with the tab
            frame = tab(self.container, self)
            self.frames.append(frame)
            frame.grid(row=0, column=0, stick="nsew")

        # Initialize the frame to hold the the save and exit buttons
        self.saveContainer = tk.Frame(self, bg=self["bg"])
        self.saveContainer.grid(row=2, column=0, sticky="nsew")
        self.saveContainer.grid_rowconfigure(0, weight=1)
        self.saveContainer.grid_columnconfigure(0, weight=1)
        # Create Save Button
        savePadding = (globe['fieldPadding'], globe['fieldPadding']/2)
        self.saveButton = HoverButton(self.saveContainer, text="Save", command=self.save)
        self.saveButton.grid(row=0, column=1, pady=globe['fieldPadding'], padx=savePadding)
        # Create Exit Button
        exitPadding = (globe['fieldPadding']/2, globe['fieldPadding'])
        self.exitButton = HoverButton(self.saveContainer, text="Exit", command=self.close)
        self.exitButton.grid(row=0, column=2, pady=globe['fieldPadding'], padx=exitPadding)

    # Call the save function for the relative tab
    def save(self):
        # Go through and update each relevant config
        saveConfigs = self.frames[self.activeTab].save()
        for settingField, settings in saveConfigs.items():
            for setting, settingVal in settings.items():
                config[settingField][setting] = settingVal

        # Save the file
        config.saveToFile()


    # Perform any initial configurations
    def open(self):
        # Reshow the arrow
        self.configure(cursor='arrow')
        self.changeSelected(0)

    # Çhange the selected tab to the new index selected tab
    def changeSelected(self, newTab):
        self.tabLabels[self.activeTab].unselect()
        self.activeTab = newTab
        self.tabLabels[newTab].select()
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





