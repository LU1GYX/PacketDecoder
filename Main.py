from tkinter import *
from Packet import Packet
from Window import Window

window = Tk() #Creating the Window Object
app = Window(window) #Initializing Object

window.wm_title("Frame Decoder") # set window title
window.geometry("600x130") #Setting up the dimension of the Window (600x110 CROPPED)
window.resizable(False, False) #Avoiding resizing the window
window.iconbitmap("package.ico")
window.mainloop() #Necessary to start the configured window

window.mainloop()