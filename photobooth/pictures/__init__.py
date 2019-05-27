from PIL import Image, ImageTk

class Photostrip():
    def __init__(self):
        self.photoPaths = []
        self.photosTK = []

    def addPhoto(self, photoPath, viewSize):
        # Open the image as a tkinter image
        imgOpen = Image.open(photoPath).resize(viewSize, Image.ANTIALIAS)
        imgTK = ImageTk.PhotoImage(imgOpen)
        # Save the photos in this class
        self.photoPaths.append(photoPath)
        self.photosTK.append(imgTK)
