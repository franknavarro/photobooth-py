import tkinter as tk

from photobooth.camera import Camera
from .countdownbar import CountDownBar
from .printselector import PrintSelector

# A place holder for where the camera sits and where the cameras taken photos will be displayed
class CameraPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        self.controller = controller

        # Count down bar size
        countBarHeight = 10

        # Inherit sizing from controller
        self.cameraResolution = controller.photostrip.imageSize
        self.size = controller.containerSize

        # Get the height of the camera window frame
        camY = controller.textHeight # Also defines the padding for the top/bottom
        camH = self.size[1] - countBarHeight

        # Get the width of the camera window frame
        camW = int(camH * self.cameraResolution[0] / self.cameraResolution[1])
        camX = int((self.size[0] - camW) / 2) #Also defines the padding for the left/right

        # Coordinates for camera on the screen
        cameraPadding = 10
        self.cameraContainer = (camX, camY, camW, camH) # [X, Y, Width, Height]
        self.cameraCoordinates = (camX + cameraPadding, camY + cameraPadding, camW - cameraPadding*2, camH - cameraPadding*2)
        print("Camera Size: {}x, {}y, {}w, {}h".format(self.cameraCoordinates[0], self.cameraCoordinates[1], self.cameraCoordinates[2], self.cameraCoordinates[3]))

        # Get the relative camera position values from the parent
        self.cameraViewSize = (self.cameraCoordinates[2], self.cameraCoordinates[3])
        print("CameraViewSize: {}w, {}h".format(self.cameraViewSize[0], self.cameraViewSize[1]))

        # Start the camera service
        self.camera = Camera(self.cameraCoordinates, self.cameraResolution)

        # Get our photostrip instance
        self.photostrip = controller.photostrip
        self.maxPhotos = self.photostrip.photoCount


        #Initialize the count down sequence
        self.maxCountDown = 5

        # Keep references here of the the top and bottom text of the parent for future use
        self.topText = controller.topText
        self.botText = controller.botText

        # Size the contents in the camera frame properly
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=self.cameraContainer[0])
        self.grid_columnconfigure(1, weight=1, minsize=self.cameraContainer[3])
        self.grid_columnconfigure(2, weight=1, minsize=self.cameraContainer[0])

        # Padding to the left of the camera
        self.cameraPad1 = tk.Frame(self, bg=self["bg"])
        self.cameraPad1.grid(row=0, column=0, sticky="nsew")

        # A Frame where the camera will sit over and where pictures will be displayed
        offWhiteColor = "#F8F8FF"
        self.pictureFrame = tk.Frame(self, width=self.cameraContainer[2], bg=self["bg"])
        self.pictureFrame.grid(row=0, column=1, sticky="nsew")
        self.pictureFrame.grid_rowconfigure(0, weight=1)
        self.pictureFrame.grid_columnconfigure(0, weight=1)

        self.picture = tk.Label(self.pictureFrame, width=self.cameraContainer[2], height=self.cameraContainer[3], bg=offWhiteColor)
        self.picture.grid(row=0, column=0, sticky="nsew")

        self.countDownBar = CountDownBar(self.pictureFrame, maxTime=self.maxCountDown-1, height=countBarHeight)
        self.countDownBar.grid(row=1, column=0, sticky="nsew")


        # Padding to the right of the camera
        self.cameraPad2 = tk.Frame(self, bg=self["bg"])
        self.cameraPad2.grid(row=0, column=2, sticky="nsew")


    def initializePage(self):
        self.photoNumber = 0
        self.topText.updateText("PHOTOBOOTH")
        self.botText.updateText("PUSH BUTTON TO START")
        # Bind space bar to start capturing pictures
        self.bindID = self.bind('<space>', self.startCaptures)
        # Start the camera service
        self.camera.start()


    # Add a picture to the screen
    def updatePicture(self, img):
        self.picture.configure(image=img)
        print("Displayed IMG Size: {}w, {}h".format(img.width(), img.height()))

    # Remove the picture from the screen
    def hidePicture(self):
        self.picture.configure(image="")


    # Start the process of taking photos
    def startCaptures(self, event):
        # Unbind the space bar event that triggers this function
        self.unbind('<space>', self.bindID)

        # Display the get ready text
        self.botText.updateText("Get ready!!!")
        # Start taking photos
        self.readyUpPictures()


    def readyUpPictures(self):
        # Hide the picuture behind the camera
        # I delay the hide so that the screen doesn't look like it 
        # flashes with everything changing all at once
        self.after(250, self.hidePicture)

        if self.photoNumber < self.maxPhotos:
            # Update the count down number and photo number
            self.currentCountDown = self.maxCountDown
            self.photoNumber += 1

            # Start the camera only if this isn't the first photo
            # Because that would mean that the camera is already running
            if self.photoNumber != 1:
                self.camera.start()


            # Display which photo number this is 
            self.topText.updateText("Photo {} of {}".format(self.photoNumber, self.maxPhotos))

            # Start counting down 
            self.after(1000, self.updateCountDown)
        else:
            self.controller.show_frame(PrintSelector)


    # Decrement the count down number by 1
    def updateCountDown(self):
        if self.currentCountDown == self.maxCountDown:
            self.countDownBar.start()
        # Only decrement if less than 0
        if self.currentCountDown > 0:
            self.botText.updateText(self.currentCountDown)
            self.currentCountDown -= 1
            self.after(1000, self.updateCountDown)
        # If count down is at zero then take a photo
        else:
            self.takePhoto()


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
        imagePath = self.camera.takePic(self.photostrip.imageFolder)
        # Stop the camera
        self.camera.stop()

        # Add the image to our photostrip
        self.photostrip.addPhoto(imagePath, self.cameraViewSize)

        # Display the photo on the screen
        self.updatePicture(self.photostrip.photosTK[-1])

        # Take next photo
        self.after(2000, self.readyUpPictures)


