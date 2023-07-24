import torch
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkVideoPlayer import TkinterVideo
import os


root = tk.Tk()


root.title('Recognizer')
root.iconbitmap('icon.ico')

bg = tk.PhotoImage(file = "bg.png")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = bg.width()
window_height = bg.height()

# find the center point
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2) - 30

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

vid_player = TkinterVideo(root)


def LoadFile():
    file_name = fd.askopenfilename()
    return file_name

def Process():
    global vid_player
    vid_player.destroy()
    vid_player = TkinterVideo(root)
    vid_player.addr = LoadFile()

    action = 'python yolov5/detect.py --weights yolov5/kek.pt --source %s' % vid_player.addr

    # Detect
    os.system(action)

    #Get file name
    vid_player.filename = os.path.basename(vid_player.addr)
    vid_player.filename = os.path.splitext(vid_player.filename)[0]

    #Find the path to the processed video
    roots = list()
    for i in os.walk('yolov5/runs/detect/', topdown=False):
        roots.append(i)
    vid_player.addr = '%s%s%s%s' % (roots[-2][0], "/", vid_player.filename, ".mp4")

    #Display a video
    vid_player.load(vid_player.addr)
    vid_player.pack(expand=True, fill="both")
    play_pause_btn["text"] = "Play"

def play_pause():
    """ pauses and plays """
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"


LabelBg = tk.Label(root, i=bg)

buttonImage=tk.PhotoImage(file="button_image.png")
loadButton = tk.Button(root, command=Process, image=buttonImage,
                       highlightthickness = 0, bd=0, activebackground="#1E1E1E")

play_pause_btn = tk.Button(root, text="Play", command=play_pause)


LabelBg.place(x=0, y=0)


loadButton.place(x=53,y=455)


play_pause_btn.pack(
                ipadx=5,
                ipady=5,
                side='bottom',
                expand=False
                )


root.mainloop()