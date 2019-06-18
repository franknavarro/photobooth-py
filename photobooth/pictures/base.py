from PIL import Image, ImageTk
import os

from photobooth.settings import config

# This is the base class for the photostrip
class Photostrip():
    def __init__(self):
        # Initialize the correct dimensions
        self.reset()

        # Get the users home directory
        self.photoboothFolder = config.get('Photostrip', 'folderPath')
        # If the folder doesn't exist create it
        if not os.path.isdir(self.photoboothFolder):
            os.makedirs(self.photoboothFolder)

        # Create the folder where the images are stored
        self.imageFolder = os.path.join(self.photoboothFolder, "singles")
        if not os.path.isdir(self.imageFolder):
            os.makedirs(self.imageFolder)

        # Create the folder where the photostrips are stored
        self.stripFolder = os.path.join(self.photoboothFolder, "strips")
        if not os.path.isdir(self.stripFolder):
            os.makedirs(self.stripFolder)

        # Create the folder where the prints are stored
        self.printFolder = os.path.join(self.photoboothFolder, "print")
        if not os.path.isdir(self.printFolder):
            os.makedirs(self.printFolder)

        print("Image Folder: ",self.imageFolder)
        print("Strip Folder: ",self.stripFolder)
        print("Print Folder: ",self.printFolder)

        # Set the dpi at which we will print at
        self.dpi = 300


    def reset(self):
        # Save photos being used
        self.photoPaths = []
        self.photosTK = []
        self.photos = []

        self.printPaths = {
            "color": "",
            "grayscale": "",
            "both": ""
        }
        
        self.printImages = {
            "color":"",
            "grayscale":"",
            "both":""
        }

        self.printsTK = {
            "color":"",
            "grayscale":"",
            "both":""
        }


    def addPhoto(self, photoPath, cameraViewSize):
        # Save the path for the photo
        self.photoPaths.append(photoPath)

        # Save the image for stitching later
        imgOpen = Image.open(photoPath)
        self.photos.append(imgOpen)

        # Save the image as a tk image object to display on screen
        imgResized = imgOpen.resize(cameraViewSize, Image.ANTIALIAS)
        imgTK = ImageTk.PhotoImage(imgResized)
        self.photosTK.append(imgTK)

    # Resizes the TK images of the photostrip depedning on the size specified
    def resizeScreenIMGs(self, **kwargs ):
        # If width is specified then update to relative height
        if 'width' in kwargs:
            newWidth = kwargs.get('width')
            newHeight = int(newWidth * self.printSize[1] / self.printSize[0])
        # If height is specified then update to relative width
        elif 'height' in kwargs:
            newHeight = kwargs.get('height')
            newWidth = int(newHeight * self.printSize[0] / self.printSize[1])
        # If no height nor width was given then update to default size
        else:
            newWidth = self.printSize[0]
            newHeight = self.printSize[1]


        stripTK = ImageTk.PhotoImage(self.printImages['color'].resize((newWidth, newHeight), Image.ANTIALIAS))
        grayscaleStripTK = ImageTk.PhotoImage(self.printImages['grayscale'].resize((newWidth, newHeight), Image.ANTIALIAS))
        bothTK = ImageTk.PhotoImage(self.printImages['both'].resize((newWidth, newHeight), Image.ANTIALIAS))

        self.printsTK.update({"color":stripTK, "grayscale":grayscaleStripTK, "both":bothTK})


    def getPrintFile(self, key):
        return self.printPaths[key]
    def getPrintTK(self, key):
        return self.printsTK[key]

    def deleteUnSelected(self, selected):
        if selected == 'color':
            remove = ['grayscale', 'both']
        elif selected == 'grayscale':
            remove = ['color', 'both']
        elif selected == 'both':
            remove = ['color', 'grayscale']

        for picType in remove:
            os.remove(self.printPaths[picType])
            self.printPaths[picType] = ""
