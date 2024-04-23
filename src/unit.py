from tkinter import *
from PIL import ImageTk, Image

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

import matplotlib.pyplot as plt

qc = QuantumCircuit(2)
qc.h(0)
qc.cz(0, 1)

figure = qc.draw("mpl")

plt.clf()

# statevector_latex = "$" + Statevector(qc).draw("latex_source") + "$"
# print()

# text = plt.text(0.5, 0.5, statevector_latex)
# print(text.bbox)
# # plt.title(statevector_latex)
# plt.savefig("statevector.png")

root = Tk()
# img = ImageTk.PhotoImage(Image.open("circuit.png"))
# panel = Label(root, image=img, text="Circuit")
# panel.pack(side = "bottom", fill = "both", expand = "yes")





root.mainloop()

# import tkinter as tk

# import matplotlib
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# from qiskit import QuantumCircuit
# from qiskit.quantum_info import Statevector

# matplotlib.use('TkAgg')
# # matplotlib.rcParams["text.usetex"] = True

# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         self.title('Tkinter Matplotlib Demo')

#         # create a figure
#         figure = Figure(figsize=(6, 4), dpi=100)

#         qc = QuantumCircuit(2)
#         qc.h(0)
#         qc.cz(0, 1)
#         qc.draw("mpl", output="circuit.png")

#         # create FigureCanvasTkAgg object
#         figure_canvas = FigureCanvasTkAgg(figure, self)

#         axes = figure.add_subplot()
#         axes.get_xaxis().set_visible(False)
#         axes.get_yaxis().set_visible(False)

#         tmptext = "$" + Statevector(qc).draw("latex_source") + "$"

#         figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# if __name__ == '__main__':
#     app = App()
#     app.mainloop()
