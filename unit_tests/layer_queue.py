from tkinter import Tk, mainloop, TOP
from tkinter.ttk import Button
from tkinter.messagebox import _show

import datetime
from threading import Lock

root = Tk()
root.geometry("200x100")
 
button = Button(root, text = "Unit")
button.pack(side = TOP, pady = 5)

deletion_lock = Lock()

layer_queue = []

def fancy_print(i, msg):
    _show(f"Operation {i}", msg)

    deletion_lock.acquire(False)

    del layer_queue[0][f"{i}"]
    if not layer_queue[0]:
        layer_queue.pop(0)

        if len(layer_queue) > 0:
            execute_next_layer()
    
    deletion_lock.release()

def example(i=0, l=0):
    root.after((2*i+2*l+1) * 1000, lambda : fancy_print(i, f"Printing after i+2*l+1={2*i+2*l+1} seconds..."))
    return True

n_layers = 3
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
