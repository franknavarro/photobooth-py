import tkinter as tk
from photobooth.camera import Camera
from photobooth.pictures import Photostrip

class CameraPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        self.size = controller.get_size()
        print("Screen Size: {}w, {}h".format(self.size[0], self.size[1]))

        cameraResolution = (1280, 720)
        # Get the height of the camera window frame
        camY = 200 # Also defines the padding for the top/bottom
        camH = int(self.size[1] - camY*2)

        # Get the width of the camera window frame
        camW = int(camH * cameraResolution[0] / cameraResolution[1])
        camX = int((self.size[0] - camW) / 2) #Also defines the padding for the left/right
        cameraPosition = (camX, camY, camW, camH)
        self.cameraViewSize = (camW, camH)

        print("Camera Size: {}x, {}y, {}w, {}h".format(camX, camY, camW, camH))

        # Initialize the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1, minsize=camY)
        self.grid_rowconfigure(1, weight=1, minsize=camH)
        self.grid_rowconfigure(2, weight=1, minsize=camY)


        # Initialize the text above the camera
        self.topText = LabelText(self, "PHOTOBOOTH")
        self.topText.grid(row=0, column=0, sticky="nsew")

        # Initialize the frame behind the camera
        self.cameraFrame = CameraFrame(self, cameraPosition)
        self.cameraFrame.grid(row=1, column=0, sticky="nsew")


        # Initialize the text below the camera
        self.botText = LabelText(self, "PUSH BUTTON TO START")
        self.botText.grid(row=2, column=0, sticky="nsew")

        # Start the camera service
        self.camera = Camera(cameraPosition, cameraResolution)
        self.camera.start()

        # Initialize the photostrip
        self.photoNumber = 0
        self.maxPhotos = 3

        #Initialize the count down sequence
        self.maxCountDown = 5
        self.photostrip = Photostrip()

        # Initialize the count down sequence
        # self.countdown = CountDown(self)

        # Initialize the Photo Counter
        # self.picCount = PictureCount(self)
        self.focus_set()
        self.bind('<space>', self.startCaptures)
        
    # Start the process of taking photos
    def startCaptures(self, event):
        # Unbind the space bar event that triggers this function
        self.unbind('<space>')

        # Display the get ready text
        self.botText.updateText("Get ready!!!")
        # Start taking photos
        self.readyUpPictures()



    def readyUpPictures(self):
        # Hide the picuture behind the camera
        # I delay the hide so that the screen doesn't look like it 
        # flashes with everything changing all at once
        self.after(500, self.cameraFrame.hidePicture)

        if self.photoNumber < self.maxPhotos:
            # Update the count down number and photo number
            self.currentCountDown = self.maxCountDown
            self.photoNumber += 1

            # Start the camera only if this isn't the first photo
            # Because that would mean that the camera is already running
            if self.photoNumber != 0:
                self.camera.start()


            # Display which photo number this is 
            self.topText.updateText("Photo {} of {}".format(self.photoNumber, self.maxPhotos))

            # Start counting down 
            self.after(1000, self.updateCountDown)
        else:
            self.topText.hideText()
            self.botText.hideText()


    # Decrement the count down number by 1
    def updateCountDown(self):
        # Only decrement if less than 0
        if self.currentCountDown > 0:
            self.botText.updateText(self.currentCountDown)
            self.currentCountDown -= 1
            self.after(1000, self.updateCountDown)
        # If count down is at zero then take a photo
        else:
            self.botText.updateText("SNAP")
            self.after(500, self.takePhoto)


    # Process to take a photo and display it for the user to see
    def takePhoto(self):
        # Add text to the top of the screen to make the person feel good
        self.topText.updateText("Looking gooood")

        # Add text for the next photo if there is a next photo
        if self.photoNumber < self.maxPhotos:
            self.botText.updateText("Get ready for the next one!!!")
        else: 
            self.botText.hideText()

        # Take the picture
        imagePath = self.camera.takePic()
        # Stop the camera
        self.camera.stop()

        # Add the image to our photostrip
        self.photostrip.addPhoto(imagePath, self.cameraViewSize)

        # Display the photo on the screen
        self.cameraFrame.updatePicture(self.photostrip.photosTK[-1])

        # Take next photo
        self.after(2000, self.readyUpPictures)


# A class to format the bottom and top text of the application
class LabelText(tk.Frame):
    def __init__(self, parent, initText):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        # Size the contents of this Frame appropriately
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Add the text to this frame
        self.text = tk.Label(self, text=initText, font=("Droid", 65, "bold"), bg=self["bg"], fg="white")
        # Position this text in the frame
        self.text.grid(row=0, column=0, sticky="nsew")

    def updateText(self, newText):
        self.text.configure(text=newText)

    def hideText(self):
        self.text.configure(text="")


# A place holder for where the camera sits and where the cameras taken photos will be displayed
class CameraFrame(tk.Frame):
    def __init__(self, parent, cameraPosition):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        # Size the contents in the camera frame properly
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=cameraPosition[0])
        self.grid_columnconfigure(1, weight=1, minsize=cameraPosition[3])
        self.grid_columnconfigure(2, weight=1, minsize=cameraPosition[0])

        # Padding to the left of the camera
        self.cameraPad1 = tk.Frame(self, bg=self["bg"])
        self.cameraPad1.grid(row=0, column=0, sticky="nsew")

        # A Label where the camera will sit over and where pictures will be displayed
        self.picture = tk.Label(self, width=cameraPosition[2], height=cameraPosition[3], bg=self["bg"])
        self.picture.grid(row=0, column=1, sticky="nsew")

        # Padding to the right of the camera
        self.cameraPad2 = tk.Frame(self, bg=self["bg"])
        self.cameraPad2.grid(row=0, column=2, sticky="nsew")


    # Add a picture to the screen
    def updatePicture(self, img):
        self.picture.configure(image=img)

    # Remove the picture from the screen
    def hidePicture(self):
        self.picture.configure(image="")










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
