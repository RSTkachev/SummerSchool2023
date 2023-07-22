import torch
import tkinter as tk
from tkinter import ttk, Canvas, PhotoImage
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import os


root = tk.Tk()


root.title('Recognizer')
root.iconbitmap('icon.ico')


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width / 2)
window_height = int(screen_height / 2)

# find the center point
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

panel = tk.Label(root)



# Model
model = torch.hub.load("yolov5", "yolov5x6", source="local")  # or yolov5n - yolov5x6, custom


def LoadFile():
    file_name = fd.askopenfilename()
    return file_name

def ProcessImage():
    global panel
    panel.destroy()
    panel = tk.Label(root)
    panel.addr = LoadFile()
    panel.im = Image.open(panel.addr)

    # Inference
    results = model(panel.im)

    # Results
    results.save()

    #Get file name
    panel.filename = os.path.basename(panel.addr)
    panel.filename = os.path.splitext(panel.filename)[0]

    #Find the path to the processed image
    roots = list()
    for i in os.walk('runs/detect/', topdown=False):
        roots.append(i)
    panel.addr = '%s%s%s%s' % (roots[-2][0], "/", panel.filename, ".jpg")

    #Display an image
    panel.im = Image.open(panel.addr)
    panel.im = panel.im.resize((window_width - 50, window_height - 50), Image.Resampling.LANCZOS)
    panel.image = ImageTk.PhotoImage(panel.im)
    panel['image'] = panel.image
    panel.pack()


loadButton = ttk.Button(root,
                        text='Download file',
                        command=lambda: ProcessImage()
                        )

loadButton.pack(
                ipadx=5,
                ipady=5,
                side='bottom',
                expand=False
                )

root.mainloop()