from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

# -- Global Variables -- #
inputImage_path = None
closestResult_path = None

root = Tk()

# -- Getting Resolution Right -- #
RESOLUTION_FACTOR = root.winfo_screenwidth() / 1440
WINDOW_WIDTH = min(int(1260 * RESOLUTION_FACTOR), 1440)
WINDOW_HEIGHT = min(int(675 * RESOLUTION_FACTOR), 880)
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
icon = ImageTk.PhotoImage(Image.open("assets/icon.png").resize((65, 65)))
iconCanvas.create_image(0, 0, anchor = NW, image = icon)

# --% Input Frame %-- #
chooseFileImg = ImageTk.PhotoImage(Image.open("assets/choose_file_btn.png"))

# Frame tempat untuk memasukkan input gambar, baik itu dari dataset, maupun untuk gambar uji
inputCanvas = Canvas(root, background = "#0D356A", highlightthickness = 0)
inputCanvas.place(relheight = 0.88, relwidth = 0.3, rely = 0.12)
inputCanvasBG = ImageTk.PhotoImage(Image.open("assets/input_canvas_bg.png").resize((int(WINDOW_WIDTH * 0.3), int(WINDOW_HEIGHT * 0.88))))
inputCanvas.create_image(0, 0, anchor = NW, image = inputCanvasBG)

# A. Insert Dataset
# . Input Dataset Label
inputDatasetLabel = Label(inputCanvas, text = "Insert Your Dataset", font = ("Montserrat", int(FONT20 * 0.9), "bold"), bg = "#0D356A", fg = "white", anchor = W)
inputDatasetLabel.place(relx = 0.11, rely = 0.075)

# . Input Dataset Button
inputDatasetBtn = Button(inputCanvas, image = chooseFileImg, borderwidth = 0, highlightthickness = 0, cursor = "hand2", bg = "#0D356A", activebackground="#0D356A")
inputDatasetBtn.place(relx = 0.11, rely = 0.15, relwidth = 0.4, relheight = 0.05)

# . Chosen Dataset Label
chosenDatasetLabel = Label(inputCanvas, text = "No file chosen", font = ("Montserrat", int(FONT16 * 0.9)), bg = "#0D356A", fg = "white", anchor = W)
chosenDatasetLabel.place(relx = 0.52, rely = 0.15)

# B. Insert Test Image
# . Input Test Image Label
inputTestImageLabel = Label(inputCanvas, text = "Insert Your Test Image", font = ("Montserrat", int(FONT20 * 0.9), "bold"), bg = "#0D356A", fg = "white", anchor = W)
inputTestImageLabel.place(relx = 0.11, rely = 0.27)

# . Input Dataset Button
inputTestImageBtn = Button(inputCanvas, image = chooseFileImg, borderwidth = 0, highlightthickness = 0, cursor = "hand2", bg = "#0D356A", activebackground="#0D356A")
inputTestImageBtn.place(relx = 0.11, rely = 0.35, relwidth = 0.4, relheight = 0.05)

# . Input Test Image Button
chosenTestImageLabel = Label(inputCanvas, text = "No file chosen", font = ("Montserrat", int(FONT16 * 0.9)), bg = "#0D356A", fg = "white", anchor = W)
chosenTestImageLabel.place(relx = 0.52, rely = 0.35)

# . Use Camera Label
useCameraLabel = Label(inputCanvas, text = "Use camera instead?", font = ("Montserrat", int(FONT16 * 0.8), "underline"), bg = "#0D356A", fg = "white", anchor = W)
useCameraLabel.place(relx = 0.11, rely = 0.42)

# . Use Camera Button
useCameraIcon = ImageTk.PhotoImage(Image.open("assets/cam_btn.png"))
useCameraBtn = Button(inputCanvas, image = useCameraIcon, borderwidth = 0, highlightthickness = 0, cursor = "hand2", bg = "#0D356A", activebackground="#0D356A")
useCameraBtn.place(relx = 0.55, rely = 0.425)

# C. Run the Test 
# . Run the Test Label
runTestIcon = ImageTk.PhotoImage(Image.open("assets/run_btn.png"))
runTestLabel = Label(inputCanvas, text = "Run the test", font = ("Montserrat", int(FONT20 * 0.9), "bold"), bg = "#0D356A", fg = "white", anchor = W)
runTestLabel.place(relx = 0.11, rely = 0.55)

# . Run the Test Button
runTestBtn = Button(inputCanvas, image = runTestIcon, borderwidth = 0, highlightthickness = 0, cursor = "hand2", bg = "#0D356A", activebackground="#0D356A")
runTestBtn.place(relx = 0.52, rely = 0.55)

# --% Output Frame %-- #
outputFrame = Frame(root, bg = "#D9D9D9")
outputFrame.place(relheight = 0.88, relwidth = 0.7, relx = 0.3, rely = 0.12)

# A. Output Test Image
outputTestImageLabel = Label(outputFrame, text = "Test Image", font = ("Montserrat", int(FONT20 * 0.9), "bold"), fg="black", bg="#D9D9D9", anchor = W)
outputTestImageLabel.place(relx = 0.07, rely = 0.07)

outputTestImageCanvas = Canvas(outputFrame, width = IMG_SIZE, height = IMG_SIZE, background = "#B8B8B8", highlightthickness = 0)
outputTestImageCanvas.place(relx = 0.07, rely = 0.15)

# B. Output Closest Result
outputClosestResultLabel = Label(outputFrame, text = "Closest Result", font = ("Montserrat", int(FONT20 * 0.9), "bold"), fg="black", bg="#D9D9D9", anchor = W)
outputClosestResultLabel.place(relx = 0.52, rely = 0.07)

outputClosestResultCanvas = Canvas(outputFrame, width = IMG_SIZE, height = IMG_SIZE, background = "#B8B8B8", highlightthickness = 0)
outputClosestResultCanvas.place(relx = 0.52, rely = 0.15)

# C. Result Summary
resultSummaryFrame = Frame(outputFrame, bg = "#07111F")
resultSummaryFrame.place(rely = 0.75, relheight = 0.25, relwidth = 1)

resultSummaryLabel = Label(resultSummaryFrame, text = "Results Summary", font = ("Montserrat", int(FONT16 * 0.9), "bold"), fg="white", bg="#07111F", anchor = W)
resultSummaryLabel.place(relx = 0.07, rely = 0.2)

resultExecTimeLabel = Label(resultSummaryFrame, text = "Execution Time : ", font = ("Montserrat", int(FONT16 * 0.8)), fg="white", bg="#07111F", anchor = W)
resultExecTimeLabel.place(relx = 0.07, rely = 0.37)

resultExecTimeValue = Label(resultSummaryFrame, text = "00.00", font = ("Montserrat", int(FONT16 * 0.8)), fg="#E2BD45", bg="#07111F", anchor = W)
resultExecTimeValue.place(relx = 0.25, rely = 0.37)

resultSummaryOutput = Label(resultSummaryFrame, text = "The closest result to the test image is", 
                            font = ("Montserrat", int(FONT16 * 0.8)), fg="white", bg="#07111F", anchor = W)
resultSummaryOutput.place(relx = 0.07, rely = 0.6)

root.mainloop()