import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400, bg="gray")
canvas.pack()

cur_rec = 0

class Rect:
    def __init__(self, x1, y1, name):
        # Create a unique tag for each object
        tag = f"movable{id(self)}"
        rec = canvas.create_rectangle(x1, y1, x1 + 40, y1 + 40, fill='#c0c0c0', tag=(tag,))
        text = canvas.create_text(x1 + 20, y1 + 20, text=name, tag=(tag,))
        print(id(self), name, rec, text)

# Test rectangles
bob = Rect(20, 20, 'Bob')
rob = Rect(80, 80, 'Rob')
different_bob = Rect(160, 160, 'Bob')

print(id(bob), id(different_bob))

for i in range(1, 50):
    print(canvas.gettags(f"movable{id(bob)}"))
    for obj in canvas.gettags(f"movable{id(bob)}"):
        root.after(i * 50, canvas.move, *[obj, 1, 0])

root.mainloop()


# from tkinter import Tk, mainloop, TOP
# from tkinter.ttk import Button
# from tkinter.messagebox import _show

# import datetime
# from threading import Lock

# root = Tk()
# root.geometry('200x100')
 
# button = Button(root, text = 'Unit')
# button.pack(side = TOP, pady = 5)

# layer_deletion_lock = Lock()

# layer_queue = []

# def run_guilambda(i, guilambda, arg):
#     guilambda()

#     del layer_queue[0][f"{i}"]

#     layer_deletion_lock.acquire(False)

#     if not layer_queue[0]:
#         layer_queue.pop(0)

#         if len(layer_queue) > 0:
#             execute_next_layer()
    
#     layer_deletion_lock.release()

# def schedule_guilambda(i=0, delay=0, guilambda=None):
#     root.after(delay * 1000, lambda : run_guilambda(i, guilambda=guilambda))
#     return True

# n_layers = 3
# for l in range(n_layers):
#     layer_ops = {}

#     for i in range(3):
#         layer_ops[f"{i}"] = lambda : schedule_guilambda(i=i, delay=2*i+1, call=_show('Hello', f'Printing after 2*i+1={2*i+1} seconds...'))
    
#     layer_queue.append(layer_ops)

# def execute_next_layer():
#     layer_ops = layer_queue[0]
#     for o, layer_op in layer_ops.items():
#         method = layer_op[0]
#         arguments = layer_op[1]

#         print(f"{datetime.datetime.now}: {layer_op} - {method}({arguments})")

#         method(**arguments)

# execute_next_layer()
 
# mainloop()