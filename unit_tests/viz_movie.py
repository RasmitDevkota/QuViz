from tkinter import *
from tkinter.ttk import Button

import datetime
from threading import Lock

from PIL import ImageGrab
import imageio

root = Tk()
root.geometry("200x100")

canvas = Canvas(root)
canvas.pack(side=TOP, fill="both", expand=True)
 
button = Button(canvas, text = "Unit")
button.pack(side=TOP, pady=5)

label = Label(canvas, text="Click the button!", font=("Arial", 24))
label.pack(pady=20)

deletion_lock = Lock()

layer_queue = []

frame = 0
frames = []

width = 0
height = 0

def capture_frame():
    global frame

    posx = root.winfo_rootx()
    posy = root.winfo_rooty()
    width = root.winfo_width()
    height = root.winfo_height()

    xi = posx
    xf = posx + width
    yi = posy
    yf = posy + height

    print(xi, xf, yi, yf)

    img = ImageGrab.grab(bbox=(xi, yi, xf, yf))

    frames.append(img)

    frame += 1

def movie():
    print(frame, len(frames))
    imageio.mimsave("movie.gif", frames, fps=1)
    print("saved movie!")

def fancy_print(i, msg):
    label.config(text=msg)

    capture_frame()

    deletion_lock.acquire(False)

    del layer_queue[0][f"{i}"]
    if not layer_queue[0]:
        layer_queue.pop(0)

        if len(layer_queue) > 0:
            execute_next_layer()
        else:
            print("done!")
            movie()
    
    deletion_lock.release()

def example(i=0, l=0):
    root.after((2*i+2*l+1) * 1000, lambda : fancy_print(i, f"Printing after i+2*l+1={2*i+2*l+1} seconds..."))
    return True

n_layers = 1
for l in range(n_layers):
    layer_ops = {}

    for i in range(3):
        layer_ops[f"{i}"] = (
            example,
            {
                "i": i,
                "l": l
            }
        )
    
    layer_queue.append(layer_ops)

def execute_next_layer():
    layer_ops = layer_queue[0]
    for o, layer_op in layer_ops.items():
        method = layer_op[0]
        arguments = layer_op[1]

        print(f"{datetime.datetime.now}: {layer_op}")

        method(**arguments)

execute_next_layer()

mainloop()
