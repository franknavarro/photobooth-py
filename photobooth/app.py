import tkinter as tk
import sys

class RootWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #self.attributes('-fullscreen', True)
        self.geometry("500x500")
        self.configure(cursor='none')
        container = ApplicationFrame(self)
        self.bind('<Escape>', self.close)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.focus_set()
        frame.tkraise()

    def close(self, event):
        sys.exit()

class ApplicationFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side="top", fill="both", expand = True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        parent.frames = {}
        frame = StartPage(self, parent)
        parent.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        parent.show_frame(StartPage)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

	# Center page 
        self.configure(background='white')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

	# Add name of application to center
        appname = tk.Label(self, text="Photobooth", font=("Droid",50,'bold italic'))
        appname.grid(row=0, column=0, sticky="nsew")

        # Add push button text to bottom
        instruct = tk.Label(self, text="Push button to start", font=("Droid", 25, 'bold'))
        instruct.grid(row=1, column=0, sticky='sew')

        # Bind Space bar to go to camera event
        print("Starting Bind")
        self.bind('<space>', self.startcam)


    def startcam(self, event):
        print("Starting Camera Service...")



# Run the application
def run():
    root = RootWindow()
    root.mainloop()
