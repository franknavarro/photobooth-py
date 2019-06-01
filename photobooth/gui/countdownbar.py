import tkinter as tk

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

        # Check if a call back function is defined
        if 'callback' in kwargs:
            self.callback = kwargs.get('callback')
        else:
            self.callback = None

        # Calculate the time
        self.time = int(self.maxSeconds * 1000)
        self.updateTime = 10

        # Create the bar we will be updating
        self.bar = self.create_rectangle(0, 0, 0, 0, fill=self.color, outline="")


    def start(self):
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
            self.barWidth -= self.updateSize
            self.time -= self.updateTime
            self.coords(self.bar, (0, 0, self.barWidth, self.height))
            self.update()
            self.after(self.updateTime, self.updateBar)

        # Once time is out reset out time variable
        else:
            self.time = int(self.maxSeconds * 1000)
            if self.callback:
                self.callback()
