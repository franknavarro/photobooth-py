from PIL import Image, ImageTk
import time
import os

class Photostrip():
    def __init__(self):
        # Save photos being used
        self.photoPaths = []
        self.photosTK = []

        # Set the folder for the user where we will store all our content
        folderPathList = ("Pictures", "Photobooth")
        # Get the users home directory
        self.photoboothFolder = os.path.expanduser("~")
        # Run through and make sure each folder exists
        for folder in folderPathList:
            self.photoboothFolder = os.path.join(self.photoboothFolder, folder)
            # If the folder doesn't exist create it
            if not os.path.isdir(self.photoboothFolder):
                os.makedirs(self.photoboothFolder)

        # Create the folder where the images are stored
        self.imageFolder = os.path.join(self.photoboothFolder, "singles")
        if not os.path.isdir(self.imageFolder):
            os.makedirs(self.imageFolder)

        # Create the folder where the photostrips are stored
        self.stripFolder = os.path.join(self.photoboothFolder, "singles")
        if not os.path.isdir(self.stripFolder):
            os.makedirs(self.stripFolder)

        print("Image Folder: ",self.imageFolder)
        print("Image Folder: ",self.stripFolder)

        # Set the dpi at which we will print at
        self.dpi = 300

        # Set wether the photo strip will have a logo
        self.hasLogo = False

    def addPhoto(self, photoPath, viewSize):
        # Open the image as a tkinter image
        imgOpen = Image.open(photoPath).resize(viewSize, Image.ANTIALIAS)
        imgTK = ImageTk.PhotoImage(imgOpen)
        # Save the photos in this class
        self.photoPaths.append(photoPath)
        self.photosTK.append(imgTK)
        

class StripEqualLogo(Photostrip):
    def __init__(self):
        Photostrip.__init__(self)
        self.hasLogo = True

        # Define how many photos are used in this image
        self.photoCount = 3

        # Define the measurements in inches
        self.stripSizeInches = (2, 6)
        self.stripBorderInches = 1 / 8

        # Define the measurements in pixels
        stripWidth = self.dpi * self.stripSizeInches[0]
        stripHeight = self.dpi * self.stripSizeInches[1]
        self.stripSize = (stripWidth, stripHeight)

        # Add up how many images are showing up in the strip (including the logo)
        imageports = self.photoCount
        if self.hasLogo:
            imageports += 1

        # Get the amount of space the borders are taking
        self.stripBorders = self.dpi * self.stripBorderInches
        bordersTotalVertical = ( imageports + 1 ) * self.stripBorders
        bordersTotalHorizontal = self.stripBorders * 2

        # Get the size of each image used in the photostrip
        imageWidth = int(stripWidth - bordersTotalHorizontal)
        imageHeight = int((stripHeight - bordersTotalVertical) / imageports)
        self.imageSize = (imageWidth, imageHeight)

        print("Image Size: {}w, {}h".format(imageWidth, imageHeight))
        print("Strip Size: {}w, {}h".format(stripWidth, stripHeight))
