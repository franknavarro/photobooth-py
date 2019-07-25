import tkinter as tk
import sys

from .mainapplication import MainApplication
from .settingsmain import SettingsMain
from photobooth.settings import config

class RootWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Window size of application
        self.attributes('-fullscreen', True)
        #self.geometry("500x500")

        # Name of application
        self.title('Photobooth')

        # Hide cursor
        self.configure(cursor='none')


        # Create container to hold all frames
        self.container = tk.Frame(self, bg=config.get('Apperance', 'mainColor'))
        self.container.pack(side="top", fill="both", expand=True)

        # Center container in window
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Set up all the frames used in the app
        self.frames = {}
        for page in (MainApplication, SettingsMain):
            frame = page(self.container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, stick="nsew")

        # Bind the Escape Key to close the application
        self.bind('<Escape>', self.close)

        # Save an instance of the camera page here used for binding references
        self.campage = self.frames[MainApplication].getCameraPage()

        # Show the start page to begin with
        self.showMain()

    
    # Function to display a loaded frames in the app
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.open()
        frame.tkraise()
        frame.focus_set()

    # Show the settings page
    def showSettings(self, event=None):
        # Unbind the key to show the settings page
        self.unbind('s')
        # Stop the camera
        self.campage.camera.stop()
        self.unbind('<space>')
        # Show the settings page
        self.show_frame(SettingsMain)

    def restartMain(self):
        # Close the camera instance to avoid resource error
        self.campage.camera.close()
        # Remove reference to original application frame
        oldApp = self.frames[MainApplication]
        oldApp.grid_forget()
        oldApp.destroy()
        del self.frames[MainApplication]
        del oldApp
        # Re-initialize the entire application
        self.container.configure(bg=config.get('Apperance', 'mainColor'))
        mainapp = MainApplication(self.container, self)
        self.frames[MainApplication] = mainapp
        mainapp.grid(row=0, column=0, stick="nsew")
        self.show_frame(SettingsMain)
        # Save the new camera page created
        self.campage = mainapp.getCameraPage()


    # Show the Main Application
    def showMain(self, event=None):
        # Bind the 's' key to the settings menu
        self.bind('s', self.showSettings)
        # Bind the 'space bar to the captues screen
        self.bind('<space>', self.startApplication)
        self.show_frame(MainApplication)

    # Start taking the pictures and unbind key presses to not mess with things
    def startApplication(self, event=None):
        self.unbind('<space>')
        self.unbind('s')
        self.campage.startCaptures()
        

    # Function to get the size of the window
    def get_size(self):
        self.update_idletasks()
        return (self.winfo_width(), self.winfo_height())

    # Function to quit the app
    def close(self, event):
        sys.exit()
