from common import gui
from common.data_structures import Experiment

from common.logging import *

def main():
    log("INFO", "Running main process")

    window = gui.construct_window()
    canvas = gui.construct_visualization_canvas(window)

    qubits = []
    for i in range(5):
        for j in range(5):
            qubit = gui.place_qubit(window, canvas, (i*100+100, j*100+100))
            qubits.append(qubit)
    
    for qubit in qubits:
        gui.move_qubit(window, canvas, qubit, [(50, 50) for _ in range(10)])

    return 0

if __name__ == "__main__":    
    main()
