import tkinter as tk

class QuantumComposer:
    def __init__(self, master):
        self.master = master
        self.master.title("Quantum Circuit Composer")

        self.canvas = tk.Canvas(master, width=600, height=400, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.x_start = 100
        self.x_end = 500
        self.y_start = 50
        self.wire_spacing = 60

        self.wires = []  # List to hold wire IDs
        self.gate_size = 30
        self.gates = {}  # Dictionary to hold gate positions {(wire_index, segment_index): gate_id}
        self.num_segments = 10

        self.grid_size = (10, 6)

        self.selected_gate = None
        self.drag_data = {"item": None, "x": 0, "y": 0}

        self.draw_wires()

        self.draw_gate_buttons()

        self.canvas.bind("<Button-1>", self.place_gate)

    def draw_wires(self):
        for i in range(5):
            wire_id = self.canvas.create_line(self.x_start, self.y_start + i * self.wire_spacing, self.x_end, self.y_start + i * self.wire_spacing, width=2)
            self.wires.append((self.y_start + i * self.wire_spacing, wire_id))

    def draw_gate_buttons(self):
        gates = ["H", "X", "Y", "Z", "CX"]
        self.buttons = []
        for gate in gates:
            button = tk.Button(self.master, text=gate, command=lambda g=gate: self.select_gate(g))
            button.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)
            self.buttons.append(button)

        # add_wire_button = tk.Button(self.master, text="Add Wire", command=self.add_wire)
        # add_wire_button.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)
        # self.buttons.append(add_wire_button)

        # remove_wire_button = tk.Button(self.master, text="Remove Wire", command=self.remove_wire)
        # remove_wire_button.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)
        # self.buttons.append(remove_wire_button)

    def select_gate(self, gate):
        self.selected_gate = gate

    def place_gate(self, event):
        if event.x > self.x_end or event.y > self.y_start + len(self.wires) * self.wire_spacing:
            return
        
        wire_index = round((event.y - self.y_start)/self.wire_spacing)
        segment_index = round((event.x - self.x_start)/self.gate_size)

        if (wire_index, segment_index) in self.gates:
            for widget in self.gates[(wire_index, segment_index)]:
                self.canvas.delete(widget)
            
            del self.gates[(wire_index, segment_index)]
            
            return

        gate_x = self.x_start + segment_index * self.gate_size
        gate_y = self.y_start + wire_index * self.wire_spacing

        single_gates = ["H", "X", "Y", "Z"]
        gate = None
        if (self.selected_gate in single_gates):
            gate = self.canvas.create_rectangle(
                gate_x - self.gate_size // 2,
                gate_y - self.gate_size // 2,
                gate_x + self.gate_size // 2,
                gate_y + self.gate_size // 2,
                fill="lightblue", tag=(f"{wire_index}{segment_index}",)
            )
        else:
            for i in range(2):
                if (wire_index + i, segment_index) in self.gates:
                    for widget in self.gates[(wire_index, segment_index)]:
                        self.canvas.delete(widget)
                    del self.gates[(wire_index, segment_index)]
            # if wire_index + 2 >= len(self.wire) - 1:
            #     return
            gate = self.canvas.create_rectangle(
                gate_x - self.gate_size // 2,
                gate_y - self.gate_size // 2,
                gate_x + self.gate_size // 2,
                gate_y + self.gate_size * 2.75,
                fill="lightblue", tag=(f"{wire_index}{segment_index}",)
            )


        text = self.canvas.create_text(gate_x, gate_y, text=self.selected_gate, tag=(f"{wire_index}{segment_index}",))
        self.gates[(wire_index, segment_index)] = [gate, text]

        return True

    # def add_wire(self):
    #     y = self.wires[-1][0] + 60
    #     wire_id = self.canvas.create_line(100, y, 500, y, width=2)
    #     self.wires.append((y, wire_id))

    # def remove_wire(self):
    #     if len(self.wires) > 1:
    #         _, wire_id = self.wires.pop()
    #         self.canvas.delete(wire_id)
    #         for segment in self.gates.copy():
    #             if segment[0] == len(self.wires):
    #                 self.canvas.delete(self.gates.pop(segment))

def main():
    root = tk.Tk()
    app = QuantumComposer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# import tkinter as tk

# root = tk.Tk()
# canvas = tk.Canvas(root, width=400, height=400, bg="gray")
# canvas.pack()

# cur_rec = 0

# class Rect:
#     def __init__(self, x1, y1, name):
#         # Create a unique tag for each object
#         tag = f"movable{id(self)}"
#         rec = canvas.create_rectangle(x1, y1, x1 + 40, y1 + 40, fill='#c0c0c0', tag=(tag,))
#         text = canvas.create_text(x1 + 20, y1 + 20, text=name, tag=(tag,))
#         print(id(self), name, rec, text)

# # Test rectangles
# bob = Rect(20, 20, 'Bob')
# rob = Rect(80, 80, 'Rob')
# different_bob = Rect(160, 160, 'Bob')

# print(id(bob), id(different_bob))

# for i in range(1, 50):
#     print(canvas.gettags(f"movable{id(bob)}"))
#     for obj in canvas.gettags(f"movable{id(bob)}"):
#         root.after(i * 50, canvas.move, *[obj, 1, 0])

# root.mainloop()


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