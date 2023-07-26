import os
from GUI.tkGIF import gifplay
from threading import Thread
import tkinter as tk
from tkinter import filedialog as fd
from tkVideoPlayer import TkinterVideo

APP_NAME = "Recognizer"
# Paths to images
BUTTON_IMG_LOAD_VIDEO = "resources/button_image.png"
BG_IMAGE = "resources/bg.png"
PLAY_IMAGE = "resources/play.png"
PAUSE_IMAGE = "resources/pause.png"
ICON_IMAGE = "resources/icon.ico"
BACK_IMAGE = "resources/back.png"
LOADING_GIF = "resources/loading.gif"

MAIN_COLOR = "#1E1E1E"
PATH_TO_RESULT = "StrongSORT-YOLO/runs/track/"
TIME_AWAIT = 5000


def chooseVideo():
    file_name = fd.askopenfilename()
    return file_name


def detect(pathToFile: str):
    # print(pathToFile)
    action = f"python StrongSORT-YOLO/track_v5.py --source {pathToFile} " \
             f"--yolo-weights StrongSORT-YOLO/thermal.pt --save-vid"
    # print(action)
    os.system(action)


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # Configure the root window
        self.title(APP_NAME)
        self.iconbitmap()

        # Images
        self.bgImage = tk.PhotoImage(file=BG_IMAGE)
        self.buttonImageLoadVideo = tk.PhotoImage(file=BUTTON_IMG_LOAD_VIDEO)
        self.imagePlay = tk.PhotoImage(file=PLAY_IMAGE)
        self.imagePause = tk.PhotoImage(file=PAUSE_IMAGE)
        self.imageBack = tk.PhotoImage(file=BACK_IMAGE)


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
        self.videoPlayer.bind("<<Ended>>", self.videoEnded)
        self.videoPlayer.bind("<<SecondChanged>>", self.updateScale)
        self.videoPlayer.bind("<<Duration>>", self.updateDuration)

        # Label with background image
        self.labelBgImage = tk.Label(self, i=self.bgImage)
        # Label for loading screen
        self.labelLoading = tk.Label(self, bd=0)
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
        # Button for back in main page
        self.btnBack = tk.Button(self, image=self.imageBack,
                                 bg="#1E1E1E",
                                 relief=tk.FLAT,
                                 command=self.commandBack)

        # Seconds for video
        self.progressValue = tk.IntVar(self)

        # Scale for video
        self.progressSlider = tk.Scale(self, variable=self.progressValue, bg="#BA55D3", fg="#1E1E1E", cursor="circle",
                                       from_=0, to=0, orient="horizontal", command=self.seek)


        # GIF
        self.gifLoading = gifplay(self.labelLoading, LOADING_GIF, 0.1)

        # Create UI
        self.initUi()

    def initUi(self):
        # Create main window
        self.labelBgImage.place(x=0, y=0)
        self.btnLoadVideo.place(x=53, y=455)

    def seek(self, value):
        self.videoPlayer.seek(int(value))

    def updateDuration(self, event):
        """ updates the duration after finding the duration """
        duration = self.videoPlayer.video_info()["duration"]
        self.progressSlider["to"] = duration

    def videoEnded(self, event):
        self.btnPlay["image"] = self.imagePlay

    def updateScale(self, event):
        """ updates the scale value """
        self.progressValue.set(self.videoPlayer.current_duration())

    def commandBack(self):
        # Hide elements
        self.btnBack.pack_forget()
        self.videoPlayer.pack_forget()
        self.btnPlay.pack_forget()
        self.progressSlider.pack_forget()
        # Display main window
        self.initUi()

    def PlayAndPause(self):
        if self.videoPlayer.is_paused():
            self.videoPlayer.play()
            self.btnPlay["image"] = self.imagePause
        else:
            self.videoPlayer.pause()
            self.btnPlay["image"] = self.imagePlay


    # Monitor for detect thread
    def monitor(self, thread):
        if thread.is_alive():
            self.after(TIME_AWAIT, lambda: self.monitor(thread))
        else:
            # Get result YOLO
            lastResult = [x for x in os.walk(PATH_TO_RESULT)][-1]
            pathToDetectVideo = f"{lastResult[0]}/{lastResult[2][0]}"

            # Hide loading elements
            self.labelLoading.place_forget()

            # Open video player
            self.videoPlayer.load(pathToDetectVideo)
            self.videoPlayer.pack(expand=True, fill="both")

            self.progressSlider.pack(expand=False, fill="x")

            # Display play button
            self.btnPlay["bg"] = MAIN_COLOR
            self.btnPlay.pack(expand=False)

            # Display back button
            self.btnBack.pack(expand=False, side=tk.LEFT)

    def loadVideo(self):
        pathFile = chooseVideo()
        if pathFile != "":

            # Detect people
            # detect(pathFile)
            thread = Thread(target=detect, args=(pathFile, ))
            thread.start()

            # Hide UI elements
            self.labelBgImage.place_forget()
            self.btnLoadVideo.place_forget()

            # Display load screen
            self.labelLoading.place(relx=0.45, rely=0.4)
            self.gifLoading.play()

            # Monitor thread with detect
            self.monitor(thread)

        else:
            pass


if __name__ == "__main__":
    print("Запуск из главного приложения")