import tkinter as tk

class SettingsMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ffffff")

        self.controller = controller

        # Initialize the grid for the page
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Set up the container where the tabs will be displayed
        self.container = tk.Frame(self, bg=self["bg"])
        self.container.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


        # Initialize the different settings tabs
        #self.frames = {}
        #for tab in (ApperanceTab, InteractionsTab, PhotostripTab):
            #frame = tab(self.container, self)
            #self.frames[tab] = frame
            #frame.grid(row=0, column=0, stick="nsew")


    # Perform any initial configurations
    def open(self):
        # Reshow the arrow
        self.configure(cursor='arrow')
        # Bind the close key
        self.bind('x', self.close)

    # Function that will show the correct tab page
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.focus_set()

    # Show the main application once again and unbind the close button
    def close(self, event=None):
        # Rehide the cursor
        self.configure(cursor='none')
        # Unbind the close button
        self.unbind('x')
        # Show the main application
        self.controller.showMain()





