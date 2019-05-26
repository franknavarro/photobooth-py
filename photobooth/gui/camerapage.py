import tkinter as tk
from PIL import Image, ImageTk
from photobooth.camera import Camera
from photobooth.pictures import Photostrip

class CameraPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.size = controller.get_size()
        cameraResolution = (720, 720)
        # Get the height of the camera window frame
        camY = 200 # Also defines the padding for the top/bottom
        camH = int(self.size[1] - camY*2)

        # Get the width of the camera window frame
        camW = int(camH * cameraResolution[0] / cameraResolution[1])
        camX = int((self.size[0] - camW) / 2) #Also defines the padding for the left/right
        cameraSize = (camX, camY, camW, camH)

        print("Camera Size: {}x, {}y, {}w, {}h".format(camX, camY, camW, camH))

        # Initialize the grid
        self.grid_columnconfigure(0, weight=1, minsize=camX)
        self.grid_columnconfigure(2, weight=1, minsize=camX)
        self.grid_rowconfigure(0, weight=1, minsize=camY)
        self.grid_rowconfigure(2, weight=1, minsize=camY)

        self.textFrame = tk.Frame(self, bg="blue")
        self.textFrame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.textFrame.grid_columnconfigure(0, weight=1)
        self.textFrame.grid_rowconfigure(0, weight=1)
        self.readyText = tk.Label(self.textFrame, text="Get Ready!!!", font=("Droid", 65, "bold"), bg=self.textFrame["bg"])
        self.readyText.grid(row=0, column=0, sticky="nsew")

        self.cameraPad1 = tk.Frame(self, bg="yellow")
        self.cameraPad1.grid(row=1, column=0, sticky="nsew")

        self.cameraFrame = tk.Frame(self, width=camW, height=camH, bg="black")
        self.cameraFrame.grid(row=1, column=1, sticky="nsew")
        self.cameraFrame.update_idletasks()
        print("Camera Frame: {}w, {}h".format(self.cameraFrame.winfo_width(), self.cameraFrame.winfo_height()))

        self.cameraPad2 = tk.Frame(self, bg="green")
        self.cameraPad2.grid(row=1, column=2, sticky="nsew")

        self.textFrame2 = tk.Frame(self, bg="red")
        self.textFrame2.grid(row=2, column=0, columnspan=3, sticky="nsew")

        self.camera = Camera(cameraSize, cameraResolution)
        self.camera.start()

        # Initialize the photostrip
        # self.photostrip = Photostrip()

        # Initialize the count down sequence
        # self.countdown = CountDown(self)

        # Initialize the Photo Counter
        # self.picCount = PictureCount(self)


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
