from tkinter import Tk, mainloop, TOP
from tkinter.ttk import Button
from tkinter.messagebox import _show

import datetime
from threading import Lock

root = Tk()
root.geometry('200x100')
 
button = Button(root, text = 'Unit')
button.pack(side = TOP, pady = 5)

layer_deletion_lock = Lock()

layer_queue = []

def run_guilambda(i, guilambda, arg):
    guilambda()

    del layer_queue[0][f"{i}"]

    layer_deletion_lock.acquire(False)

    if not layer_queue[0]:
        layer_queue.pop(0)

        if len(layer_queue) > 0:
            execute_next_layer()
    
    layer_deletion_lock.release()

def schedule_guilambda(i=0, delay=0, guilambda=None):
    root.after(delay * 1000, lambda : run_guilambda(i, guilambda=guilambda))
    return True

n_layers = 3
for l in range(n_layers):
    layer_ops = {}

    for i in range(3):
        layer_ops[f"{i}"] = lambda : schedule_guilambda(i=i, delay=2*i+1, call=_show('Hello', f'Printing after 2*i+1={2*i+1} seconds...'))
    
    layer_queue.append(layer_ops)

def execute_next_layer():
    layer_ops = layer_queue[0]
    for o, layer_op in layer_ops.items():
        method = layer_op[0]
        arguments = layer_op[1]

        print(f"{datetime.datetime.now}: {layer_op} - {method}({arguments})")

        method(**arguments)

execute_next_layer()
 
mainloop()