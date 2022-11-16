from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from imagehandler import *
import time as t
import camerainput as cIn
 
# ========= GLOBAL VARIABLES =========
IMG_PLACEHOLDER = "assets/img_placeholder.png"

inputImage_path = IMG_PLACEHOLDER
closestResult_path = IMG_PLACEHOLDER

dataset_path = ""

f_testInputImage = None
f_closestResultImage = None

# ========= BUTTONS =========
def selectDataset():
    global dataset_path 
    dataset_path = filedialog.askdirectory(initialdir="./", title="Select Dataset")

def selectTest():
    global inputImage_path 
    inputImage_path = filedialog.askopenfilename(initialdir="./", title="Select Test Image", 
    filetypes=(("png/jpeg", "*.png, *.jpeg, *.jpg"), ("all files", "*.*")))
    updateInputImage()

def runFaceRecog():
    # global closestResult_path
    # closestResult_path = FindClosestImage(inputImage_path, dataset_path)
    # updateInputImage()
    global actualExecTimeLabel
    start = t.time()
    bufferFunction(5)
    end = t.time()
    elapsed = end - start
    if (elapsed < 10):
        actualExecTimeLabel.config(text="0{:.2f}".format(elapsed))
    else:
        actualExecTimeLabel.config(text="{:.2f}".format(elapsed))
        

def bufferFunction(sec):
    t.sleep(sec)

# ========= FUNCTIONS =========
# --* Update Input Image *-- #
def updateInputImage():
    testInputImage = Image.open(inputImage_path)
    testInputImage = SquareCropImage(testInputImage)
    testInputImage = ResizeImage(testInputImage, IMG_SIZE)

    global f_testInputImage 
    f_testInputImage =  ImageTk.PhotoImage(testInputImage)

    global testInputCanvas
    testInputCanvas.create_image(0, 0, anchor=NW, image=f_testInputImage)

    closestResultImage = Image.open(IMG_PLACEHOLDER)
    resized_closestResultImage = closestResultImage.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
    
    global f_closestResultImage 
    f_closestResultImage =  ImageTk.PhotoImage(resized_closestResultImage)

    global closestResultCanvas
    closestResultCanvas.create_image(0, 0, anchor=NW, image=f_closestResultImage)

# --* Open Camera *-- #
def openCamera():
    global window
    cIn.popUpCamera(window)

# ========= ACTUAL GUI =========
window = Tk()

# --* Getting Resolution Right *-- #
RESOLUTION_FACTOR = window.winfo_screenwidth() / 1260
WINDOW_WIDTH = min(int(1260 * RESOLUTION_FACTOR), 1260)
WINDOW_HEIGHT = min(int(675 * RESOLUTION_FACTOR), 675)
IMG_SIZE = min(int(380 * RESOLUTION_FACTOR), 380)

FONT16 = min(int(16 * RESOLUTION_FACTOR), 16)
FONT12 = min(int(12 * RESOLUTION_FACTOR), 12)

# --* Window Configuration *-- #
window.title("Face Recognition App")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.configure(background = "white")
window.resizable(False, False)

# --* Main Container *-- #
mainContainer = Frame(window, bg = "white")
mainContainer.place(relheight = 1, relwidth = 0.95, relx = 0.025)

# --* Title Frame *-- #
titleFrame = Frame(mainContainer, bg = "white")
titleFrame.pack(fill = X)

titleLabel = Label(titleFrame, text = "Face Recognition App", bg = "white", fg = "black", font = ("Segoe UI", 26), anchor = W)
titleLabel.pack(fill = X, pady = 20, padx = 20)

lineCanvas = Frame(titleFrame, bg="black", border = 0, highlightthickness = 0, height = 1)
lineCanvas.place(relx = 0.025, rely = 0.95, relwidth = 0.95)

# --* Input Frame *-- #
# Frame tempat untuk memasukkan input gambar, baik itu dari dataset, maupun untuk gambar uji
inputFrame = Frame(mainContainer, background = "white")
inputFrame.place(relheight = 0.9, relwidth = 0.25, relx = 0.02, rely = 0.2)

# Image untuk button
chooseFileImg = PhotoImage(file = "assets/chose_file_btn.png")

# Menginput Dataset
DATASET_INPUT = StringVar()
DATASET_INPUT.set("No File Chosen")

TEST_INPUT = StringVar()
TEST_INPUT.set("No File Chosen")

datasetLabel = Label(inputFrame, text = "Insert Your Dataset", font = ("Segoe UI", FONT16), bg = "white", fg = "black", anchor = W)
datasetLabel.pack(fill = X, pady = 5)

insertDatasetFrame = Frame(inputFrame, bg = "white")
insertDatasetFrame.pack(fill = X, pady = 5)

insertDatasetBtn = Button(insertDatasetFrame, font = ("Segoe UI", FONT12), bg = "white", image = chooseFileImg, border = 0,
                          highlightthickness = 0, command = selectDataset,  cursor="hand2")
insertDatasetBtn.grid(row = 0, column = 0, padx = 5)

inputtedDatasetLabel = Label(insertDatasetFrame, textvariable = DATASET_INPUT, font = ("Segoe UI", FONT12), bg = "white", fg = "black", anchor = W)
inputtedDatasetLabel.grid(row = 0, column = 1, padx = 5)

# SPACING
spacingLabel = Label(inputFrame, text = "", bg = "white")
spacingLabel.pack(fill = X, pady = 0)

# Menginput Data Test
testLabel = Label(inputFrame, text = "Insert Your Test Image", font = ("Segoe UI", FONT16), bg = "white", fg = "black", anchor = W)
testLabel.pack(fill = X, pady = 5)

insertTestFrame = Frame(inputFrame, bg = "white")
insertTestFrame.pack(fill = X, pady = 5)

insertTestBtn = Button(insertTestFrame, font = ("Segoe UI", FONT12), bg = "white", image = chooseFileImg, border = 0, 
                       highlightthickness = 0, command = selectTest,  cursor="hand2")
insertTestBtn.grid(row = 0, column = 0, padx = 5)

inputtedTestLabel = Label(insertTestFrame, textvariable = TEST_INPUT, font = ("Segoe UI", FONT12), bg = "white", fg = "black", anchor = W)
inputtedTestLabel.grid(row = 0, column = 1, padx = 5)

useCameraButton = Button(insertTestFrame, text = "Use camera instead?", font = ("Segoe UI", FONT12, "underline"), bg = "white", fg = "#6974D4", border = 0, highlightthickness = 0, 
                         command = openCamera, cursor="hand2")
useCameraButton.grid(row = 1, column = 0, pady=5)

# SPACING
spacingLabel = Label(inputFrame, text = "", bg = "white")
spacingLabel.pack(pady = 0)

# Result
runButtonImg = PhotoImage(file = "assets/run_btn.png")

runTestFrame = Frame(inputFrame, bg = "white")
runTestFrame.pack(pady = 5, fill=X)

runLabel = Label(runTestFrame, text = "Run Test", font = ("Segoe UI", FONT16, "bold"), bg = "white", fg = "black", anchor = W)
runLabel.grid(row = 0, column = 0)

runButton = Button(runTestFrame, font = ("Segoe UI", FONT16), bg = "white", border = 0, highlightthickness = 0, image = runButtonImg,
                   command = runFaceRecog, cursor = "hand2")
runButton.grid(row = 0, column = 1, padx = 20)

resultLabel = Label(inputFrame, text = "Result", font = ("Segoe UI", FONT16), bg = "white", fg = "black", anchor = W)
resultLabel.pack(fill = X, pady = 4)

actualResultLabel = Label(inputFrame, text = "None", font = ("Segoe UI", FONT16), bg = "white", fg = "#39CB74", anchor = W)
actualResultLabel.pack(fill = X, padx = 25)

# --* Output Frame *-- #
outputFrame = Frame(mainContainer, background = "white")
outputFrame.place(relheight = 0.8, relwidth = 0.7, relx = 0.3, rely = 0.18)

# Test Input
testInputFrame = Frame(outputFrame, background = "white")
testInputFrame.place(relheight = 1, relwidth = 0.5)

testInputLabel = Label(testInputFrame, text = "Test Image", font = ("Segoe UI", FONT16), anchor = W, background = "white")
testInputLabel.pack(fill = X)

testInputCanvas = Canvas(testInputFrame, bg = "gray", border = 0, highlightthickness = 0, height= IMG_SIZE, width = IMG_SIZE)
testInputCanvas.pack(anchor = NW)
testInputCanvas.create_image(0, 0, anchor = NW, image = f_testInputImage)

# Execution Time
execTimeFrame = Frame(testInputFrame, background = "white")
execTimeFrame.pack(anchor = NW, pady = 10)

execTimeLabel = Label(execTimeFrame, text = "Execution Time :", font = ("Segoe UI", FONT12), anchor = W, background = "white")
execTimeLabel.grid(row = 0, column = 0)

actualExecTimeLabel = Label(execTimeFrame, text = "00.00", font = ("Segoe UI", FONT12), anchor = W, bg = "white", fg = "#39CB74")
actualExecTimeLabel.grid(row = 0, column = 1)

# Closest Output
closestResultFrame = Frame(outputFrame, background = "white")
closestResultFrame.place(relheight = 1, relwidth = 0.5, relx = 0.5)

closestResultLabel = Label(closestResultFrame, text = "Closest Result", font = ("Segoe UI", FONT16), anchor = W, background = "white")
closestResultLabel.pack(fill = X)

closestResultCanvas = Canvas(closestResultFrame,  bg = "gray", border = 0, highlightthickness = 0, height= IMG_SIZE, width = IMG_SIZE)
closestResultCanvas.pack(anchor = NW)
closestResultCanvas.create_image(0, 0, anchor = NW, image = f_closestResultImage)

updateInputImage()

window.mainloop()