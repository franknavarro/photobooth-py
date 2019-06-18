from PIL import Image, ImageTk
import time
import os

from photobooth.settings import config
from .base import Photostrip

class StripVertical(Photostrip):
    def __init__(self):
        Photostrip.__init__(self)

        self.calculateDimensions()


    def calculateDimensions(self):
        # Set wether the photo strip will have a logo
        self.hasLogo = config.getboolean('StripVertical', 'hasLogo')
        # Define how many photos are used in this image
        self.photoCount = config.getint('StripVertical', 'photoCount')

        # Define the print image size
        self.printSizeInches = config.getlist('StripVertical', 'paperSize')
        printSizeWidth = self.dpi * self.printSizeInches[0]
        printSizeHeight = self.dpi * self.printSizeInches[1]
        self.printSize = (int(printSizeWidth), int(printSizeHeight))

        # Define the measurements in inches
        self.stripSizeInches = ( self.printSizeInches[0]/2, self.printSizeInches[1] )
        self.stripBorderInches = config.getfloat('StripVertical', 'border')

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

        grayscaleStrip = strip.convert('L')

        # Create the colored strip using pillow
        stripPrint = Image.new("RGB", self.printSize, "white")
        stripPrint.paste(strip, (0, 0))
        stripPrint.paste(strip, (self.stripSize[0], 0))
        # Create the TK compatible image
        stripTK = ImageTk.PhotoImage(stripPrint)
        # Get the file name for the printable image and save it
        colorFileName = "".join(("colored_",stripTimeStamp,".jpg"))
        colorFilePath = os.path.join(self.printFolder, colorFileName)
        stripPrint.save(colorFilePath)

        # Create the grayscale strip using pillow
        grayscaleStripPrint = stripPrint.convert('L')
        # Create the TK compatible image
        grayscaleStripTK = ImageTk.PhotoImage(grayscaleStripPrint)
        # Get the file name for the printable image and save it
        grayFileName = "".join(("grayscale_",stripTimeStamp,".jpg"))
        grayFilePath = os.path.join(self.printFolder, grayFileName)
        grayscaleStripPrint.save(grayFilePath)

        # Create the grayscale strip using pillow
        bothPrint = Image.new("RGB", self.printSize, "white")
        bothPrint.paste(strip, (0, 0))
        bothPrint.paste(grayscaleStrip, (self.stripSize[0], 0))
        # Create the TK compatible image
        bothTK = ImageTk.PhotoImage(bothPrint)
        # Get the file name for the printable image and save it
        bothFileName = "".join(("both_",stripTimeStamp,".jpg"))
        bothFilePath = os.path.join(self.printFolder, bothFileName)
        bothPrint.save(bothFilePath)

        self.printPaths.update({"color":colorFilePath, "grayscale":grayFilePath, "both":bothFilePath})
        self.printImages.update({"color":stripPrint, "grayscale":grayscaleStripPrint, "both":bothPrint})
        self.printsTK.update({"color":stripTK, "grayscale":grayscaleStripTK, "both":bothTK})


