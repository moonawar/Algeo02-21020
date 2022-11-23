# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2
import os
import app
import time

# ==== GLOBAL VARIABLES ====
app_path = os.path.dirname(os.path.abspath(__file__))

TRAINING = 0
TESTING = 1

toggleOnImg = None
toggleOffImg = None
toggleBtn = None
modeLabel = None
modeInfoLabel = None

currentMode = TRAINING

cap = None

training_count = 0

Training_Mode_Info = "You're in training mode. Click on the capture button to capture your image. You can capture as many images as you want." 
" Once you're done, click on the toggle button to switch to testing mode."

Testing_Mode_Info = "You're in testing mode. Click on the capture button to capture your image. Capture will only occur once and after that, you will be "
"redirected to the main application."

win = None

# ========= FUNCTIONS =========
def changeMode():
   global currentMode
   global modeLabel
   global toggleBtn
   global modeInfoLabel

   if currentMode == TRAINING:
      currentMode = TESTING
      modeLabel.configure(text = "Current Mode : Testing Mode")

      modeInfoLabel.configure(text = Testing_Mode_Info)

      global toggleOffImg
      toggleBtn.configure(image = toggleOffImg)
   else:
      currentMode = TRAINING
      modeLabel.configure(text = "Current Mode : Training Mode")

      modeInfoLabel.configure(text = Training_Mode_Info)

      global toggleOnImg
      toggleBtn.configure(image = toggleOnImg)

# --* Pop Up Camera *-- #
def popUpCamera(root):
   global win

   win = Toplevel(root)
   win.title("Camera")

   # Create a Label to capture the Video frames
   cam = Label(win)
   cam.pack()

   global cap
   cap = cv2.VideoCapture(0)

   # Set the size of the window based on cam res
   MIN_WIDTH = 900
   
   width = max(MIN_WIDTH, int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
   height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

   win.geometry(f"{width}x{height + 80}")
   win.configure(bg = "#07111F")
   win.resizable(False, False)

   captureBtnImage = ImageTk.PhotoImage(Image.open(f"{app_path}/assets/capture_btn.png"))

   captureBtn = Button(win, text = "Capture", image = captureBtnImage, background="#07111F", borderwidth = 0, highlightthickness = 0, activebackground="#07111F", 
                      cursor="hand2", command=capturePhoto)
   captureBtn.place(y = height + 40, x = width/2, anchor = CENTER)

   # . Toggle Mode Button
   global toggleOnImg, toggleOffImg

   toggleOnImg = ImageTk.PhotoImage(Image.open(f"{app_path}/assets/toggle_on.png"))
   toggleOffImg = ImageTk.PhotoImage(Image.open(f"{app_path}/assets/toggle_off.png"))

   global toggleBtn
   toggleBtn = Button(win, image = toggleOnImg, background="#07111F", borderwidth = 0, highlightthickness = 0, activebackground="#07111F", command = changeMode,
                      cursor="hand2")
   toggleBtn.place(relx = 0.025, rely = 0.92 , anchor = NW)

   # . Mode Label
   global modeLabel
   modeLabel = Label(win, text = "Current Mode : Training Mode", font = ("Montserrat", 12), bg = "#07111F", fg = "#FFFFFF")
   modeLabel.place(relx = 0.07, rely = 0.92, anchor = NW)

   # . Mode Info Label
   global modeInfoLabel
   modeInfoLabel = Label(win, text = Training_Mode_Info, font = ("Montserrat", 10), bg = "#07111F", fg = "#FFFFFF", wraplength = 0.35 * width, justify = LEFT)
   modeInfoLabel.place(relx = 0.62, rely = 0.9, anchor = NW)

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

def exitCamera():
   global win
   app.dataset_path = f"{app_path}/../test/dataset/camera training"
   app.inputImage_path = f"{app_path}/../test/camera testing/testing.png"
   app.updateInputImage()

   app.chosenDatasetLabel.configure(text = f"camera training")
   app.chosenTestImageLabel.configure(text = f"testing.png")

   win.destroy()

def imageCapturedNotification():
   global win
   global training_count
   captureNotificationLabel = Label(win, text = f"Image {training_count + 1} Captured.", font = ("Montserrat", 13), bg = "#07111F", fg = "#FFFFFF")
   captureNotificationLabel.place(relx = 0.5, rely = 0.6, anchor = CENTER)

   captureNotificationLabel.after(2000, lambda: captureNotificationLabel.destroy())

# --* Capture Photo *-- #
def capturePhoto():
   global cap
   cv2image = cap.read()[1]
   cv2image = cv2.flip(cv2image, 1)
   imageCapturedNotification()
   
   if currentMode == TRAINING:
      global training_count
      if os.path.exists(f"{app_path}/../test/dataset/camera training/") and training_count == 0:
         for file in os.listdir(f"{app_path}/../test/dataset/camera training/"):
            os.remove(f"{app_path}/../test/dataset/camera training/{file}")
         os.rmdir(f"{app_path}/../test/dataset/camera training/")

      if not os.path.exists(f"{app_path}/../test/dataset/camera training/"):
         os.mkdir(f"{app_path}/../test/dataset/camera training/")
      
      cv2.imwrite(f"{app_path}/../test/dataset/camera training/training {training_count}.png", cv2image)
      training_count += 1
   else:
      if os.path.exists(f"{app_path}/../test/camera testing/testing.png"):
         for file in os.listdir(f"{app_path}/../test/camera testing/"):
            os.remove(f"{app_path}/../test/camera testing/{file}")
         os.rmdir(f"{app_path}/../test/camera testing/")
      
      if not os.path.exists(f"{app_path}/../test/camera testing/"):
         os.mkdir(f"{app_path}/../test/camera testing/")

      cv2.imwrite(f"{app_path}/../test/camera testing/testing.png", cv2image)
      exitCamera()
      