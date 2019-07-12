import tkinter as tk
import math
from photobooth.settings import config

class CountDownBar(tk.Canvas):
    def __init__ (self, parent, color=config.get('Apperance', 'secondaryColor'), **kwargs):
        self.color = color  # bar color
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

        # Access a label that will update will display the seconds counted down
        if 'secondsLabel' in kwargs:
            self.secondsLabel = kwargs.get('secondsLabel')
        else:
            self.secondsLabel = None

        # Check if a call back function is defined
        if 'callback' in kwargs:
            self.callback = kwargs.get('callback')
        else:
            self.callback = None


        # Create the bar we will be updating
        self.bar = self.create_rectangle(0, 0, 0, 0, fill=self.color, outline="")


    def start(self):
        # Calculate the time
        self.time = int(self.maxSeconds * 1000)
        self.seconds = self.maxSeconds
        self.updateTime = 25
        # Get the size of the count down line
        self.update()
        self.barWidth = self.winfo_width()
        # Create a rectangle that spans the width of the canvas
        self.coords(self.bar, (0, 0, self.barWidth, self.height))
        self.update()
        # Calculate the amount we need to adjust the width with every update call
        self.updateSize = self.updateTime * self.barWidth / self.time
        # Start counting down
        self.after(self.updateTime, self.updateBar)
    
    def updateBar(self):
        # As long as we have more time decrement the bars length
        if self.time >= 0:
            # The new bar size
            self.barWidth -= self.updateSize
            # The new time in milliseconds
            self.time -= self.updateTime
            self.seconds = math.ceil(self.time / 1000)

            # If there is a seconds label update it only if the time is greater than 0
            #   This is necessary because above we only check if time is greater than or 
            #   equal to 0 because we want the bar to reach bellow 0 so it "disapears"
            if self.secondsLabel and self.time > 0:
                self.secondsLabel.configure(text=self.seconds)

            # Refresh the page to show the new bar size
            self.coords(self.bar, (0, 0, self.barWidth, self.height))
            self.update()
            self.after(self.updateTime, self.updateBar)

        # Once time is out reset out time variable
        else:
            if self.callback:
                self.callback()
