import tkinter as tk
from photobooth.camera import Camera
from photobooth.pictures import StripEqualLogo

class CameraPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        # Initialize the photostrip
        self.photostrip = StripEqualLogo()

        # Calculate sizes for our various frames
        self.size = controller.get_size()

        self.textWidth = self.size[0]
        self.textHeight = 200
        self.textSize = (self.textWidth, self.textHeight)

        self.containerWidth = self.size[0]
        self.containerHeight = int(self.size[1] - self.textHeight*2)
        self.containerSize = (self.containerWidth, self.containerHeight)

        print("Screen Size: {}w, {}h".format(self.size[0], self.size[1]))


        # Initialize the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1, minsize=self.textHeight)
        self.grid_rowconfigure(1, weight=1, minsize=self.containerHeight)
        self.grid_rowconfigure(2, weight=1, minsize=self.textHeight)


        # Initialize the text above the camera
        self.topText = LabelText(self, "PHOTOBOOTH")
        self.topText.grid(row=0, column=0, sticky="nsew")

        # Initialize the text below the camera
        self.botText = LabelText(self, "PUSH BUTTON TO START")
        self.botText.grid(row=2, column=0, sticky="nsew")

        # Create container to hold both the Camera Page and the Printing Page
        self.container = tk.Frame(self, bg=self["bg"])
        self.container.grid(row=1, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Initialize the Camera Frame
        self.frames = {}
        self.load_frame(CameraFrame)
        self.show_frame(CameraFrame)


    # Function to display a loaded frames in the app
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.focus_set()
        frame.tkraise()

    # Loads in the container from a class and then displays it
    def load_frame(self, cont):
        frame = cont(self.container, self)
        self.frames[cont] = frame
        frame.grid(row=0, column=0, stick="nsew")



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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        self.controller = controller

        # Inherit sizing from controller
        self.cameraResolution = controller.photostrip.imageSize
        self.size = controller.containerSize

        # Get the height of the camera window frame
        camY = controller.textHeight # Also defines the padding for the top/bottom
        camH = self.size[1]

        # Get the width of the camera window frame
        camW = int(camH * self.cameraResolution[0] / self.cameraResolution[1])
        camX = int((self.size[0] - camW) / 2) #Also defines the padding for the left/right

        # Coordinates for camera on the screen
        self.cameraPosition = (camX, camY, camW, camH) # [X, Y, Width, Height]
        print("Camera Size: {}x, {}y, {}w, {}h".format(camX, camY, camW, camH))

        # Get the relative camera position values from the parent
        self.cameraViewSize = (camW, camH)

        # Start the camera service
        self.camera = Camera(self.cameraPosition, self.cameraResolution)
        self.camera.start()

        # Get our photostrip instance
        self.photostrip = controller.photostrip
        self.photoNumber = 0
        self.maxPhotos = self.photostrip.photoCount


        #Initialize the count down sequence
        self.maxCountDown = 1

        # Keep references here of the the top and bottom text of the parent for future use
        self.topText = controller.topText
        self.botText = controller.botText

        # Size the contents in the camera frame properly
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=self.cameraPosition[0])
        self.grid_columnconfigure(1, weight=1, minsize=self.cameraPosition[3])
        self.grid_columnconfigure(2, weight=1, minsize=self.cameraPosition[0])

        # Padding to the left of the camera
        self.cameraPad1 = tk.Frame(self, bg=self["bg"])
        self.cameraPad1.grid(row=0, column=0, sticky="nsew")

        # A Label where the camera will sit over and where pictures will be displayed
        self.picture = tk.Label(self, width=self.cameraPosition[2], height=self.cameraPosition[3], bg=self["bg"])
        self.picture.grid(row=0, column=1, sticky="nsew")

        # Padding to the right of the camera
        self.cameraPad2 = tk.Frame(self, bg=self["bg"])
        self.cameraPad2.grid(row=0, column=2, sticky="nsew")

        # Bind space bar to start capturing pictures
        self.bind('<space>', self.startCaptures)


    # Add a picture to the screen
    def updatePicture(self, img):
        self.picture.configure(image=img)

    # Remove the picture from the screen
    def hidePicture(self):
        self.picture.configure(image="")


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
        self.after(500, self.hidePicture)

        if self.photoNumber < self.maxPhotos:
            # Update the count down number and photo number
            self.currentCountDown = self.maxCountDown
            self.photoNumber += 1

            # Start the camera only if this isn't the first photo
            # Because that would mean that the camera is already running
            if self.photoNumber != 1:
                self.camera.start()
                print("Restart Camera")


            # Display which photo number this is 
            self.topText.updateText("Photo {} of {}".format(self.photoNumber, self.maxPhotos))

            # Start counting down 
            self.after(1000, self.updateCountDown)
        else:
            self.topText.hideText()
            self.botText.hideText()
            self.controller.load_frame(PrintingPage)
            self.controller.show_frame(PrintingPage)


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
        imagePath = self.camera.takePic(self.photostrip.imageFolder)
        # Stop the camera
        self.camera.stop()

        # Add the image to our photostrip
        self.photostrip.addPhoto(imagePath, self.cameraViewSize)

        # Display the photo on the screen
        self.updatePicture(self.photostrip.photosTK[-1])

        # Take next photo
        self.after(2000, self.readyUpPictures)


class PrintingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        # Get the relative window size
        self.size = controller.containerSize

        # Get the container sizes
        self.padding = 50
        textHeight = 100
        countHeight = 25
        stripContainerHeight = self.size[1] - self.padding * 2 - textHeight - countHeight
        columnWidths = int( self.size[0] / 3 )


        # Set up the grid sizing
        self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=columnWidths)
        self.grid_columnconfigure(1, weight=1, minsize=columnWidths)
        self.grid_columnconfigure(2, weight=1, minsize=columnWidths)

        # Keep references here of the the top and bottom text of the parent for future use
        self.topText = controller.topText
        self.botText = controller.botText

        # Update the text
        self.topText.updateText("Select print color")
        self.botText.updateText("Push button to change")

        # Get the photostrip instance
        self.photostrip = controller.photostrip
        self.photostrip.generateStrip()

        self.photostrip.resizeScreenIMGs( height=stripContainerHeight )

        # Size the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.middleColumn = columnWidths / 2

        # The Colored Photostrip to display
        self.coloredImage = ImageSelector(self, self.photostrip, option='color', selected=True)
        self.coloredImage.grid(row=0, column=0, sticky="nsew") 

        # The Grayscale Image
        self.grayscaleImage = ImageSelector(self, self.photostrip, option='grayscale')
        self.grayscaleImage.grid(row=0, column=1, sticky="nsew") 

        # The Both Grayscale and Colored Image
        self.bothImage = ImageSelector(self, self.photostrip, option='both')
        self.bothImage.grid(row=0, column=2, sticky="nsew") 

        # Create a count down bar
        self.countDown = CountDownBar(self, maxTime=10, height=countHeight)
        self.countDown.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.countDown.start()

        # Bind space bar to toggle the next option
        self.bind('<space>', self.toggleNext)

    # Depending on the currently selected select the next one
    def toggleNext(self, event):
        if self.coloredImage.selected:
            self.coloredImage.toggleSelected()
            self.grayscaleImage.toggleSelected()

        elif self.grayscaleImage.selected:
            self.grayscaleImage.toggleSelected()
            self.bothImage.toggleSelected()

        elif self.bothImage.selected:
            self.bothImage.toggleSelected()
            self.coloredImage.toggleSelected()



class ImageSelector(tk.Frame):
    def __init__ (self, parent, photostrip, **kwargs):
        tk.Frame.__init__(self, parent, bg=parent["bg"])

        if 'selected' in kwargs:
            self.selected = kwargs.get('selected')
        else:
            self.selected = False

        # Get the option passed in if there was one
        if 'option' in kwargs:
            option = kwargs.get('option')
        else:
            option = 'color'

        # Get preset depending on the option
        if option == "grayscale":
            text = "Black & White"
            pic = photostrip.grayscaleStripTK
        elif option == "both":
            text = "Both"
            pic = photostrip.bothTK
        else:
            text = "Color"
            pic = photostrip.stripTK

        # Size the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create the image
        self.image = tk.Label(self, image=pic, bg=self["bg"])
        self.image.grid(row=0, column=0, sticky="nsew") 

        # Create the text
        self.text = tk.Label(self, text=text, bg=self["bg"], font=("Droid", 45, "bold"), fg="white")
        self.text.grid(row=1, column=0, sticky="nsew")

        self.highlightColor = "#AFF2F1"
        if self.selected:
            self.text.configure( bg=self.highlightColor )

    def toggleSelected(self):
        self.selected = not self.selected

        # Change background color
        if self.selected:
            self.text.configure(bg=self.highlightColor)
        else:
            self.text.configure(bg=self["bg"])

        # Update the screen 
        self.update()

class CountDownBar(tk.Canvas):
    def __init__ (self, parent, **kwargs):
        self.color = "#AFF2F1" # bar color
        self.backColor = parent["bg"] # Save for later
        # Start as background as the bar color so that the bar looks filled to start
        tk.Canvas.__init__(self, parent, bg=self.backColor, bd=0, highlightthickness=0, relief='flat')

        # Check if the height is defined
        if 'height' in kwargs:
            self.height = kwargs.get('height')
        else:
            self.height = 10

        self.configure(height=self.height)

        # Check if the max time is defined
        if 'maxTime' in kwargs:
            self.maxSeconds = kwargs.get('maxTime')
        else:
            self.maxSeconds = 5

        self.time = int(self.maxSeconds * 1000)
        self.updateTime = 5


    def start(self):
        self.update()
        self.width = self.winfo_width()
        self.bar = self.create_rectangle(0, 0, self.width, self.height, fill=self.color, outline="")
        self.configure(bg=self.backColor)
        self.updateSize = self.updateTime * self.width / self.time
        self.after(self.updateTime, self.updateBar)
    
    def updateBar(self):
        if self.time >= 0:
            self.width -= self.updateSize
            self.time -= self.updateTime
            self.coords(self.bar, (0, 0, self.width, self.height))
            self.update()
            self.after(self.updateTime, self.updateBar)
        else:
            self.time = self.maxTime
            self.width = self.maxWidth
