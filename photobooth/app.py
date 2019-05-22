import tkinter as tk
import sys

class RootWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.attributes('-fullscreen', True)
        container = ApplicationFrame(self)
        self.bind('<Escape>', self.close)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
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

        label = tk.Label(self, text="PRESS BUTTON", font=("Verdana",12))
        label.pack(pady=10,padx=10)



# Run the application
def run():
    root = RootWindow()
    root.mainloop()
