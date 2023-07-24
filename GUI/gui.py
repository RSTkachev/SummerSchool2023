import os
import tkinter as tk
from tkinter import filedialog as fd
from tkVideoPlayer import TkinterVideo

APP_NAME = "Recognizer"
BUTTON_IMG_LOAD_VIDEO = "button_image.png"
MAIN_COLOR = "#1E1E1E"
PATH_TO_RESULT = "../yolov5/runs/detect/"


def chooseVideo():
    file_name = fd.askopenfilename()
    return file_name


def detect(pathToFile: str):
    action = f"python ../yolov5/detect.py --weights ../yolov5/kek.pt --source {pathToFile}"
    print(action)
    os.system(action)


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # Configure the root window
        self.title(APP_NAME)
        self.iconbitmap('icon.ico')

        # Images
        self.bgImage = tk.PhotoImage(file="bg.png")
        self.buttonImageLoadVideo = tk.PhotoImage(file=BUTTON_IMG_LOAD_VIDEO)
        self.imagePlay = tk.PhotoImage(file="play.png")
        self.imagePause = tk.PhotoImage(file="pause.png")

        # Configure MainWindow
        self["bg"] = MAIN_COLOR

        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        self.windowWidth = self.bgImage.width()
        self.windowHeight = self.bgImage.height()

        centerX = int(screenWidth / 2 - self.windowWidth / 2)
        centerY = int(screenHeight / 2 - self.windowHeight / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{self.windowWidth}x{self.windowHeight}+{centerX}+{centerY - 30}')

        # UI ELEMENTS
        # Video player
        self.videoPlayer = TkinterVideo(self, scaled=True, bg=MAIN_COLOR)
        # Label with background image
        self.labelBgImage = tk.Label(self, i=self.bgImage)
        # Button for choose video
        self.btnLoadVideo = tk.Button(self, i=self.buttonImageLoadVideo,
                                      command=self.loadVideo,
                                      relief=tk.FLAT,
                                      highlightthickness=0,
                                      activebackground=MAIN_COLOR,
                                      bd=0)
        # Button for play and pause video
        self.btnPlay = tk.Button(self, image=self.imagePlay,
                                 relief=tk.FLAT,
                                 command=self.PlayAndPause)

        # Create UI
        self.initUi()

    def initUi(self):

        # self.labelBgImage = tk.Label(self)
        self.labelBgImage.place(x=0, y=0)

        self.btnLoadVideo.place(x=53, y=455)

    def PlayAndPause(self):
        if self.videoPlayer.is_paused():
            self.videoPlayer.play()
            self.btnPlay["image"] = self.imagePause
        else:
            self.videoPlayer.pause()
            self.btnPlay["image"] = self.imagePlay

    def loadVideo(self):
        pathFile = chooseVideo()
        if pathFile != "":

            # Detect people
            detect(pathFile)

            # Get result YOLO
            lastResult = [x for x in os.walk(PATH_TO_RESULT)][-1]
            pathToDetectVideo = f"{lastResult[0]}/{lastResult[2][0]}"
            print(pathToDetectVideo)

            # Hide elements
            self.labelBgImage.place_forget()
            self.btnLoadVideo.place_forget()

            # Open video player
            self.videoPlayer.load(pathToDetectVideo)
            self.videoPlayer.pack(expand=True, fill="both")

            # Display play button
            self.btnPlay["bg"] = MAIN_COLOR
            self.btnPlay.pack(expand=False, side=tk.BOTTOM)

        else:
            pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
