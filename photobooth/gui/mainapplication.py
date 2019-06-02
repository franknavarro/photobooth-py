import tkinter as tk

from photobooth.pictures import StripEqualLogo

from .camerapage import CameraPage
from .labeltext import LabelText

class MainApplication(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        # Initialize the photostrip
        self.photostrip = StripEqualLogo()
        self.printImage = ""

        # Calculate sizes for our various frames
        self.size = controller.get_size()

        self.textWidth = self.size[0]
        self.textHeight = 200
        self.textSize = (self.textWidth, self.textHeight)

        self.containerWidth = self.size[0]
        self.containerHeight = int(self.size[1] - self.textHeight*2)
        self.containerSize = (self.containerWidth, self.containerHeight)

        print("Screen Size: {}w, {}h".format(self.size[0], self.size[1]))


        # Initialize the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1, minsize=self.textHeight)
        self.grid_rowconfigure(1, weight=1, minsize=self.containerHeight)
        self.grid_rowconfigure(2, weight=1, minsize=self.textHeight)


        # Initialize the text above the camera
        self.topText = LabelText(self, "PHOTOBOOTH")
        self.topText.grid(row=0, column=0, sticky="nsew")

        # Initialize the text below the camera
        self.botText = LabelText(self, "PUSH BUTTON TO START")
        self.botText.grid(row=2, column=0, sticky="nsew")

        # Create container to hold both the Camera Page and the Printing Page
        self.container = tk.Frame(self, bg=self["bg"])
        self.container.grid(row=1, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Initialize the Camera Frame
        self.frames = {}
        self.load_frame(CameraPage)
        self.show_frame(CameraPage)


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


    def resetCameraPage(self):
        self.topText.updateText("PHOTOBOOTH")
        self.botText.updateText("PUSH BUTTON TO START")
        self.load_showFrame(CameraPage)
