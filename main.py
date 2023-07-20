import tkinter as tk
from tkinter import ttk, Canvas, PhotoImage
from tkinter import filedialog as fd
from PIL import Image, ImageTk

root = tk.Tk()

def LoadFile():
    file_name = fd.askopenfilename()
    return file_name

def OpenImg():
    panel = tk.Label(root)
    panel.im = Image.open(LoadFile())
    print(panel.im.size)
    panel.image = ImageTk.PhotoImage(panel.im)
    panel['image'] = panel.image
    panel.pack()



root.title('Recognizer')
root.iconbitmap('pythontutorial.ico')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width / 2)
window_height = int(screen_height / 2)

# find the center point
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

loadButton = ttk.Button(root,
                        text='Download file',
                        command=lambda: OpenImg()
                        )

loadButton.pack(
                ipadx=5,
                ipady=5,
                expand=True
                )

root.mainloop()
