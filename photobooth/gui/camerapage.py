import tkinter as tk
from PIL import Image, ImageTk
from photobooth.camera import Camera

class CameraPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.counterLabel = tk.Label(self, text="", font=("Droid", 100, "bold"))
        self.counterLabel.grid(row=0, column=0, sticky="nsew")

        self.size = controller.get_size()

        self.camera = Camera(self.size)
        self.camera.start()

        count = CountDown(self)


class CountDown(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self, parent, height=parent.size[0], width=parent.size[1])
        self.grid(row=0, column=0, sticky="nsew")

        # Create the transparent black box over the camera image
        self.backImage = Image.new('RGBA', parent.size, (0, 0, 0, 255//2))
        self.background = ImageTk.PhotoImage(self.backImage)
        self.create_image(0, 0, image=self.background, anchor="nw")


        
