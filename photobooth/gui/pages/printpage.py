import tkinter as tk
import cups
import os

from photobooth.settings import config

class PrintPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])
        self.controller = controller

        # Variables to hold the text
        self.printText = "Printing in progress"
        # Get the description texts
        self.topText = controller.topText
        self.botText = controller.botText

        # Size the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add the canvas where the text will be created
        self.canvas = tk.Canvas(self, bg=self["bg"], bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Open the connection to cups
        self.connection = cups.Connection()

        # Get the default printer
        printers = self.connection.getPrinters().keys()
        self.printerName = list(printers)[0]

        # These make it so we have no borders when printing
        self.printOptions = {
            "page-left":"0",
            "page-right":"0",
            "page-top":"0",
            "page-bottom":"0"
        }


    def initializePage(self):
        # Only used for testing
        self.count = 0
        # Update all the text for this page
        self.topText.hideText()
        self.botText.hideText()
        self.text = self.canvas.create_text(0, 0, fill=config.get('Apperance', 'fontColor'), text=self.printText, font=("Droid", 65, "bold"), anchor="nw")
        self.dots = ""
        # Get the selected image
        self.printImage = self.controller.printImage
        # Get the size of the canvas and text
        self.size = (self.winfo_width(), self.winfo_height())
        self.textSize = self.canvas.bbox(self.text)
        # Position the text
        textX = int((self.size[0] - self.textSize[2]) / 2)
        textY = int((self.size[1] - self.textSize[3]) / 2)
        self.canvas.move(self.text, textX, textY)
        self.update()
        # Begin the print job
        #self.printID = self.connection.printFile(self.printerName, self.printImage, "Photobooth", self.printOptions)
        # Update the dots so we know something is happening
        self.after(1000, self.checkPrintStatus)

    def checkPrintStatus(self):
        # Check if the print job is done
        # if self.connection.getJobs().get(self.printID, None) is not None:
        if self.count < 10:
            self.count += 1
            # Add a dot
            if len(self.dots) < 3:
                self.dots += "."
            # If more then 3 dots reset the dots
            else:
                self.dots = ""

            self.canvas.itemconfigure(self.text, text=self.printText + self.dots)
            self.after(1000, self.checkPrintStatus)
        else:
            self.canvas.delete(self.text)
            self.controller.controller.showMain()
            
