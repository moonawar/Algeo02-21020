# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2

# ========= FUNCTIONS =========
# --* Pop Up Camera *-- #
def popUpCamera(root):
   win = Toplevel(root)
   win.title("Camera")

   # Create a Label to capture the Video frames
   cam = Label(win)
   cam.pack()
   cap = cv2.VideoCapture(0)

   # Set the size of the window based on cam res
   width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
   height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

   win.geometry(f"{width}x{height + 80}")
   win.configure(bg = "#07111F")

   # Capture button
   # bottomFrame = Frame(win, bg = "#07111F")
   # bottomFrame.pack(side = BOTTOM)

   captureBtnImage = ImageTk.PhotoImage(Image.open("assets/capture_btn.png"))

   captureBtn = Button(win, text = "Capture", image = captureBtnImage, background="#07111F", borderwidth = 0, highlightthickness = 0, activebackground="#07111F", 
                      )
   captureBtn.place(y = height + 40, x = width/2, anchor = CENTER)

   # Define function to show frame
   def show_frames():
      # Get the latest frame and convert into Image
      cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
      cv2image = cv2.flip(cv2image, 1)
      img = Image.fromarray(cv2image)
      # Convert image to PhotoImage
      imgtk = ImageTk.PhotoImage(image = img)
      cam.imgtk = imgtk
      cam.configure(image = imgtk)
      # Repeat after an interval to capture continiously
      cam.after(10, show_frames)

   show_frames()
   win.mainloop()

# --* Capture Photo *-- #
