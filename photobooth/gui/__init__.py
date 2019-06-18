import tkinter as tk
import sys

from .mainapplication import MainApplication
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

        # Bind the Escape Key to close the application
        self.bind('<Escape>', self.close)

        # Create container to hold all frames
        self.container = tk.Frame(self, bg=config.get('Apperance', 'mainColor'))
        self.container.pack(side="top", fill="both", expand=True)

        # Center container in window
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Set up all the frames used in the app
        self.frames = {}

        # Show the start page to begin with
        self.load_frame(MainApplication)
        self.show_frame(MainApplication)

    
    # Function to display a loaded frames in the app
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.focus_set()
        frame.tkraise()

    # Loads in the container from a class and then displays it
    def load_frame(self, cont):
        frame = cont(self.container, self)
        self.frames[cont] = frame
        frame.grid(row=0, column=0, stick="nsew")

    def get_size(self):
        self.update_idletasks()
        return (self.winfo_width(), self.winfo_height())

    # Function to quit the app
    def close(self, event):
        sys.exit()
