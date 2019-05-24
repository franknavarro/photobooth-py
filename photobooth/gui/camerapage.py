import tkinter as tk
from photobooth.camera import Camera
from photobooth.pictures import Photostrip

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

        self.photostrip = Photostrip()


        count = CountDown(self, self.camera, self.photostrip)


class CountDown(tk.Label):
    def __init__(self, parent, camera, photostrip):
        tk.Label.__init__(self, parent, text="GET READY!!!", font=("Droid", 75, "bold"), bg="black", fg="white")
        self.camera = camera
        self.photostrip = photostrip
        self.startCountDown()


    def updateCounter(self):
        if self.count > 0:
            self.configure(text=self.count, font=("Droid", 200, "bold"))
            self.count -= 1
            self.after(1000, self.updateCounter)
        else:
            self.configure(text="STRIKE A POSE", font=("Droid", 75, "bold"))
            self.after(1000, self.grid_forget)
            self.after(1250, self.finishCountDown)
            

    def startCountDown(self):
        self.count = 3
        self.grid(row=0, column=0, sticky="nsew")
        self.after(1000, self.updateCounter)

    def finishCountDown(self):
        self.photostrip.photos.append(self.camera.finish())
        print(self.photostrip.photos)

