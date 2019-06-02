import tkinter as tk
import cups
import os

class PrintPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=parent["bg"])
        self.controller = controller

        # Variables to hold the text
        self.printText = "Printing in progress"
        self.dots = ""
        # Get the description texts
        self.topText = controller.topText
        self.botText = controller.botText



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
        # Get the selected image
        self.printImage = self.controller.printImage
        # Hide the texts as we won't use them in this
        self.topText.updateText(self.printText)
        self.botText.hideText()
        # Begin the print job
        self.printID = self.connection.printFile(self.printerName, self.printImage, "Photobooth", self.printOptions)
        # Update the dots so we know something is happening
        self.after(1000, self.checkPrintStatus)

    def checkPrintStatus(self):
        # Check if the print job is done
        if self.connection.getJobs().get(self.printID, None) is not None:
            # Add a dot
            if len(self.dots) < 3:
                self.dots += "."
            # If more then 3 dots reset the dots
            else:
                self.dots = ""

            self.topText.updateText(self.printText + self.dots)
            self.after(1000, self.checkPrintStatus)
        else:
            self.controller.setUpCameraPage()
            
