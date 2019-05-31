from PIL import Image, ImageTk
import time
import os

class Photostrip():
    def __init__(self):
        # Save photos being used
        self.photoPaths = []
        self.photosTK = []
        self.photos = []

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
        self.stripFolder = os.path.join(self.photoboothFolder, "strips")
        if not os.path.isdir(self.stripFolder):
            os.makedirs(self.stripFolder)

        print("Image Folder: ",self.imageFolder)
        print("Image Folder: ",self.stripFolder)

        # Set the dpi at which we will print at
        self.dpi = 300

        # Set wether the photo strip will have a logo
        self.hasLogo = False

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

        self.stripTK = ImageTk.PhotoImage(self.stripPrint.resize((newWidth, newHeight), Image.ANTIALIAS))
        self.grayscaleStripTK = ImageTk.PhotoImage(self.grayscaleStripPrint.resize((newWidth, newHeight), Image.ANTIALIAS))
        self.bothTK = ImageTk.PhotoImage(self.bothPrint.resize((newWidth, newHeight), Image.ANTIALIAS))


        

class StripEqualLogo(Photostrip):
    def __init__(self):
        Photostrip.__init__(self)
        self.hasLogo = True

        # Define how many photos are used in this image
        self.photoCount = 3

        # Define the measurements in inches
        self.stripSizeInches = (2, 6)
        self.stripBorderInches = 1 / 16

        # Define the print image size
        self.printSizeInches = (4, 6)
        printSizeWidth = self.dpi * self.printSizeInches[0]
        printSizeHeight = self.dpi * self.printSizeInches[1]
        self.printSize = (int(printSizeWidth), int(printSizeHeight))

        # Define the measurements in pixels
        stripWidth = self.dpi * self.stripSizeInches[0]
        stripHeight = self.dpi * self.stripSizeInches[1]
        self.stripSize = (int(stripWidth), int(stripHeight))

        # Add up how many images are showing up in the strip (including the logo)
        imageports = self.photoCount
        if self.hasLogo:
            imageports += 1

        # Get the amount of space the borders are taking
        self.stripBorders = int(self.dpi * self.stripBorderInches)
        bordersTotalVertical = ( imageports + 1 ) * self.stripBorders
        bordersTotalHorizontal = self.stripBorders * 2

        # Get the size of each image used in the photostrip
        imageWidth = int(stripWidth - bordersTotalHorizontal)
        imageHeight = int((stripHeight - bordersTotalVertical) / imageports)
        self.imageSize = (imageWidth, imageHeight)

        print("Image Size: {}w, {}h".format(imageWidth, imageHeight))
        print("Strip Size: {}w, {}h".format(stripWidth, stripHeight))

    def generateStrip(self):
        print("Generating Photostrip")
        strip = Image.new("RGB", self.stripSize, "white")
        positionX = self.stripBorders
        positionY = self.stripBorders # Will increment this to go down
        for image in self.photos:
            strip.paste(image, (positionX, positionY))
            positionY += self.imageSize[1] + self.stripBorders

        stripTimeStamp = time.strftime("%Y-%m-%d_%H.%M.%S")
        stripFilename = "".join(("colored_",stripTimeStamp,".jpg"))
        stripFilePath = os.path.join(self.stripFolder, stripFilename)
        strip.save(stripFilePath)

        self.strip = strip
        self.grayscaleStrip = strip.convert('LA')

        self.stripPrint = Image.new("RGB", self.printSize, "white")
        self.stripPrint.paste(self.strip, (0, 0))
        self.stripPrint.paste(self.strip, (self.stripSize[0], 0))
        self.stripTK = ImageTk.PhotoImage(self.stripPrint)

        self.grayscaleStripPrint = self.stripPrint.convert('LA')
        self.grayscaleStripTK = ImageTk.PhotoImage(self.grayscaleStripPrint)

        self.bothPrint = Image.new("RGB", self.printSize, "white")
        self.bothPrint.paste(self.strip, (0, 0))
        self.bothPrint.paste(self.grayscaleStrip, (self.stripSize[0], 0))
        self.bothTK = ImageTk.PhotoImage(self.bothPrint)


