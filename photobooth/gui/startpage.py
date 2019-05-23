import tkinter as tk
from .camerapage import CameraPage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Set page background to white
        self.configure(background='white')
	# Center page 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

	# Add name of application to center
        appname = tk.Label(self, text="Photobooth", font=("Droid",50,'bold italic'))
        appname.grid(row=0, column=0, sticky="nsew")

        # Add push button text to bottom
        instruct = tk.Label(self, text="Push button to start", font=("Droid", 25, 'bold'))
        instruct.grid(row=1, column=0, sticky='sew')

        # Bind Space bar to go to camera event
        self.bind('<space>', self.startcam)


    # Begin the camera page
    def startcam(self, event):
        print("Navigating to Camera...")
        self.controller.load_frame(CameraPage)

