import tkinter as tk
from PIL import Image, ImageTk
from photobooth.camera import Camera
from photobooth.pictures import Photostrip

class CameraPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize the camera
        self.size = controller.get_size()
        self.camera = Camera(self.size)

        # Initialize the photostrip
        self.photostrip = Photostrip()

        # Initialize the count down sequence
        self.countdown = CountDown(self)

        # Initialize the Photo Counter
        self.picCount = PictureCount(self)


class CountDown(tk.Label):
    def __init__(self, parent):
        tk.Label.__init__(self, parent)
        self.parent = parent

    def updateCounter(self):
        if self.count > 0:
            self.configure(text=self.count, font=("Droid", 200, "bold"))
            self.count -= 1
            self.after(1000, self.updateCounter)
        else:
            self.configure(text="STRIKE A POSE", font=("Droid", 75, "bold"))
            self.after(1000, self.showImage)
            

    def startCountDown(self):
        self.count = 5
        self.parent.camera.start()
        self.configure(text="GET READY!!!", bg="black", fg="white", font=("Droid", 75, "bold"), image="")
        self.grid(row=0, column=0, sticky="nsew")
        self.after(1250, self.updateCounter)

    def showImage(self):
        imgPath = self.parent.camera.finish()
        imgOpen = Image.open(imgPath).resize(self.parent.size, Image.ANTIALIAS)
        img = ImageTk.PhotoImage(imgOpen)
        self.parent.photostrip.photoPaths.append(imgPath)
        self.parent.photostrip.photosTK.append(img)
        self.configure(image=self.parent.photostrip.photosTK[-1], bg="white")
        self.after(2000, self.finishCountDown)

    def finishCountDown(self):
        self.grid_forget()
        self.parent.picCount.getNextImg()



class PictureCount(tk.Label):
    def __init__(self, parent):
        self.currentImg = 1
        self.totalImgs = 3
        tk.Label.__init__(self, parent, text=self.getImgNum(), font=("Droid", 75, "bold")) 
        self.parent = parent

        self.getNextImg()

    def getNextImg(self):
        if self.currentImg <= self.totalImgs:
            self.configure(text=self.getImgNum())
            self. currentImg += 1
            self.grid(row=0, column=0, sticky="nsew")
            self.after(1500, self.grid_forget)
            self.after(1500, self.parent.countdown.startCountDown)

    def getImgNum(self):
        return "Photo {} of {}".format(self.currentImg, self.totalImgs)
