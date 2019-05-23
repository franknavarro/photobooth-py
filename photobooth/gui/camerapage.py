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


class CountDown(tk.Label):
    def __init__(self, parent):
        tk.Label.__init__(self, parent, text="GET READY!!!", font=("Droid", 75, "bold"), bg="black", fg="white")
        self.grid(row=0, column=0, sticky="nsew")

        self.count = 3
        self.after(1000, self.updateCounter)

    def updateCounter(self):
        if self.count > 0:
            self.configure(text=self.count, font=("Droid", 200, "bold"))
            self.count -= 1
            self.after(1000, self.updateCounter)
        else:
            self.configure(text="STRIKE A POSE", font=("Droid", 75, "bold"))
            self.after(1000, self.destroy)



        
