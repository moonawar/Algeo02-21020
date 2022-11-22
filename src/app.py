from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from image_handler import *
import euclidean_distance as ed
import cv2 as cv
import camerainput as cam
import time as t
import os

# --% Global Variables %-- #
inputImage_path = None
dataset_path = None
closestResult_path = None

NO_FILE_CHOSEN = "No file chosen"
DATASET_INPUT = NO_FILE_CHOSEN
TEST_INPUT = NO_FILE_CHOSEN

SUMMARY = ""
STARTING_TIME = None

eigen_faces = None
test_image_weights = None
dataset_mean = None
image_index = None

app_path = os.path.dirname(os.path.abspath(__file__))

isShowingOriginalImage = True # Otherwise, show inputted image which is on grayscale mode
isShowingClosestImage = True # Otherwise, show the reconstructed image

# --% Functions %-- #
def selectDataset():
    # Select dataset foldet with images
    global dataset_path 
    dataset_path = filedialog.askdirectory(initialdir=f"{app_path}/../test/", title="Select Dataset")

    global chosenDatasetLabel
    dataset_folder = ""
    if dataset_path != "":
        for c in dataset_path:
            if c == "/":
                dataset_folder = ""
            else:
                dataset_folder += c

        DATASET_INPUT = dataset_folder
        chosenDatasetLabel.config(text = DATASET_INPUT)
        updateSummary("")
        delWarning()
    else:
        dataset_path = None
        DATASET_INPUT = NO_FILE_CHOSEN
        chosenDatasetLabel.config(text = DATASET_INPUT)

    global outputClosestResultCanvas
    outputClosestResultCanvas.delete("all")
    resetExecTime()

def selectTestImage():
    # Select test image
    global inputImage_path
    inputImage_path = filedialog.askopenfilename(initialdir=f"{app_path}/../test/", title="Select Test Image", filetypes=(("image files", "*.jpg *.png *.gif *.jpeg"), ("all files", "*.*")))

    test_image = ""
    if inputImage_path != "":
        for c in inputImage_path:
            if c == "/":
                test_image = ""
            else:
                test_image += c
        
        if (len(test_image) > 32):
            test_image = "..." + test_image[-32:]

        TEST_INPUT = test_image
        global chosenTestImageLabel
        chosenTestImageLabel.config(text = TEST_INPUT)
        updateInputImage()
        delWarning()

    global outputClosestResultCanvas
    outputClosestResultCanvas.delete("all")
    resetExecTime()
    updateSummary("")

def updateInputImage():
    # Update input image GUI (showing image on the panel)
    testInputImage = Image.open(inputImage_path)
    testInputImage = SquareCropImageTk(testInputImage)
    testInputImage = ResizeImage(testInputImage, IMG_SIZE)

    global f_testInputImage 
    f_testInputImage =  ImageTk.PhotoImage(testInputImage)

    global outputTestImageCanvas
    outputTestImageCanvas.delete("all")
    outputTestImageCanvas.create_image(0, 0, anchor=NW, image=f_testInputImage)

def updateClosestResultImage():
    # Update closest result image GUI (showing image on the panel)
    closestResultImage = Image.open(closestResult_path)
    closestResultImage = SquareCropImageTk(closestResultImage)
    closestResultImage = ResizeImage(closestResultImage, IMG_SIZE)

    global f_closestResultImage 
    f_closestResultImage =  ImageTk.PhotoImage(closestResultImage)

    global outputClosestResultCanvas
    outputClosestResultCanvas.delete("all")
    outputClosestResultCanvas.create_image(0, 0, anchor=NW, image=f_closestResultImage)

def updateSummary(summary):
    # Update summary GUI (showing summary on the panel)
    global SUMMARY
    SUMMARY = summary

    global resultSummaryOutput
    resultSummaryOutput.config(text = SUMMARY)

def popUpWarning(warning):
    # Pop up warning message
    global warningLabel
    warningLabel.config(text = warning)

def delWarning():
    # Delete warning message
    global warningLabel
    warningLabel.config(text = "")

def updateExecTime():
    # Update execution time GUI (showing execution time on the panel)
    global STARTING_TIME
    global resultExecTimeValue

    if STARTING_TIME != None:
        execTime = t.time() - STARTING_TIME
        resultExecTimeValue.config(text = "{0:.2f} seconds".format(execTime))
    else:
        resultExecTimeValue.config(text = "0.0 seconds")

def resetExecTime():
    # Reset execution time GUI (showing execution time on the panel)
    global STARTING_TIME
    STARTING_TIME = None

    global resultExecTimeValue
    resultExecTimeValue.config(text = "0.0 seconds")

def toggleShowOriginalImage():
    # Toggle between showing original image and inputted image
    global isShowingOriginalImage
    global toggleOriginalImageBtn
    global toggleOff
    global toggleOn

    if inputImage_path != None:
        if isShowingOriginalImage:
            toggleOriginalImageBtn.config(image = toggleOff)
            isShowingOriginalImage = False
            
            img = cv.imread(inputImage_path, cv.IMREAD_GRAYSCALE)
            img = SquareCropImageCV(img)
            img = cv.resize(img, (IMG_SIZE, IMG_SIZE))

            global f_testInputImage
            f_testInputImage = ImageTk.PhotoImage(Image.fromarray(img))

            global outputTestImageCanvas
            outputTestImageCanvas.delete("all")
            outputTestImageCanvas.create_image(0, 0, anchor=NW, image=f_testInputImage)
            
        else:
            toggleOriginalImageBtn.config(image = toggleOn)
            updateInputImage()
            isShowingOriginalImage = True
    else:
        popUpWarning("Please select a test image.")

def toggleShowClosestImage():
    # Toggle between showing closest image and reconstructed image
    global isShowingClosestImage
    global toggleClosestImageBtn
    global toggleOff
    global toggleOn

    import face_recog as fr

    if closestResult_path != None:
        if isShowingClosestImage:
            toggleClosestImageBtn.config(image = toggleOff)

            global dataset_mean, eigen_faces, test_image_weights
            img = fr.ReconstructImage(eigen_faces, dataset_mean, test_image_weights)

            global f_closestResultImage
            f_closestResultImage = ImageTk.PhotoImage(Image.fromarray(img).resize((IMG_SIZE, IMG_SIZE)))

            global outputClosestResultCanvas
            outputClosestResultCanvas.delete("all")
            outputClosestResultCanvas.create_image(0, 0, anchor=NW, image=f_closestResultImage)

            isShowingClosestImage = False
        else:
            toggleClosestImageBtn.config(image = toggleOn)
            updateClosestResultImage()
            isShowingClosestImage = True
    else:
        popUpWarning("Please run the face recognition first.")

def RunFaceRecognition():
    # Run face recognition
    global dataset_path
    global inputImage_path
    global closestResult_path
    global eigen_faces, dataset_mean, test_image_weights

    eigen_faces = None
    dataset_mean = None
    test_image_weights = None

    global STARTING_TIME

    import face_recog as fr

    if dataset_path == None or inputImage_path == None:
        popUpWarning("Please select a dataset and a test image.")
        return   

    STARTING_TIME = t.time()
    closestResult_path = fr.FaceRecognition(dataset_path, inputImage_path)
    if closestResult_path == -1:
        updateSummary("No close face detected in the test image.")
        updateExecTime()
    else:
        updateClosestResultImage()
        updateExecTime()

# --* Open Camera *-- #
def openCamera():
    global root
    cam.popUpCamera(root)


def START_APP():
    global root
    root = Tk()

    # --% Getting Resolution Right %-- #
    global RESOLUTION_FACTOR
    RESOLUTION_FACTOR = root.winfo_screenwidth() / 1440

    WINDOW_WIDTH = min(int(1260 * RESOLUTION_FACTOR), 1440)
    WINDOW_HEIGHT = min(int(675 * RESOLUTION_FACTOR), 880)

    global IMG_SIZE
    IMG_SIZE = min(int(400 * RESOLUTION_FACTOR), 400)

    FONT28 = min(int(28 * RESOLUTION_FACTOR), 28)
    FONT20 = min(int(20 * RESOLUTION_FACTOR), 20)
    FONT16 = min(int(16 * RESOLUTION_FACTOR), 16)

    # --% Window Configuration %-- #
    root.title("Face Recognition App : Ei")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)

    # --% Title Frame %-- #
    titleFrame = Frame(root, bg = "#07111F")
    titleFrame.place(relheight = 0.12, relwidth = 1)

    # . Title Label
    titleLabel = Label(titleFrame, text = "Face Recognition", font = ("Montserrat", int(FONT28), "bold"), bg = "#07111F", fg = "#E2BD45", anchor = W)
    titleLabel.place(relx = 0.04, rely = 0.1, relheight = 0.8)

    # . Icon
    iconCanvas = Canvas(titleFrame, width = 65, height = 65, background = "#07111F" , highlightthickness = 0)
    iconCanvas.place(relx = 0.92, rely = 0.18)
    icon = ImageTk.PhotoImage(Image.open(f"{app_path}/assets/icon.png").resize((65, 65)))
    iconCanvas.create_image(0, 0, anchor = NW, image = icon)

    # --% Input Frame %-- #
    chooseFileImg = ImageTk.PhotoImage(Image.open(f"{app_path}/assets/choose_file_btn.png"))

    # Frame tempat untuk memasukkan input gambar, baik itu dari dataset, maupun untuk gambar uji
    inputCanvas = Canvas(root, background = "#0D356A", highlightthickness = 0)
    inputCanvas.place(relheight = 0.88, relwidth = 0.3, rely = 0.12)
    inputCanvasBG = ImageTk.PhotoImage(Image.open(f"{app_path}/assets/input_canvas_bg.png").resize((int(WINDOW_WIDTH * 0.3), int(WINDOW_HEIGHT * 0.88))))
    inputCanvas.create_image(0, 0, anchor = NW, image = inputCanvasBG)

    # A. Insert Dataset
    # . Input Dataset Label
    inputDatasetLabel = Label(inputCanvas, text = "Insert Your Dataset", font = ("Montserrat", int(FONT20 * 0.9), "bold"), bg = "#0D356A", fg = "white", anchor = W)
    inputDatasetLabel.place(relx = 0.11, rely = 0.075)

    # . Input Dataset Button
    inputDatasetBtn = Button(inputCanvas, image = chooseFileImg, borderwidth = 0, highlightthickness = 0, cursor = "hand2", bg = "#0D356A", activebackground="#0D356A"
                            , command = selectDataset)
    inputDatasetBtn.place(relx = 0.11, rely = 0.15, relwidth = 0.4, relheight = 0.05)

    # . Chosen Dataset Label
    global chosenDatasetLabel

    chosenDatasetLabel = Label(inputCanvas, text = DATASET_INPUT, font = ("Montserrat", int(FONT16 * 0.9)), bg = "#0D356A", fg = "white", anchor = NW, wraplength = 170, justify = LEFT)
    chosenDatasetLabel.place(relx = 0.52, rely = 0.15)

    # B. Insert Test Image
    # . Input Test Image Label
    inputTestImageLabel = Label(inputCanvas, text = "Insert Your Test Image", font = ("Montserrat", int(FONT20 * 0.9), "bold"), bg = "#0D356A", fg = "white", anchor = W)
    inputTestImageLabel.place(relx = 0.11, rely = 0.27)

    # . Input Dataset Button
    inputTestImageBtn = Button(inputCanvas, image = chooseFileImg, borderwidth = 0, highlightthickness = 0, cursor = "hand2", bg = "#0D356A", activebackground="#0D356A",
                            command = selectTestImage)
    inputTestImageBtn.place(relx = 0.11, rely = 0.35, relwidth = 0.4, relheight = 0.05)

    # . Input Test Image Button
    global chosenTestImageLabel

    chosenTestImageLabel = Label(inputCanvas, text = TEST_INPUT, font = ("Montserrat", int(FONT16 * 0.9)), bg = "#0D356A", fg = "white", anchor = NW, wraplength = 170, justify = LEFT)
    chosenTestImageLabel.place(relx = 0.52, rely = 0.35, relheight=0.07)

    # . Use Camera Label
    useCameraLabel = Label(inputCanvas, text = "Use camera instead?", font = ("Montserrat", int(FONT16 * 0.8), "underline"), bg = "#0D356A", fg = "white", anchor = W)
    useCameraLabel.place(relx = 0.11, rely = 0.42)

    # . Use Camera Button
    useCameraIcon = ImageTk.PhotoImage(Image.open(f"{app_path}/assets/cam_btn.png"))
    useCameraBtn = Button(inputCanvas, image = useCameraIcon, borderwidth = 0, highlightthickness = 0, cursor = "hand2", bg = "#0D356A", activebackground="#0D356A",
                        command = openCamera)
    useCameraBtn.place(relx = 0.55, rely = 0.425)

    # C. Run the Test 
    # . Run the Test Label
    runTestIcon = ImageTk.PhotoImage(Image.open(f"{app_path}/assets/run_btn.png"))
    runTestLabel = Label(inputCanvas, text = "Run the test", font = ("Montserrat", int(FONT20 * 0.9), "bold"), bg = "#0D356A", fg = "white", anchor = W)
    runTestLabel.place(relx = 0.11, rely = 0.55)

    # . Run the Test Button
    runTestBtn = Button(inputCanvas, image = runTestIcon, borderwidth = 0, highlightthickness = 0, cursor = "hand2", bg = "#0D356A", activebackground="#0D356A",
                        command = RunFaceRecognition)
    runTestBtn.place(relx = 0.52, rely = 0.55)

    # . Warning Label
    global warningLabel
    warningLabel = Label(inputCanvas, font = ("Montserrat", int(FONT16 * 0.8)), bg = "#0D356A", fg = "white", anchor = W)
    warningLabel.place(relx = 0.11, rely = 0.65)

    # --% Output Frame %-- #
    outputFrame = Frame(root, bg = "#D9D9D9")
    outputFrame.place(relheight = 0.88, relwidth = 0.7, relx = 0.3, rely = 0.12)

    # . for toggle button
    global toggleOn, toggleOff
    toggleOn = ImageTk.PhotoImage(Image.open(f"{app_path}/assets/toggle_on.png"))
    toggleOff = ImageTk.PhotoImage(Image.open(f"{app_path}/assets/toggle_off.png"))
    
    # A. Output Test Image
    outputTestImageLabel = Label(outputFrame, text = "Test Image", font = ("Montserrat", int(FONT20 * 0.9), "bold"), fg="black", bg="#D9D9D9", anchor = W)
    outputTestImageLabel.place(relx = 0.07, rely = 0.04)

    global outputTestImageCanvas
    outputTestImageCanvas = Canvas(outputFrame, width = IMG_SIZE, height = IMG_SIZE, background = "#B8B8B8", highlightthickness = 0)
    outputTestImageCanvas.place(relx = 0.07, rely = 0.12)

    global toggleOriginalImageBtn
    toggleOriginalImageBtn = Button(outputFrame, background = "#D9D9D9", highlightthickness = 0, border = 0, image = toggleOn, 
                                    cursor = "hand2", command = toggleShowOriginalImage)
    toggleOriginalImageBtn.place(relx = 0.07, rely = 0.66)

    toggleOriginalImageLabel = Label(outputFrame, text = "Toggle Original/Grayscale Image", font = ("Montserrat", int(FONT16 * 0.72), "bold"), bg = "#D9D9D9", 
                                    fg = "black", anchor = NW)
    toggleOriginalImageLabel.place(relx = 0.14, rely = 0.655)

    # B. Output Closest Result
    outputClosestResultLabel = Label(outputFrame, text = "Closest Result", font = ("Montserrat", int(FONT20 * 0.9), "bold"), fg="black", bg="#D9D9D9", anchor = W)
    outputClosestResultLabel.place(relx = 0.52, rely = 0.04)

    global outputClosestResultCanvas
    outputClosestResultCanvas = Canvas(outputFrame, width = IMG_SIZE, height = IMG_SIZE, background = "#B8B8B8", highlightthickness = 0)
    outputClosestResultCanvas.place(relx = 0.52, rely = 0.12)

    global toggleClosestImageBtn
    toggleClosestImageBtn = Button(outputFrame, background = "#D9D9D9", highlightthickness = 0, border = 0, image = toggleOn, cursor="hand2", command = toggleShowClosestImage)
    toggleClosestImageBtn.place(relx = 0.52, rely = 0.66)

    toggleClosestImageLabel = Label(outputFrame, text = "Toggle Closest Image/Reconstructed Image", font = ("Montserrat", int(FONT16 * 0.72), "bold"), bg = "#D9D9D9", 
                                    fg = "black", anchor = NW)
    toggleClosestImageLabel.place(relx = 0.59, rely = 0.655)


    # C. Result Summary
    resultSummaryFrame = Frame(outputFrame, bg = "#07111F")
    resultSummaryFrame.place(rely = 0.75, relheight = 0.25, relwidth = 1)

    resultSummaryLabel = Label(resultSummaryFrame, text = "Results Summary", font = ("Montserrat", int(FONT16 * 0.9), "bold"), fg="white", bg="#07111F", anchor = W)
    resultSummaryLabel.place(relx = 0.07, rely = 0.2)

    resultExecTimeLabel = Label(resultSummaryFrame, text = "Execution Time : ", font = ("Montserrat", int(FONT16 * 0.8)), fg="white", bg="#07111F", anchor = W)
    resultExecTimeLabel.place(relx = 0.07, rely = 0.37)

    global resultExecTimeValue
    resultExecTimeValue = Label(resultSummaryFrame, text = "00.00", font = ("Montserrat", int(FONT16 * 0.8)), fg="#E2BD45", bg="#07111F", anchor = W)
    resultExecTimeValue.place(relx = 0.25, rely = 0.37)

    global resultSummaryOutput
    resultSummaryOutput = Label(resultSummaryFrame, text = SUMMARY, 
                                font = ("Montserrat", int(FONT16 * 0.8)), fg="white", bg="#07111F", anchor = W)
    resultSummaryOutput.place(relx = 0.07, rely = 0.6)

    root.mainloop()